// client/src/App.js
import React, { useState, useEffect, useRef } from 'react';
import {
  fetchNodes,
  fetchEdges,
  createNode,
  updateNode,
  deleteNode,
  createEdge,
  updateEdge,
  deleteEdge,
  saveNetwork,
  listNetworks,
  loadNetwork,
} from './services/api';
import GraphEditor from './components/GraphEditor';
import SidePanel from './components/SidePanel';

function App() {
  const fileInputRef = useRef(null);

  const handleExportJSON = () => {
    const json = JSON.stringify(elements, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'network.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImportJSON = event => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {
      try {
        const imported = JSON.parse(e.target.result);
        setElements(imported);
      } catch {
        alert('Invalid JSON file');
      }
    };
    reader.readAsText(file);
    // Clear input
    event.target.value = '';
  };
  const [elements, setElements] = useState([]);
  const [selectedElement, setSelectedElement] = useState(null);
  const [networks, setNetworks] = useState([]);
  const [networkName, setNetworkName] = useState('');

  // Load nodes & edges on mount
  useEffect(() => {
    Promise.all([fetchNodes(), fetchEdges(), listNetworks()])
      .then(([nRes, eRes, netsRes]) => {
        const nodeEls = nRes.data.map(n => ({
          data: {
            ...n,
            label: `${n.description}\n${(n.prior_probability * 100).toFixed(1)}%`,
          },
        }));
        const edgeEls = eRes.data.map(e => ({ data: e }));
        setElements([...nodeEls, ...edgeEls]);
        setNetworks(netsRes.data);
      })
      .catch(err => console.error(err));
  }, []);

  // Node handlers
  const handleUpdateNode = (id, updates) =>
    updateNode(id, updates).then(res => {
      const n = res.data;
      const labeled = {
        ...n,
        label: `${n.description}\n${(n.prior_probability * 100).toFixed(1)}%`,
      };
      setElements(e => e.map(el => (el.data.id === id ? { data: labeled } : el)));
      if (selectedElement?.data.id === id) {
        setSelectedElement({ data: labeled });
      }
    });

  const handleDeleteNode = id =>
    deleteNode(id).then(() => {
      setElements(e =>
        e.filter(el => !(el.data.id === id || el.data.source === id || el.data.target === id))
      );
      if (selectedElement?.data.id === id) setSelectedElement(null);
    });

  // Edge handlers
  const handleAddEdge = ({ source, target, weight }) =>
    createEdge({ source, target, weight }).then(res =>
      setElements(e => [...e, { data: res.data }])
    );

  const handleUpdateEdge = (id, updates) =>
    updateEdge(id, updates).then(res => {
      setElements(e => e.map(el => (el.data.id === id ? { data: res.data } : el)));
      if (selectedElement?.data.id === id) setSelectedElement({ data: res.data });
    });

  const handleDeleteEdge = id =>
    deleteEdge(id).then(() => {
      setElements(e => e.filter(el => el.data.id !== id));
      if (selectedElement?.data.id === id) setSelectedElement(null);
    });

  // Add node
  const promptAndAddNode = () => {
    const description = prompt('Node description:');
    if (!description) return;
    createNode({ description, prior_probability: 0 }).then(res => {
      const newNode = res.data;
      setElements(e => [...e, { data: { ...newNode, label: `${newNode.description}\n0.0%` } }]);
      setSelectedElement({ data: { ...newNode, label: `${newNode.description}\n0.0%` } });
    });
  };

  // Save current network
  const handleSaveNetwork = () => {
    const name = prompt('Network name:');
    if (!name) return;
    const nodes = elements.filter(el => el.data.source === undefined).map(el => el.data);
    const edges = elements.filter(el => el.data.source !== undefined).map(el => el.data);
    saveNetwork({ name, nodes, edges }).then(res => {
      setNetworks(nets => [...nets, res.data]);
      alert('Network saved!');
    });
  };

  // Load selected network
  const handleLoadNetwork = () => {
    if (!networkName) return;
    loadNetwork(networkName).then(res => {
      const { nodes, edges } = res.data;
      const nodeEls = nodes.map(n => ({ data: { ...n, label: `${n.description}\n${(n.prior_probability * 100).toFixed(1)}%` } }));
      const edgeEls = edges.map(e => ({ data: e }));
      setElements([...nodeEls, ...edgeEls]);
      setSelectedElement(null);
    });
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      {/* Left pane: toolbar + graph */}
      <div style={{ flex: 1, padding: 20, display: 'flex', flexDirection: 'column' }}>
        <div style={{ marginBottom: 10 }}>
  <button onClick={promptAndAddNode} style={{ marginRight: 8 }}>
    + Add EH
  </button>
  <button onClick={handleSaveNetwork} style={{ marginRight: 8 }}>
    💾 Save Network
  </button>
  <select
    value={networkName}
    onChange={e => setNetworkName(e.target.value)}
    style={{ marginRight: 4 }}
  >
    <option value="">Load…</option>
    {networks.map(net => (
      <option key={net.id} value={net.id}>
        {net.name}
      </option>
    ))}
  </select>
  <button onClick={handleLoadNetwork} disabled={!networkName} style={{ marginRight: 8 }}>
    ▶️ Load
  </button>
  {/* Export/Import JSON */}
  <button onClick={handleExportJSON} style={{ marginRight: 8 }}>
    📤 Export JSON
  </button>
  <button onClick={() => fileInputRef.current.click()}>📥 Import JSON</button>
  {/* Hidden file input */}
  <input
    type="file"
    accept="application/json"
    style={{ display: 'none' }}
    ref={fileInputRef}
    onChange={handleImportJSON}
  />
</div>
        <div style={{ flex: 1, border: '1px solid #ccc' }}>
          <GraphEditor
            elements={elements}
            onSelectNode={nodeData => setSelectedElement({ data: nodeData })}
            onSelectEdge={edgeData => setSelectedElement({ data: edgeData })}
            onDeleteNode={handleDeleteNode}
            onAddEdge={handleAddEdge}
            onUpdateEdge={handleUpdateEdge}
            onDeleteEdge={handleDeleteEdge}
          />
        </div>
      </div>

      {/* Right pane: side panel */}
      <SidePanel
        element={selectedElement?.data}
        onUpdate={updates => {
          if (!selectedElement) return;
          const { id, source } = selectedElement.data;
          if (source !== undefined) {
            handleUpdateEdge(id, updates);
          } else {
            handleUpdateNode(id, updates);
          }
        }}
        onDelete={() => {
          if (!selectedElement) return;
          const { id, source } = selectedElement.data;
          if (source !== undefined) {
            handleDeleteEdge(id);
          } else {
            handleDeleteNode(id);
          }
        }}
      />
    </div>
  );
}

export default App;
