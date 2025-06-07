# Evidence Network Builder

An interactive Streamlit application for constructing, editing, and analyzing evidence–hypothesis networks. This tool uses OpenAI’s GPT to extract nodes from narrative text, allows manual graph editing, captures user‐defined likelihoods and weights, and performs logistic‐based probability updates and full truth‐table enumerations. It also offers an interactive PyVis visualization and JSON import/export.

---

## Features

- **Narrative → JSON**  
  Paste or upload a narrative; GPT extracts evidence items (`E*`), hypotheses (`H*`), and directed connections.

- **Graph Editing**  
  Add or delete evidence/hypothesis nodes and edges via an intuitive Streamlit UI.

- **Parameter Inputs**  
  Specify qualitative priors for hypotheses, reliability for evidence, and odds‐multiplier weights for edges.

- **Bayesian Tables**  
  - Computes “Calc Prior (%)” for each hypothesis based on incoming evidence  
  - Generates full truth‐tables (2ᵐ combinations) for each network component  

- **Interactive Visualization**  
  Renders the directed graph in PyVis with color‐coded, thickness‐scaled edges.

- **Import/Export**  
  - Upload or paste JSON to initialize the network  
  - Download the complete network (nodes, connections, priors, weights) as pretty JSON  

- **Utility Scripts**  
  - `save.py`: Snapshot your environment, update `requirements.txt`, commit, and push  
  - `load.py`: Pull latest changes, check Python version, and install dependencies  

---

## Theory Overview

### Logistic Evidence‐Weighting Rule

- **Baseline log-odds**  
