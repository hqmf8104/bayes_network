// client/src/App.js
import React, { useState, useEffect } from 'react';
import {
  fetchNodes,
  fetchEdges,
  createNode,
  updateNode,
  deleteNode,
  createEdge,
  updateEdge,
  deleteEdge
} from './services/api';
import GraphEditor from './components/GraphEditor';
import SidePanel from './components/SidePanel';

function App() {
  const [elements, setElements] = useState([]);
  const [selectedElement, setSelectedElement] = useState(null);

  // Load nodes & edges on mount
  useEffect(() => {
    Promise.all([fetchNodes(), fetchEdges()])
      .then(([nRes, eRes]) => {
        const nodeEls = nRes.data.map(n => ({
          data: {
            ...n,
           label: `${n.description}\n${(n.prior_probability*100).toFixed(1)}%` 
          }
        }));
        const edgeEls = eRes.data.map(e => ({ data: e }));
        setElements([...nodeEls, ...edgeEls]);
      })
      .catch(err => console.error(err));
  }, []);

  // Node handlers

  const handleUpdateNode = (id, updates) =>
    updateNode(id, updates).then(res => {
      const n = res.data;
      const labeled = {
        ...n,
        label: `${n.description}\n${(n.prior_probability * 100).toFixed(1)}%`
      };
      setElements(e =>
        e.map(el => el.data.id === id ? { data: labeled } : el)
      );
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

  // Edge handlers (keep drag-to-add)
  const handleAddEdge = ({ source, target, weight }) =>
    createEdge({ source, target, weight }).then(res =>
      setElements(e => [...e, { data: res.data }])
    );

  const handleUpdateEdge = (id, updates) =>
    updateEdge(id, updates).then(res => {
      setElements(e => e.map(el => el.data.id === id ? { data: res.data } : el));
      if (selectedElement?.data.id === id) setSelectedElement({ data: res.data });
    });

  const handleDeleteEdge = id =>
    deleteEdge(id).then(() => {
      setElements(e => e.filter(el => el.data.id !== id));
      if (selectedElement?.data.id === id) setSelectedElement(null);
    });

  // Prompt only for description, create node with placeholder prior of 0,
  // then open its SidePanel so you can pick the real prior from the dropdown.
  const promptAndAddNode = () => {
    const description = prompt('Node description:');
    if (!description) return;

    // Create node with a temporary 0% prior
    createNode({ description, prior_probability: 0 }).then(res => {
      const newNode = res.data;
      setElements(e => [...e, { data: newNode }]);
      // Immediately select it so the dropdown appears
      setSelectedElement({ data: newNode });
    });
  };


  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      {/* Left pane: toolbar + graph */}
      <div style={{ flex: 1, padding: 20, display: 'flex', flexDirection: 'column' }}>
        <button
          onClick={promptAndAddNode}
          style={{ padding: '8px 12px', marginBottom: 10, fontSize: 16 }}
        >
          + Add EH
        </button>
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
