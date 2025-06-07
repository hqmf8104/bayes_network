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
β₀ = logit(p₀) = ln(p₀ / (1 − p₀))

- **Edge weight log-odds**  
βᵢ = ln(rᵢ)

- **Posterior probability**  
P(H = True | X) = σ(β₀ + Σᵢ βᵢ·Xᵢ),
where σ(z) = 1 / (1 + e^(−z))


### Binary Network Propagation

1. Enumerate all truth‐value combinations of input evidence.  
2. Compute each combination’s probability and the corresponding hypothesis probability via the logistic rule.  
3. Aggregate to yield exact posterior probabilities and full truth‐tables.

---

## Example Files

- **test_json_001.json**  
Contains two prebuilt networks for quick testing.

- **test_prompt.md**  
Houses the exact LLM prompt template used for narrative extraction.

---

## Installation & Usage

1. **Clone the repo**  
 ```bash
 git clone https://github.com/hqmf8104/bayes_network.git
 cd bayes_network

2. **Clone the repo**  
 ```bash
 python -m venv .venv
 # macOS/Linux
 source .venv/bin/activate
 # Windows PowerShell
 .\.venv\Scripts\Activate

3. **Install dependencies**
 ```bash 
 pip install -r requirements.txt

4. **Set your OpenAI API key**
 ```bash 
 # macOS/Linux
 export OPENAI_API_KEY="your_api_key_here"
 # Windows PowerShell
 $env:OPENAI_API_KEY="your_api_key_here"

5. **Run the app**
 ```bash 
 streamlit run ui.py


###License
This project is licensed under the MIT License. Feel free to modify and extend!

© 2025 Evidence Network Builder