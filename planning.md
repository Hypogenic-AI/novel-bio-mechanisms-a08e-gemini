## Motivation & Novelty Assessment

### Why This Research Matters
Protein language models (pLMs) encode complex biological information, but their internal representations remain largely opaque. By treating these models as hypothesis generators rather than mere predictors, we can uncover new biological motifs and mechanisms. This is critical for advancing protein engineering and deepening our understanding of biology beyond current human-curated annotations.

### Gap in Existing Work
Existing mechanistic interpretability studies on pLMs typically map latent representations back to known functional annotations (like UniProt or Pfam). The field currently lacks systematic pipelines to analyze highly active, context-specific latent features that *do not* map to any known biology, and to explicitly use them to formulate novel, testable biological hypotheses.

### Our Novel Contribution
We propose an automated pipeline that leverages Sparse Autoencoders (SAEs) on ESM-2 to identify "orphan" latent features—those with strong, sequence-specific activations but poor correlation with existing databases. We then uniquely employ LLMs (e.g., Claude/GPT-4) to semantically interpret the sequence contexts of these novel features and generate explicit hypotheses regarding uncharacterized structural motifs or interaction sites.

### Experiment Justification
- **Experiment 1 (Feature Extraction):** Required to obtain interpretable latent representations of the protein sequences using ESM-2 and an SAE.
- **Experiment 2 (Annotation Alignment):** Necessary to filter out features that correspond to known biological annotations (Swiss-Prot/UniProt), isolating the "orphan" features.
- **Experiment 3 (LLM Hypothesis Generation):** Essential to conceptually translate the sequence contexts of these novel features into meaningful, testable biological hypotheses.

## Research Question
Can Sparse Autoencoder (SAE) features of Protein Language Models (pLMs) reveal and help describe biologically meaningful motifs that are currently unannotated in standard databases?

## Background and Motivation
Despite their predictive success, pLMs operate as black boxes. Mechanistic interpretability through SAEs has shown promise in making pLM features understandable. If we assume pLMs learn a robust model of biology, their unexplained representations might correspond to real, but undiscovered, biological mechanisms. Harnessing these internal representations could accelerate scientific discovery.

## Hypothesis Decomposition
1. ESM-2 representations encode functional properties not captured by Swiss-Prot or Pfam.
2. Sparse autoencoders can disentangle these properties into isolated, monosemantic features.
3. Features that frequently activate on unannotated regions possess conserved sequence or structural patterns.
4. Large Language Models can recognize patterns in the sequence windows corresponding to these orphan features to suggest new functional hypotheses.

## Proposed Methodology

### Approach
We will leverage the existing `InterPLM` framework to process a subset of 1,000 Swiss-Prot sequences through ESM-2 (8M parameters) and an associated pre-trained SAE. We will then correlate the SAE activations with known UniProt annotations, isolate features with high activation variance but low annotation correlation, and use an LLM API to interpret their highest-activating contexts.

### Experimental Steps
1. **Data Prep:** Load the `subset_1000.fasta` from the `datasets/uniprot/` directory.
2. **Feature Extraction:** Use `InterPLM`'s pre-trained SAE for `esm2-8m` to obtain feature activations for all amino acids in the sequence subset.
3. **Annotation Check:** Implement a correlation check between feature activations and existing UniProt annotations to define "known" vs "novel" features.
4. **LLM Hypothesis Generation:** For the top 5 "novel" features, extract the 20 amino-acid window around the peak activation in the top 10 sequences. Send these sequences to an LLM API to hypothesize common biological properties (e.g., charge, hydrophobicity patterns).

### Baselines
Randomly selected 20-amino-acid windows from the dataset will be fed to the LLM to verify whether the hypothesis generated for SAE features is significantly more coherent and specific than chance.

### Evaluation Metrics
- **Sparsity:** L0 norm of the SAE activations.
- **Alignment Score:** Correlation coefficient between feature activations and known UniProt properties.
- **Hypothesis Coherence:** Qualitative and quantitative (LLM self-evaluated) coherence of the proposed biological mechanisms against the random baseline.

### Statistical Analysis Plan
We will compare the distribution of alignment scores to identify the threshold for "unannotated." We will also conduct a paired comparison of LLM confidence/coherence scores for SAE-driven hypotheses vs. random-window hypotheses.

## Expected Outcomes
We expect to find a subset of SAE features that activate consistently across diverse proteins but have near-zero correlation with existing UniProt metadata. We expect the LLM to successfully propose plausible, shared biochemical motifs for these features, outperforming random baselines.

## Timeline and Milestones
- **Setup & Data (20 min):** Environment configuration, data loading.
- **Implementation (45 min):** Integration of InterPLM, extraction pipeline, annotation correlation logic.
- **Experimentation (45 min):** Running extraction, identifying novel features, running LLM prompts.
- **Analysis (30 min):** Comparing LLM outputs, formatting results.
- **Documentation (30 min):** Compiling REPORT.md and README.md.

## Potential Challenges
- **Compute constraints:** If processing 1000 sequences is too slow, we will further subset to 100 sequences for fast iteration.
- **LLM Hallucinations:** LLMs might hallucinate biological meaning in random sequences. The random baseline is crucial for mitigating this.
- **Missing Annotations:** "Novel" features might just be known features missing from our specific annotation subset.

## Success Criteria
1. Successful extraction of SAE features for the dataset.
2. Identification of at least 5 "orphan" features with high activation but low annotation correlation.
3. Generation of coherent, testable hypotheses for these features via an LLM, showing clear distinction from random baselines.
