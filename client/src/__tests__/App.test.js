import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders the EH Network Editor heading and Cytoscape mock', () => {
  render(<App />);

  // Heading
  expect(screen.getByText(/EH Network Editor/i)).toBeInTheDocument();

  // CytoscapeComponent mock
  expect(screen.getByTestId('cytoscape-mock')).toBeInTheDocument();
});
