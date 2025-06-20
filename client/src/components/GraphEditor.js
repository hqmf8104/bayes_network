// client/src/components/GraphEditor.js
import React, { useRef, useEffect } from 'react';
import cytoscape from 'cytoscape';
import edgehandles from 'cytoscape-edgehandles';
import CytoscapeComponent from 'react-cytoscapejs';

// Register the edge-drawing extension
cytoscape.use(edgehandles);

export default function GraphEditor({
  elements,
  onSelectNode,
  onSelectEdge,
  onDeleteNode,
  onAddEdge,
  onUpdateEdge,
  onDeleteEdge
}) {
  const cyRef = useRef(null);
  const [shiftSource, setShiftSource] = React.useState(null);

  const onCyReady = cy => {
    cyRef.current = cy;
    cy.edgehandles();

    // Shift-click workflow
    cy.on('tap', 'node', evt => {
      const nodeData = evt.target.data();
      const event = evt.originalEvent;
      if (event.shiftKey) {
        if (!shiftSource) {
          setShiftSource(nodeData.id);
        } else if (shiftSource !== nodeData.id) {
          const sourceId = shiftSource;
          const targetId = nodeData.id;
          const w = prompt(`Edge weight from ${sourceId} → ${targetId}?`);
          if (w !== null) onAddEdge({ source: sourceId, target: targetId, weight: parseFloat(w) });
          setShiftSource(null);
        }
      } else {
        onSelectNode && onSelectNode(nodeData);
      }
    });

    // Node right-click → delete
    cy.on('cxttap', 'node', evt => {
      if (window.confirm('Delete this node?')) onDeleteNode(evt.target.id());
    });

    // Edge complete (drag) → add edge
    cy.on('ehcomplete', event => {
      const { source, target, edge } = event;
      const w = prompt('Edge weight?');
      if (w !== null) onAddEdge({ source: source.id(), target: target.id(), weight: parseFloat(w) });
      else cy.remove(edge);
    });

    // Edge click → select and update weight
    cy.on('tap', 'edge', evt => {
      const data = evt.target.data();
      onSelectEdge && onSelectEdge(data);
      const w = prompt('New weight?', data.weight);
      if (w !== null) onUpdateEdge(evt.target.id(), { weight: parseFloat(w) });
    });

    // Edge right-click → delete
    cy.on('cxttap', 'edge', evt => {
      if (window.confirm('Delete this edge?')) onDeleteEdge(evt.target.id());
    });
  };

  // Highlight nodes selected for shift-edge
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.nodes().forEach(node => {
      if (node.id() === shiftSource) node.addClass('selected-shift');
      else node.removeClass('selected-shift');
    });
  }, [shiftSource]);

  return (
    <CytoscapeComponent
      elements={elements}
      style={{ width: '100%', height: '100%' }}
      layout={{ name: 'cose' }}
      cy={onCyReady}
      stylesheet={[
        {
          selector: 'node.selected',
          style: { 'border-color': '#f00', 'border-width': 3 }
        },
        {
          selector: 'node.selected-shift',
          style: { 'border-color': '#00f', 'border-width': 3 }
        },
        {
          selector: 'edge',
          style: {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'target-arrow-color': '#999',
            'line-color': '#999'
          }
        }
      ]}
    />
  );
}
