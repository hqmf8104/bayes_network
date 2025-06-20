// client/src/components/SidePanel.js
import React, { useState, useEffect } from 'react';

// SidePanel now handles both nodes and edges
// Pass in `element` which is the .data object from Cytoscape for a node or edge
// For nodes, element has { id, description, prior_probability }
// For edges, element has { id, source, target, weight }
export default function SidePanel({ element, onUpdate, onDelete }) {
  const [description, setDescription] = useState('');
  const [prior, setPrior] = useState('');
  const [weight, setWeight] = useState('');

  // Sync local form state when selected element changes
  useEffect(() => {
    if (!element) {
      setDescription('');
      setPrior('');
      setWeight('');
      return;
    }
    // Destructure common fields
    const { description, prior_probability, weight } = element;
    setDescription(description || '');
    setPrior(prior_probability !== undefined ? prior_probability : '');
    setWeight(weight !== undefined ? weight : '');
  }, [element]);

  // If nothing selected
  if (!element) {
    return (
      <div style={{ width: 250, padding: 20, borderLeft: '1px solid #ccc' }}>
        <p>Select a node or edge to view/edit parameters.</p>
      </div>
    );
  }

  // Determine whether the element is an edge (has source) or a node
  const isEdge = element.source !== undefined;

  // Handler to save changes
  const handleSave = () => {
    if (isEdge) {
      const w = parseFloat(weight);
      if (isNaN(w)) {
        alert('Weight must be a number.');
        return;
      }
      onUpdate({ weight: w });
    } else {
      const p = parseFloat(prior);
      if (isNaN(p) || p < 0 || p > 1) {
        alert('Prior must be between 0 and 1.');
        return;
      }
      onUpdate({ description, prior_probability: p });
    }
  };

  return (
    <div style={{ width: 250, padding: 20, borderLeft: '1px solid #ccc' }}>
      <h2>{isEdge ? 'Edge Parameters' : 'Node Parameters'}</h2>
      {isEdge ? (
        <>
          <p><strong>Source:</strong> {element.source}</p>
          <p><strong>Target:</strong> {element.target}</p>
          <label>Weight:</label>
          <input
            type="number"
            step="0.01"
            value={weight}
            onChange={e => setWeight(e.target.value)}
            style={{ width: '100%', marginBottom: 10 }}
          />
        </>
      ) : (
        <>
          <label>Description:</label>
          <textarea
            value={description}
            onChange={e => setDescription(e.target.value)}
            style={{ width: '100%', marginBottom: 10 }}
          />
          <label>Prior probability:</label>
          <input
            type="number"
            step="0.01"
            min="0"
            max="1"
            value={prior}
            onChange={e => setPrior(e.target.value)}
            style={{ width: '100%', marginBottom: 10 }}
          />
        </>
      )}
      <button onClick={handleSave} style={{ marginRight: 10 }}>Save</button>
      <button onClick={onDelete}>Delete</button>
    </div>
  );
}
