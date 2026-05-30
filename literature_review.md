# Literature Review: Discovering Novel Biological Mechanisms from Protein Language Models

## Research Area Overview
The field of protein language models (pLMs) has advanced rapidly, with models like ESM-2 demonstrating the ability to capture complex biological information from sequences alone. However, these models are often treated as "black boxes." Recent research has pivoted towards **Mechanistic Interpretability**, specifically using **Sparse Autoencoders (SAEs)** to decompose the high-dimensional internal representations of pLMs into human-interpretable features. The hypothesis is that these latent features may correspond to biological mechanisms that are currently unknown or unannotated.

## Key Papers

### 1. InterPLM: Discovering Interpretable Features in Protein Language Models via Sparse Autoencoders
- **Authors**: Elana Simon, James Y. Zou
- **Year**: 2024 (Nature Methods 2025)
- **Key Contribution**: Introduces a framework to extract and analyze interpretable features from ESM-2 using SAEs.
- **Methodology**: Trains SAEs on ESM-2 embeddings to identify thousands of latent features. Uses an LLM-based pipeline to automatically interpret features that do not map to known annotations.
- **Datasets Used**: UniRef50 (training), Swiss-Prot (evaluation).
- **Results**: Discovered that PLMs represent concepts in superposition. Identified novel, coherent concepts that do not map to existing annotations.
- **Relevance**: Provides the primary methodology and visualization tools (InterPLM.ai) for this research.

### 2. From Mechanistic Interpretability to Mechanistic Biology
- **Authors**: Etowah Adams, Liam Bai, Minji Lee, Yiyang Yu, Mohammed AlQuraishi
- **Year**: 2024/2025
- **Key Contribution**: Focuses on bridging the gap between model interpretability and biological discovery.
- **Methodology**: Similar SAE-based approach on ESM-2's residual stream. Characterizes features as "generic" vs. "family-specific."
- **Results**: Demonstrated that known sequence determinants (e.g., thermostability) can be identified. Proposed a hypothesis-generation pipeline for unknown mechanisms.
- **Relevance**: Directly supports the research hypothesis by showing how SAE features can be used to generate biological hypotheses.

### 3. ESM-2: Evolutionary-scale prediction of atomic-level protein structure with a language model
- **Authors**: Lin et al. (Meta AI)
- **Year**: 2022
- **Key Contribution**: Established the ESM-2 model as a state-of-the-art pLM.
- **Methodology**: Large-scale transformer trained on UniRef50.
- **Results**: Showed that internal representations contain enough information to predict 3D structure with high accuracy.
- **Relevance**: The foundational model upon which the interpretability studies are built.

## Common Methodologies
- **Sparse Autoencoders (SAEs)**: Used to solve the "superposition" problem in neural networks, allowing for the extraction of monosemantic (interpretable) features.
- **Linear Probing**: Used to verify if specific biological properties (like binding sites) are linearly encoded in the embeddings or SAE features.
- **LLM-aided Interpretation**: Using large language models to describe the biological patterns captured by novel SAE features.

## Evaluation Metrics
- **Reconstruction Fidelity**: How well the SAE can reconstruct the original embedding.
- **Sparsity (L0 norm)**: Number of active features per protein.
- **Concept Alignment**: Correlation between feature activations and known biological annotations (e.g., from UniProt).

## Datasets in the Literature
- **UniRef50/100**: Standard for training large pLMs.
- **Swiss-Prot**: The gold standard for high-quality, manually curated annotations.
- **ProteinGym**: Used for evaluating the impact of mutations on function.

## Gaps and Opportunities
- **Verification of Novel Motifs**: While SAEs identify "novel" features, experimental validation is still largely missing.
- **Cross-Model Consistency**: Do different models (e.g., ESM vs. ProtBert) learn the same "novel" mechanisms?
- **Dynamic Mechanisms**: Most current work focuses on static sequences; capturing conformational changes or dynamic interactions remains a challenge.

## Recommendations for Our Experiment
- **Primary Method**: Use the `InterPLM` framework to train or load pre-trained SAEs for ESM-2.
- **Primary Dataset**: Use `Swiss-Prot` for its rich annotations to differentiate between "known" and "novel" features.
- **Focus**: Targeted analysis of features that correlate strongly with function but have low overlap with existing Pfam/UniProt domains.
