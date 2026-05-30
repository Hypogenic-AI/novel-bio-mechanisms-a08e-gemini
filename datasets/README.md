# Research Datasets

## Swiss-Prot Subset
- **Source**: [UniProt Swiss-Prot](https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz)
- **Description**: A subset of 1,000 proteins from the manually curated Swiss-Prot database, filtered for length < 1022.
- **Format**: FASTA
- **Use**: Training and evaluating Sparse Autoencoders (SAEs) on ESM-2 embeddings.

## Download Instructions
The full Swiss-Prot dataset can be downloaded from:
`https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz`

The subset was created using the `subset_fasta.py` script from the `interPLM` repository.
