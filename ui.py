import streamlit as st

# ✅ 1st: set page config
st.set_page_config(
    page_title="Evidence Network Builder",
    layout="wide",
)

# ✅ All other imports
import json
import networkx as nx
from pyvis.network import Network
import pandas as pd
import textwrap
import streamlit.components.v1 as components
import tempfile
import os
import textwrap
import math
from openai import OpenAI
import itertools
import streamlit as st
from streamlit.runtime.scriptrunner.script_runner import RerunException

# -----------------------------
# a) Functions
# -----------------------------

def get_prob_color(prob: float) -> str:
    # Simple red (low) → green (high) gradient
    r = int((1 - prob) * 255)
    g = int(prob * 255)
    b = 100  # fixed for contrast
    return f"rgb({r},{g},{b})"


def clean_state(g):
    # 1) Remove priors for hypotheses that no longer exist
    for h_id in list(st.session_state.priors):
        if h_id not in g.nodes or g.nodes[h_id].get("group") != "hypothesis":
            del st.session_state.priors[h_id]

    # 2) Remove truth‐prob entries for evidence that no longer exist
    for e_id in list(st.session_state.truth_probs):
        if e_id not in g.nodes or g.nodes[e_id].get("group") != "evidence":
            del st.session_state.truth_probs[e_id]

    # 3) Remove edge strength entries for edges that no longer exist
    for key in list(st.session_state.edge_strengths):
        if key not in g.edges:
            del st.session_state.edge_strengths[key]


# -----------------------------
# 0) Initialize or load underlying JSON data
# -----------------------------
if "network_data" not in st.session_state:
    st.session_state.network_data = {
        "evidence": [],
        "hypotheses": [],
        "connections": []
    }

def build_graph_from_json(data_json):
    g = nx.DiGraph()
    for ev in data_json["evidence"]:
        g.add_node(ev["id"], group="evidence", description=ev["text"], likelihood="")
    for hy in data_json["hypotheses"]:
        g.add_node(hy["id"], group="hypothesis", description=hy["text"], likelihood=hy.get("likelihood",""))
    for conn in data_json["connections"]:
        g.add_edge(conn["source"], conn["target"])
    return g

# -----------------------------
# 1) Rebuild graph and clean stale session_state
# -----------------------------
g = build_graph_from_json(st.session_state.network_data)

# Ensure these dicts exist
if "priors" not in st.session_state:
    st.session_state.priors = {}        # hypothesis_id → qualitative prior
if "truth_probs" not in st.session_state:
    st.session_state.truth_probs = {}   # evidence_id → qualitative truth‐prob
if "edge_strengths" not in st.session_state:
    st.session_state.edge_strengths = {}  # (src, dst) → float multiplier

# Remove priors for hypotheses no longer in graph
for h_id in list(st.session_state.priors):
    if h_id not in g.nodes or g.nodes[h_id].get("group") != "hypothesis":
        del st.session_state.priors[h_id]

# Remove truth_probs for evidence no longer in graph
for e_id in list(st.session_state.truth_probs):
    if e_id not in g.nodes or g.nodes[e_id].get("group") != "evidence":
        del st.session_state.truth_probs[e_id]

# Remove edge_strengths for edges no longer in graph
for key in list(st.session_state.edge_strengths):
    if key not in g.edges:
        del st.session_state.edge_strengths[key]

# -----------------------------
# 2) Narrative → GPT or Load JSON (overwrites network_data)
# -----------------------------
st.title("🔗 Evidence-Network Builder")
st.header("Narrative → GPT or Load JSON")

col_text, col_file = st.columns(2)
with col_text:
    user_text = st.text_area("📄 Paste or type your evidence narrative here:", height=160)
    run_gpt = st.button("Submit Narrative to GPT")
with col_file:
    uploaded_json = st.file_uploader("📂 …or upload pre-made JSON", type="json")

client = OpenAI()  # reads env vars

PROMPT_TEMPLATE = textwrap.dedent("""
You will receive an analytic text.
Task: extract **evidence** items and **hypotheses** items, then return
ONE JSON object with exactly three arrays:

{
  "evidence":   [ {"id": "E1", "text": "..."} ],
  "hypotheses": [ {"id": "H1", "text": "...", "likelihood": "Likely or Probable"} ],
  "connections": [ {"source": "E1", "target": "H1"},
                   {"source": "H1", "target": "H2"} ]
}

Rules:
• Evidence IDs start with "E"; hypothesis IDs start with "H".
• A connection links an evidence to a hypothesis OR a hypothesis to another hypothesis.
• Include a "likelihood" field only if the source text states one value must be one of:
    Remote Chance, Highly Unlikely, Unlikely, Realistic Possibility,
    Likely or Probable, Highly Likely, Almost Certain.

Return **nothing** except this JSON.

Apply the rules to:
{payload}
""")

if run_gpt and user_text:
    with st.spinner("Sending to GPT and awaiting response …"):
        prompt = PROMPT_TEMPLATE.format(payload=user_text)
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            raw_json = resp.choices[0].message.content.strip()
            st.subheader("Raw JSON from GPT")
            st.code(raw_json, language="json")
            parsed = json.loads(raw_json)
            st.session_state.network_data = parsed
        except Exception as e:
            st.error(f"GPT call / JSON parse failed: {e}")

elif uploaded_json is not None:
    try:
        raw = uploaded_json.getvalue().decode("utf-8")
        parsed = json.loads(raw)
        st.subheader("Raw JSON from file")
        st.code(raw, language="json")

        # --- load core network_data ---
        # if the file has our extended schema, pick off just the three arrays
        st.session_state.network_data = {
            "evidence":   parsed.get("evidence", []),
            "hypotheses": parsed.get("hypotheses", []),
            "connections":parsed.get("connections", [])
        }

        # --- load priors / truth_probs if present ---
        if "priors" in parsed:
            st.session_state.priors = parsed["priors"]
        if "truth_probs" in parsed:
            st.session_state.truth_probs = parsed["truth_probs"]

        # --- load edge_strengths if present ---
        if "edge_strengths" in parsed:
            # keys were saved as "U->V"; convert back to tuple
            es = {}
            for k, v in parsed["edge_strengths"].items():
                if "->" in k:
                    u, v_str = k.split("->", 1)
                    es[(u, v_str)] = v
            st.session_state.edge_strengths = es

        st.success("✅ Loaded network + parameters from JSON")

    except Exception as e:
        st.error(f"Failed to read/parse uploaded JSON: {e}")


# Because network_data may have changed, rebuild g and clean again
g = build_graph_from_json(st.session_state.network_data)
for h_id in list(st.session_state.priors):
    if h_id not in g.nodes or g.nodes[h_id].get("group") != "hypothesis":
        del st.session_state.priors[h_id]
for e_id in list(st.session_state.truth_probs):
    if e_id not in g.nodes or g.nodes[e_id].get("group") != "evidence":
        del st.session_state.truth_probs[e_id]
for key in list(st.session_state.edge_strengths):
    if key not in g.edges:
        del st.session_state.edge_strengths[key]

# -----------------------------
# 3) Build / Edit underlying JSON via UI
# -----------------------------
st.header("Build / Edit Network Data")

# 3A) Add Node
with st.expander("➕ Add Node", expanded=False):
    with st.form("add_node_form"):
        new_id   = st.text_input("Node ID", key="new_node_id")
        new_type = st.selectbox("Node Type", ["evidence", "hypothesis"], key="new_node_type")
        new_txt  = st.text_area("Description/Text", height=100, key="new_node_text")
        add_sub  = st.form_submit_button("Add Node")
    if add_sub:
        if not new_id:
            st.error("Node ID cannot be empty.")
        elif new_id in g.nodes:
            st.error(f"Node '{new_id}' already exists.")
        else:
            entry = {"id": new_id, "text": new_txt}
            if new_type == "hypothesis":
                entry["likelihood"] = ""
                st.session_state.network_data["hypotheses"].append(entry)
            else:
                st.session_state.network_data["evidence"].append(entry)
            st.success(f"Added {new_type} '{new_id}'.")

# **Rebuild graph so downstream expanders see the new node**
g = build_graph_from_json(st.session_state.network_data)
clean_state(g)

# 3B) Delete Node
with st.expander("➖ Delete Node", expanded=False):
    if g.nodes:
        del_node_id = st.selectbox("Choose node to delete", list(g.nodes), key="del_node_select")
        with st.form("delete_node_form"):
            del_sub = st.form_submit_button("Delete Node")
        if del_sub:
            st.session_state.network_data["evidence"] = [
                ev for ev in st.session_state.network_data["evidence"] if ev["id"] != del_node_id
            ]
            st.session_state.network_data["hypotheses"] = [
                hy for hy in st.session_state.network_data["hypotheses"] if hy["id"] != del_node_id
            ]
            st.session_state.network_data["connections"] = [
                c for c in st.session_state.network_data["connections"]
                if c["source"] != del_node_id and c["target"] != del_node_id
            ]
            st.success(f"Deleted node '{del_node_id}' (and its connections).")

# Rebuild again before edge forms
g = build_graph_from_json(st.session_state.network_data)
clean_state(g)

# … after rebuilding g …

# 3C) Add Edge
with st.expander("➕ Add Edge", expanded=False):
    if len(g.nodes) >= 2:
        # Everything in one form
        with st.form("add_edge_form"):
            src = st.selectbox("From", list(g.nodes), key="edge_src")
            dst = st.selectbox("To",   list(g.nodes), key="edge_dst")
            add_e_sub = st.form_submit_button("Add Edge")
        if add_e_sub:
            exists = any(
                c["source"] == src and c["target"] == dst
                for c in st.session_state.network_data["connections"]
            )
            if exists:
                st.error(f"Edge {src} → {dst} already exists.")
            else:
                st.session_state.network_data["connections"].append({
                    "source": src, "target": dst
                })
                st.success(f"Added edge {src} → {dst}.")

    else:
        st.write("At least two nodes required to create an edge.")

# Rebuild so delete‐edge sees up-to-date graph
g = build_graph_from_json(st.session_state.network_data)
clean_state(g)

# 3D) Delete Edge
with st.expander("➖ Delete Edge", expanded=False):
    if g.edges:
        with st.form("delete_edge_form"):
            choice = st.selectbox(
                "Choose edge to delete",
                [f"{u} → {v}" for u, v in g.edges],
                key="del_edge_choice"
            )
            del_e_sub = st.form_submit_button("Delete Edge")
        if del_e_sub:
            u, v = choice.split(" → ")
            st.session_state.network_data["connections"] = [
                c for c in st.session_state.network_data["connections"]
                if not (c["source"] == u and c["target"] == v)
            ]
            st.success(f"Deleted edge {u} → {v}.")
    else:
        st.write("No edges to delete.")

# And one final rebuild
g = build_graph_from_json(st.session_state.network_data)
clean_state(g)

# -----------------------------
# 4) User Inputs: Priors, Evidence Reliability, Edge Strength
# -----------------------------
st.header("User Inputs: Priors, Evidence Reliability, Edge Strength")

SCALE = [
    "Remote Chance",
    "Highly Unlikely",
    "Unlikely",
    "Realistic Possibility",
    "Likely or Probable",
    "Highly Likely",
    "Almost Certain",
]

# 4A) Priors for hypotheses
with st.expander("🧩 Hypothesis priors", expanded=False):
    for hy in st.session_state.network_data["hypotheses"]:
        hid     = hy["id"]
        default = st.session_state.priors.get(hid, "Realistic Possibility")
        st.session_state.priors[hid] = st.selectbox(
            f"{hid} prior probability",
            SCALE,
            index=SCALE.index(default),
            key=f"prior_{hid}"
        )

# 4B) Truth probability for evidence
with st.expander("📄 Evidence reliability", expanded=False):
    for ev in st.session_state.network_data["evidence"]:
        eid     = ev["id"]
        default = st.session_state.truth_probs.get(eid, "Likely or Probable")
        st.session_state.truth_probs[eid] = st.selectbox(
            f"{eid} probability it is true",
            SCALE,
            index=SCALE.index(default),
            key=f"truth_{eid}"
        )

# 4C) Edge odds multipliers
with st.expander("🔗 Edge strength (odds multipliers)", expanded=False):
    for conn in st.session_state.network_data["connections"]:
        u, v    = conn["source"], conn["target"]
        key     = (u, v)
        default = st.session_state.edge_strengths.get(key, 2.0)
        st.session_state.edge_strengths[key] = st.number_input(
            f"{u} ➜ {v}  (× odds)",
            min_value=0.0,
            max_value=100.0,
            step=0.01,
            value=float(default),
            format="%.2f",
            key=f"weight_{u}_{v}"
        )

# Confirmation that state has been updated
st.success("💾 All user inputs stored in session_state (`priors`, `truth_probs`, `edge_strengths`)")

# === New: Save button below all expanders ===
if st.button("💾 Save priors & weights"):
    st.success("Priors & weights saved!")

# After saving, the next rerun will pick up the updated session_state and rebuild everything
# -----------------------------
# 5) Network Tables
# -----------------------------
st.header("Network Tables")

LABEL_TO_PERCENT = {
    "Remote Chance":         5,
    "Highly Unlikely":       15,
    "Unlikely":              30,
    "Realistic Possibility": 45,
    "Likely or Probable":    65,
    "Highly Likely":         85,
    "Almost Certain":        97.5,
}
LABEL_TO_DECIMAL = {
    "Remote Chance":         0.05,
    "Highly Unlikely":       0.15,
    "Unlikely":              0.30,
    "Realistic Possibility": 0.45,
    "Likely or Probable":    0.65,
    "Highly Likely":         0.85,
    "Almost Certain":        0.975,
}

def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))

# Rebuild g to be sure it’s up to date
g = build_graph_from_json(st.session_state.network_data)

# Build Nodes DataFrame
node_rows = []
for node_id in g.nodes:
    data = g.nodes[node_id]
    grp = data["group"]
    desc = data.get("description", "")
    lik_label = data.get("likelihood", "")

    prior_text = ""
    prior_pct = ""
    truth_text = ""
    truth_pct = ""
    calc_prior_pct = ""

    if grp == "hypothesis":
        prior_text = st.session_state.priors.get(node_id, "")
        if prior_text in LABEL_TO_PERCENT:
            prior_pct = LABEL_TO_PERCENT[prior_text]
    elif grp == "evidence":
        truth_text = st.session_state.truth_probs.get(node_id, "")
        if truth_text in LABEL_TO_PERCENT:
            truth_pct = LABEL_TO_PERCENT[truth_text]

    # Compute logistic‐based “Calc Prior (%)” for hypotheses
    if grp == "hypothesis":
        p0 = LABEL_TO_DECIMAL.get(prior_text, None)
        if p0 is not None:
            p0_c = max(min(p0, 0.9999), 0.0001)
            b0 = math.log(p0_c / (1.0 - p0_c))
            z = b0
            for parent in g.predecessors(node_id):
                if g.nodes[parent]["group"] == "evidence":
                    r = st.session_state.edge_strengths.get((parent, node_id), None)
                    if r is None or r <= 0:
                        continue
                    b_i = math.log(r)
                    parent_label = st.session_state.truth_probs.get(parent, "")
                    t_i = LABEL_TO_DECIMAL.get(parent_label, 0.0)
                    z += b_i * t_i
            p_h = sigmoid(z)
            calc_prior_pct = f"≈ {p_h * 100:.1f}%"

    node_rows.append({
        "ID":               node_id,
        "Type":             grp,
        "Description":      desc,
        "Likelihood(node)": lik_label or "",
        "Prior(text)":      prior_text,
        "Prior(%)":         f"≈ {prior_pct}%" if prior_pct != "" else "",
        "Truth-Prob(text)": truth_text,
        "Truth-Prob(%)":    f"≈ {truth_pct}%" if truth_pct != "" else "",
        "Calc Prior(%)":    calc_prior_pct,
    })

nodes_df = pd.DataFrame(node_rows)

# Build Edges DataFrame
edge_rows = []
for conn in st.session_state.network_data["connections"]:
    u = conn["source"]
    v = conn["target"]
    w = st.session_state.edge_strengths.get((u, v), None)
    edge_rows.append({"From": u, "To": v, "Weight": w})

edges_df = pd.DataFrame(edge_rows)

with st.expander("📋 Nodes"):
    st.subheader("Nodes")
    st.dataframe(nodes_df, use_container_width=True)

with st.expander("📈 Edges"):
    st.subheader("Edges")
    st.dataframe(edges_df, use_container_width=True)

# -----------------------------
# 6) Truth tables per connected component
#    (treat ancestor hypotheses like evidence)
# -----------------------------
st.header("Truth Tables by Connected Component")

# Build undirected connectivity
undirected = g.to_undirected()
components = list(nx.connected_components(undirected))

if not components:
    st.write("No nodes in the network.")
else:
    for idx, comp_nodes in enumerate(components, start=1):
        comp_subg = g.subgraph(comp_nodes).copy()

        # Separate evidence & hypotheses in this component
        comp_evidence = [n for n in comp_nodes if g.nodes[n]["group"] == "evidence"]
        comp_hypotheses = [n for n in comp_nodes if g.nodes[n]["group"] == "hypothesis"]

        st.subheader(f"Component {idx}")

        if not comp_hypotheses:
            st.write("No hypotheses here; skipping.")
            continue

        # Compute depth within subgraph
        depth = {}
        for node in nx.topological_sort(comp_subg):
            preds = list(comp_subg.predecessors(node))
            depth[node] = 0 if not preds else max(depth[p] + 1 for p in preds)

        # Choose the deepest hypothesis
        deepest_hyp = max(comp_hypotheses, key=lambda h: depth.get(h, 0))
        st.markdown(f"**Deepest hypothesis:** `{deepest_hyp}` (depth={depth[deepest_hyp]})")

        # All ancestors of that deepest hypothesis
        all_anc = nx.ancestors(comp_subg, deepest_hyp)
        # Filter to those that are evidence or hypothesis
        input_nodes = [n for n in all_anc if comp_subg.nodes[n]["group"] in ("evidence", "hypothesis")]

        if not input_nodes:
            st.write("No ancestor inputs; skipping.")
            continue

        # Precompute evidence‐truth decimals
        evidence_prob = {
            eid: LABEL_TO_DECIMAL.get(st.session_state.truth_probs.get(eid, ""), 0.0)
            for eid in comp_evidence
        }

        # Compute β₀ for deepest hypothesis
        prior_label = st.session_state.priors.get(deepest_hyp, "")
        p0 = LABEL_TO_DECIMAL.get(prior_label, 0.5)
        p0_c = max(min(p0, 0.9999), 0.0001)
        beta0 = math.log(p0_c / (1.0 - p0_c))

        # Compute βᵢ for each direct parent (evidence or hypothesis) of deepest_hyp
        direct_parents = []
        for parent in comp_subg.predecessors(deepest_hyp):
            r = st.session_state.edge_strengths.get((parent, deepest_hyp), 1.0)
            b_i = math.log(r) if r > 0 else 0.0
            direct_parents.append((parent, b_i))

        # Enumerate all 2^m assignments over input_nodes
        combos = list(itertools.product([False, True], repeat=len(input_nodes)))

        rows = []
        for combo in combos:
            # Compute P(deepest_hyp=True | this assignment)
            z = beta0
            for (parent, b_i) in direct_parents:
                if parent in input_nodes:
                    i = input_nodes.index(parent)
                    X_i = 1 if combo[i] else 0
                else:
                    X_i = 0
                z += b_i * X_i
            p_h_true = sigmoid(z)

            # Build row dict
            row = { node: combo[input_nodes.index(node)] for node in input_nodes }
            row[f"P({deepest_hyp}=True) (%)"] = f"{p_h_true * 100:.2f}%"
            rows.append(row)

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

# -----------------------------
# 7) Network Visualisation (with weight‐based edge color & thickness)
# -----------------------------
st.header("Network Visualisation")

try:
    options_dict = {
        "layout": {
            "hierarchical": {
                "enabled": True,
                "levelSeparation": 150,
                "nodeSpacing": 350,
                "treeSpacing": 200,
                "direction": "UD",
                "sortMethod": "directed",
                "blockShifting": False,
                "edgeMinimization": True
            }
        },
        "nodes": {
            "shape": "box",
            "font": {
                "multi": True,
                "align": "left"
            }
        },
        "edges": {
            "smooth": { "enabled": True, "type": "cubicBezier" }
        },
        "physics": {
            "enabled": False
        }
    }

    tmp_net = Network(
        height="600px",
        width="100%",
        directed=True,
        notebook=False,
    )
    tmp_net.set_options(json.dumps(options_dict))

    # add nodes as before
    for n in g.nodes:
        node_data = g.nodes[n]
        desc = node_data.get("description", "")
        wrapped = textwrap.fill(desc, width=50)

        prob = None
        if node_data["group"] == "hypothesis":
            # Use Calc Prior (%)
            prior_label = st.session_state.priors.get(n, "")
            p0 = LABEL_TO_DECIMAL.get(prior_label, None)
            if p0 is not None:
                p0 = max(min(p0, 0.9999), 0.0001)
                b0 = math.log(p0 / (1 - p0))
                z = b0
                for parent in g.predecessors(n):
                    if g.nodes[parent]["group"] == "evidence":
                        r = st.session_state.edge_strengths.get((parent, n), 1.0)
                        b_i = math.log(r) if r > 0 else 0.0
                        t_i = LABEL_TO_DECIMAL.get(st.session_state.truth_probs.get(parent, ""), 0.0)
                        z += b_i * t_i
                prob = sigmoid(z)

        elif node_data["group"] == "evidence":
            truth_label = st.session_state.truth_probs.get(n, "")
            prob = LABEL_TO_DECIMAL.get(truth_label, None)

        color = get_prob_color(prob) if prob is not None else "gray"
        prob_str = f"{prob * 100:.1f}%" if prob is not None else "?"

        label = f"{n}\n{wrapped}\n({prob_str})"

        tmp_net.add_node(
            n,
            label=label,
            title=desc,
            shape="box",
            font={"multi": True, "align": "left"},
            color=color,
        )


    # add edges with dynamic color & width
    for u, v in g.edges:
        w = st.session_state.edge_strengths.get((u, v), 1.0)
        if 0 < w <= 1:
            color = "red"
            width = 1 + (1 - w) * 10
        else:
            color = "green"
            width = 1 + (w - 1) 

        tmp_net.add_edge(
            u,
            v,
            color=color,
            width=width,
            arrows="to"
        )

    # render HTML
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        tmp_net.save_graph(tmp_file.name)
        html = open(tmp_file.name, "r", encoding="utf-8").read()

    if html:
        st.components.v1.html(html, height=700, scrolling=True)
    else:
        st.warning("⚠️ Visualization HTML was empty.")
    os.unlink(tmp_file.name)

except Exception as e:
    st.error(f"Could not generate network visualization: {e}")

# -----------------------------
# 8) Save / Export Network Data
# -----------------------------
st.header("Export Network Data")

# First, merge in the current priors, truth‐probs, and edge strengths
export_data = {
    **st.session_state.network_data,          # evidence, hypotheses, connections
    "priors": st.session_state.priors,        # hypothesis_id → qualitative prior
    "truth_probs": st.session_state.truth_probs,  # evidence_id → qualitative truth‐prob
    # convert tuple keys to strings so JSON can encode them
    "edge_strengths": {
        f"{u}->{v}": w
        for (u, v), w in st.session_state.edge_strengths.items()
    }
}

# Serialize to pretty JSON
json_str = json.dumps(export_data, indent=2)

# Overwrite a temp file each run (optional)
tmp_path = os.path.join(tempfile.gettempdir(), "network_data.json")
with open(tmp_path, "w", encoding="utf-8") as f:
    f.write(json_str)

# Provide a download button
st.download_button(
    label="Download current network JSON",
    data=json_str,
    file_name="network_data.json",
    mime="application/json"
)

st.caption(f"🔄 Temp file overwritten on each run: `{tmp_path}`")


# -----------------------------
# Footer
# -----------------------------
st.caption("© 2025 Evidence-Network UI – Streamlit & PyVis demo")
