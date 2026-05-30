# Resources Catalog

## Summary
This document catalogs the papers, datasets, and code repositories gathered for the research project "Discovering Novel Biological Mechanisms from Protein Language Models."

## Papers
Total papers downloaded: 3

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| InterPLM | Simon & Zou | 2024 | papers/2412.12101_InterPLM.pdf | SAE framework for ESM-2 features. |
| Mechanistic Biology | Adams et al. | 2025 | papers/2406.04093_Mechanistic_Biology.pdf | Hypothesizing unknown mechanisms. |
| ESM-2 | Lin et al. | 2022 | papers/2207.03061_ESM2.pdf | Foundation pLM for structure prediction. |

See `papers/README.md` for detailed descriptions.

## Datasets
Total datasets: 1 (with subset)

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| Swiss-Prot | UniProt | 1000 samples | Annotation | datasets/uniprot/ | Curated subset for SAE analysis. |

See `datasets/README.md` for detailed descriptions and download instructions.

## Code Repositories
Total repositories cloned: 2

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| InterPLM | github.com/ElanaPearl/interPLM | Feature discovery | code/interPLM/ | Toolkit for SAEs and dashboard. |
| InterProt | github.com/etowahadams/interprot | Mechanistic Biology | code/interprot/ | Training and interpretation scripts. |

See `code/README.md` for detailed descriptions.

## Resource Gathering Notes

### Search Strategy
- Used `paper-finder` for initial literature search.
- Conducted targeted search for ArXiv IDs of key papers.
- Identified standard benchmarks (FLIP, ProteinGym) and gold-standard datasets (Swiss-Prot).
- Cloned state-of-the-art repositories for SAE-based interpretability in pLMs.

### Selection Criteria
- **Relevance**: Focused on Sparse Autoencoders applied to Protein Language Models, as this is the current state-of-the-art for the research hypothesis.
- **Maturity**: Selected repositories with clear documentation and pre-trained models.
- **Data Quality**: Chose Swiss-Prot over UniRef for evaluation due to its high-quality manual annotations.

### Challenges Encountered
- ArXiv API rate limiting (mitigated by direct curl downloads).
- Missing dependencies in cloned repos (mitigated by manual installation in venv).

## Recommendations for Experiment Design

1. **Primary Methodology**: Adopt the Sparse Autoencoder (SAE) approach from `InterPLM`. It provides a clean way to decompose embeddings into interpretable features.
2. **Base Model**: Use `ESM-2-8M` for initial experiments (fast iteration) and `ESM-2-650M` for validating more complex features.
3. **Data Pipeline**:
   - Extract embeddings for the Swiss-Prot subset.
   - Run SAE inference to get feature activations.
   - Use the `InterPLM` analysis scripts to cross-reference activations with UniProt annotations.
4. **Hypothesis Generation**: Identify features with high activation variance but low correlation with known domains. Use an LLM (e.g., Claude/GPT-4) to describe the motifs captured by these features, looking for structural or functional patterns (e.g., specific residue clusters, secondary structure transitions).
