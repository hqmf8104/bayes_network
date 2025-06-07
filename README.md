# Evidence Network Builder

An interactive Streamlit app for constructing and analyzing evidence-hypothesis graphs.  
Leverages OpenAI’s GPT to extract evidence and hypotheses from a narrative, lets you curate nodes & edges, specify priors and reliabilities, and then performs Bayesian-style updates and visualizations via NetworkX and PyVis.

## Theory

### Logistic Evidence-Weighting Rule

1. **Purpose**  
   Convert qualitative beliefs (baseline plausibility and importance weights) into a numerical probability for a binary hypothesis \(H\).  

2. **Inputs**  
   - **Baseline probability** \(p_0\): \(P(H=\text{True})\) if none of its parents are true.  
   - **Importance weights** \(w_i\) (or odds multipliers \(r_i\)): strength of support/undermining from each parent.  

3. **Formula**  
   \[
   \beta_0 = \operatorname{logit}(p_0) = \ln\!\bigl(\tfrac{p_0}{1-p_0}\bigr),\quad
   \beta_i = \ln(r_i)
   \]
   \[
   P(H=\text{True}\mid X_1,\dots,X_k)
     = \sigma\bigl(\beta_0 + \sum_{i=1}^k \beta_i\,X_i\bigr),
   \quad \sigma(z)=\frac1{1+e^{-z}}
   \]

4. **Benefits**  
   - Compact: only \(k+1\) parameters vs.\ \(2^k\) rows in a full CPT  
   - Additive in log-odds: each weight acts as an independent “vote”  
   - Smooth & bounded: always in [0,1]  
   - Learnable: fits standard logistic regression frameworks  

### Binary Network Propagation Guide

1. **Leaf Evidence**  
   For each piece of raw evidence \(E_i\), get its reliability \(P(E_i=\text{True})\).

2. **Hypothesis Rules**  
   For each non-leaf hypothesis, use the logistic conditional rule above.

3. **Propagation Steps**  
   1. **Enumerate** all \(2^m\) truth-patterns of the \(m\) leaf evidences.  
   2. **Compute** pattern probability: \(\prod_i P(E_i)\) or \(\prod_i [1-P(E_i)]\) as appropriate.  
   3. **Apply** logistic rule to get \(P(H_j=\text{True}\mid \text{pattern})\).  
   4. **Accumulate** each pattern’s contribution:  
      \[
        \text{Contribution} = P(\text{pattern}) \times P(H=\text{True}\mid\text{pattern})
      \]
   5. **Sum** across patterns for \(P(H=\text{True})\); use \(1 - P(H=\text{True})\) for false.

4. **Use-Cases**  
   - Small models: full-pattern tables for exact analysis and sensitivity checks  
   - Larger models: delegate numeric propagation to a Bayesian-network library  

## Example Files

- **test_json_001.json**  
  A sample network dump created using the tool. It contains **two separate networks** for you to load via the “Upload JSON” control and experiment with all UI sections without starting from scratch. :contentReference[oaicite:0]{index=0}

- **test_prompt.md**  
  The exact prompt template used in the code to drive the LLM extraction of evidence and hypotheses. You can review or tweak it before pasting into the “Submit Narrative” panel. :contentReference[oaicite:1]{index=1}

## Features

- **Narrative → JSON**: Paste a narrative or upload JSON—GPT extracts `evidence`, `hypotheses`, and their `connections`.  
- **Graph Editing**: Add or delete evidence/hypothesis nodes and directed edges in the UI.  
- **Parameter Inputs**: Assign qualitative priors, evidence reliabilities, and edge-strength multipliers.  
- **Bayesian Tables**: Compute updated probabilities (“Calc Prior (%)”) and full truth-tables per connected component.  
- **Interactive Visualization**: Render and explore the directed graph with color-coded edges in a PyVis widget.  
- **Export**: Download the full network (including all parameters) as pretty JSON.

## Getting Started

### Prerequisites

- Python 3.9+  
- A virtual environment (recommended) 
