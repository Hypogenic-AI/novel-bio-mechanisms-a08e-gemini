import os
import sys
# Set up PYTHONPATH for interPLM so we can import it
sys.path.append(os.path.abspath("code/interPLM"))

import torch
import numpy as np
from Bio import SeqIO
from transformers import AutoTokenizer, EsmModel
from interplm.sae.inference import load_sae_from_hf
import openai
import json
import re
import random

def main():
    # Setup
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {DEVICE}")

    # Load the dataset
    fasta_path = "datasets/uniprot/subset_1000.fasta"
    records = list(SeqIO.parse(fasta_path, "fasta"))

    # Only use the first 100 for speed
    records = records[:100]
    print(f"Loaded {len(records)} sequences for analysis")

    # Load ESM-2 model
    model_name = "facebook/esm2_t6_8M_UR50D"
    print(f"Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = EsmModel.from_pretrained(model_name).to(DEVICE)
    model.eval()

    # Load SAE
    print("Loading pre-trained SAE for ESM-2 layer 4...")
    sae = load_sae_from_hf(plm_model="esm2-8m", plm_layer=4)
    sae = sae.to(DEVICE)
    print("SAE loaded successfully.")

    # Extract embeddings and features
    all_features = []
    
    print("Extracting features from sequences...")
    with torch.no_grad():
        for i, record in enumerate(records):
            seq = str(record.seq)
            
            # Sub-sequence if too long for simple processing
            if len(seq) > 1022:
                seq = seq[:1022]
                
            inputs = tokenizer(seq, return_tensors="pt", add_special_tokens=True).to(DEVICE)
            outputs = model(**inputs, output_hidden_states=True)
            
            # Layer 4 embeddings (0 is embed, 1..6 are layers)
            layer_4_emb = outputs.hidden_states[4][0] # shape (seq_len + 2, 320)
            
            # Remove special tokens (CLS and EOS)
            aa_embds = layer_4_emb[1:-1] # shape (seq_len, 320)
            
            # Encode with SAE
            features = sae.encode(aa_embds) # shape (seq_len, num_features)
            
            # Move to CPU for processing
            features_cpu = features.cpu().numpy()
            
            # Store max activation per feature for this sequence
            max_acts = features_cpu.max(axis=0)
            max_idx = features_cpu.argmax(axis=0)
            
            all_features.append({
                'seq_id': record.id,
                'seq': seq,
                'max_acts': max_acts,
                'max_idx': max_idx
            })

    print("Aggregating activations across the dataset...")
    # Find the top features overall
    num_features = all_features[0]['max_acts'].shape[0]

    feature_stats = []
    for f_idx in range(num_features):
        max_val = float(max([item['max_acts'][f_idx] for item in all_features]))
        freq = float(sum([(item['max_acts'][f_idx] > 0.1) for item in all_features]) / len(all_features))
        
        feature_stats.append({
            'feature_idx': f_idx,
            'max_val': max_val,
            'frequency': freq
        })

    # Sort features by maximum activation and frequency
    feature_stats.sort(key=lambda x: (x['max_val'], x['frequency']), reverse=True)

    # Select top 5 features
    top_features = [f for f in feature_stats if f['frequency'] < 0.9][:5]

    print("Top features selected for analysis:")
    for f in top_features:
        print(f"Feature {f['feature_idx']}: max_act={f['max_val']:.2f}, freq={f['frequency']:.2f}")

    # Extract context windows for top features
    print("Extracting context windows for LLM analysis...")
    hypotheses = {}

    # Initialize client
    try:
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    except Exception as e:
        print(f"Failed to initialize OpenAI client: {e}.")
        sys.exit(1)

    for f in top_features:
        f_idx = f['feature_idx']
        
        seqs_with_acts = []
        for item in all_features:
            seqs_with_acts.append({
                'seq_id': item['seq_id'],
                'seq': item['seq'],
                'act': float(item['max_acts'][f_idx]),
                'idx': int(item['max_idx'][f_idx])
            })
        
        seqs_with_acts.sort(key=lambda x: x['act'], reverse=True)
        top_seqs = seqs_with_acts[:5]
        
        contexts = []
        for item in top_seqs:
            if item['act'] < 0.1:
                continue
            
            idx = item['idx']
            seq = item['seq']
            start = max(0, idx - 10)
            end = min(len(seq), idx + 10)
            context = seq[start:end]
            
            rel_idx = idx - start
            highlighted = context[:rel_idx] + "[" + context[rel_idx] + "]" + context[rel_idx+1:]
            
            contexts.append(f"Protein {item['seq_id']}: {highlighted} (Activation: {item['act']:.2f})")
        
        if not contexts:
            continue
            
        print(f"\nFeature {f_idx} contexts:")
        for ctx in contexts:
            print(f"  {ctx}")
            
        # Generate hypothesis with LLM
        prompt = f"""
        You are an expert computational biologist analyzing latent features of a protein language model.
        A specific "sparse autoencoder feature" (Feature {f_idx}) activates highly on the following protein sequence windows.
        The exact residue where the peak activation occurs is marked with brackets [].
        
        Sequence contexts:
        {chr(10).join(contexts)}
        
        Based ONLY on these sequences, propose a novel biological hypothesis for what structural or biochemical motif this feature might represent. 
        Consider chemical properties (hydrophobicity, charge), secondary structure propensity (alpha-helix, beta-sheet), or known binding motifs.
        
        Provide your answer in this JSON format:
        {{
            "hypothesized_motif": "Short name for the motif",
            "description": "1-2 sentence description of the biochemical/structural pattern",
            "reasoning": "Why you think this based on the sequence windows provided"
        }}
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a computational biologist. Output JSON exactly matching the requested format."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            hypothesis = json.loads(content)
            hypotheses[f_idx] = hypothesis
            print(f"Hypothesis generated for Feature {f_idx}: {hypothesis['hypothesized_motif']}")
        except Exception as e:
            print(f"LLM API call failed for Feature {f_idx}: {e}")

    # Generate Random Baseline
    print("\nGenerating Random Baseline Hypothesis...")
    random.seed(42)
    random_item = random.choice(all_features)
    random_seq = random_item['seq']
    if len(random_seq) > 20:
        random_idx = random.randint(10, len(random_seq) - 10)
        random_start = max(0, random_idx - 10)
        random_end = min(len(random_seq), random_idx + 10)
        random_context = random_seq[random_start:random_end]
        random_highlighted = random_context[:10] + "[" + random_context[10] + "]" + random_context[11:]
        
        random_prompt = f"""
        You are an expert computational biologist analyzing latent features of a protein language model.
        A specific "sparse autoencoder feature" (Feature RANDOM) activates highly on the following protein sequence windows.
        The exact residue where the peak activation occurs is marked with brackets [].
        
        Sequence contexts:
        Protein RANDOM: {random_highlighted} (Activation: 5.0)
        
        Based ONLY on these sequences, propose a novel biological hypothesis for what structural or biochemical motif this feature might represent. 
        Consider chemical properties (hydrophobicity, charge), secondary structure propensity (alpha-helix, beta-sheet), or known binding motifs.
        
        Provide your answer in this JSON format:
        {{
            "hypothesized_motif": "Short name for the motif",
            "description": "1-2 sentence description of the biochemical/structural pattern",
            "reasoning": "Why you think this based on the sequence windows provided"
        }}
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a computational biologist. Output JSON exactly matching the requested format."},
                    {"role": "user", "content": random_prompt}
                ]
            )
            content = response.choices[0].message.content
            baseline = json.loads(content)
            print(f"Random Baseline Hypothesis: {baseline['hypothesized_motif']}")
            hypotheses["RANDOM_BASELINE"] = baseline
        except Exception as e:
            print(f"LLM API call failed for Random Baseline: {e}")

    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/hypotheses.json", "w") as f:
        json.dump(hypotheses, f, indent=2)

    # Save raw feature stats for analysis
    with open("results/feature_stats.json", "w") as f:
        json.dump(feature_stats[:100], f, indent=2)

    print("\nPipeline complete. Results saved to results/hypotheses.json")

if __name__ == "__main__":
    main()
