// client/src/__mocks__/react-cytoscapejs.js
const React = require('react');

// Render just a plain div with children—ignore any Cytoscape-specific props
module.exports = function CytoscapeComponent({ children }) {
  return React.createElement('div', { 'data-testid': 'cytoscape-mock' }, children);
};
