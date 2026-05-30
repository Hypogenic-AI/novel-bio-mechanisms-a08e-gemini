# Discovering Novel Biological Mechanisms from Protein Language Models

## Project Overview
This repository contains the code and results for an automated research pipeline that investigates whether protein language models (pLMs) encode novel biological mechanisms. By applying Sparse Autoencoders (SAEs) to ESM-2 embeddings and leveraging Large Language Models (LLMs) for interpretation, we demonstrate how AI foundation models can act as active hypothesis generators for uncharacterized protein motifs.

## Key Findings
- **Automated Pipeline Success:** Successfully extracted sparse, interpretable features from the ESM-2 (8M) model using the `InterPLM` framework.
- **Hypothesis Generation:** Identified highly active, sequence-specific "orphan" features and used GPT-4o to propose plausible biochemical motifs (e.g., "Charged Beta-Turns" and "Positively-Charged Helix Caps").
- **LLM Sensitivity:** The LLM could accurately identify biophysical properties in the sequence windows, though a random baseline test highlighted the need for rigorous statistical filtering, as LLMs will infer structure even in random fragments.
- **Feature Redundancy:** Discovered instances of "feature splitting," where multiple SAE features trigger on identical sequences to represent slight variations of the same underlying motif.

## How to Reproduce

### Environment Setup
The project uses `uv` for fast dependency management.
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install required dependencies
uv pip install torch torchvision nnsight transformers biopython datasets einops fair-esm h5py huggingface-hub matplotlib multiprocess pandas plotly pyyaml py3dmol scikit-learn scipy seaborn streamlit typed-argument-parser umap-learn wandb openai anthropic tenacity
```

### Running the Experiment
Ensure you have the required API keys (e.g., `OPENAI_API_KEY`) set in your environment.
```bash
python src/run_pipeline.py
```

## File Structure
- `src/run_pipeline.py`: Main execution script that extracts ESM-2 embeddings, runs the SAE, and queries the LLM.
- `results/hypotheses.json`: The LLM-generated hypotheses for the identified SAE features.
- `results/feature_stats.json`: Raw statistics for the feature activations across the dataset.
- `REPORT.md`: The full comprehensive research report.
- `planning.md`: Initial experimental design and methodology.

## Detailed Report
Please read [REPORT.md](./REPORT.md) for full methodological details, experimental results, and scientific discussion.