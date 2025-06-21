// client/src/components/SidePanel.js
import React, { useState, useEffect } from 'react';

// Dropdown options for descriptive priors
const PRIOR_OPTIONS = [
{ label: 'Evidence Refuted', value: 0.05 },
  { label: '≈5%: Remote Chance', value: 0.05 },
  { label: '≈10% - ≈20%: Highly Unlikely', value: 0.15 },
  { label: '≈25% - ≈35%: Unlikely', value: 0.30 },
  { label: '≈40% - <50%: Realistic Possibility', value: 0.45 },
  { label: '≈55% - ≈75%: Likely or Probable', value: 0.65 },
  { label: '≈80% - ≈90%: Highly Likely', value: 0.85 },
  { label: '≈95% - <100%: Almost Certain', value: 0.975 },
  { label: 'Evidence Confirmed', value: 1.0 },
];

export default function SidePanel({ element, onUpdate, onDelete }) {
  const [description, setDescription] = useState('');
  const [prior, setPrior] = useState('');
  const [weight, setWeight] = useState('');

  useEffect(() => {
    if (!element) {
      setDescription('');
      setPrior('');
      setWeight('');
      return;
    }
    const { description, prior_probability, weight } = element;
    setDescription(description || '');
    setPrior(prior_probability !== undefined ? prior_probability : '');
    setWeight(weight !== undefined ? weight : '');
  }, [element]);

  if (!element) {
    return (
      <div style={{ width: 250, padding: 20, borderLeft: '1px solid #ccc' }}>
        <p>Select a node or edge to view/edit parameters.</p>
      </div>
    );
  }

  const isEdge = element.source !== undefined;

  const handleSave = async () => {
  try {
    if (isEdge) {
      const w = parseFloat(weight);
      if (isNaN(w)) throw new Error('Weight must be a number.');
      await onUpdate({ weight: w });
    } else {
      const p = parseFloat(prior);
      if (isNaN(p)) throw new Error('Please select a valid prior.');
      await onUpdate({ description, prior_probability: p });
    }
    alert('Saved!');
  } catch (err) {
    console.error(err);
    alert('Save failed: ' + (err.response?.data?.message || err.message));
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
          <select
            value={prior}
            onChange={e => setPrior(e.target.value)}
            style={{ width: '100%', marginBottom: 10, padding: '4px' }}
          >
            <option value="">-- Select Prior --</option>
            {PRIOR_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </>
      )}
      <button onClick={handleSave} style={{ marginRight: 10 }}>Save</button>
      <button onClick={onDelete}>Delete</button>
    </div>
  );
}
