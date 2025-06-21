// server/index.js
const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(cors());
app.use(express.json());  // built-in JSON parser

let nodes = [];
let edges = [];
let networks = {};

// --- Node routes ---
app.get('/nodes', (req, res) => res.json(nodes));

app.post('/nodes', (req, res) => {
  const { description, prior_probability } = req.body;
  const node = { id: uuidv4(), description, prior_probability };
  nodes.push(node);
  res.status(201).json(node);
});

app.patch('/nodes/:id', (req, res) => {
  const node = nodes.find(n => n.id === req.params.id);
  if (!node) return res.sendStatus(404);
  // merge updates, default to empty object
  Object.assign(node, req.body || {});
  res.json(node);
});

app.delete('/nodes/:id', (req, res) => {
  nodes = nodes.filter(n => n.id !== req.params.id);
  edges = edges.filter(e => e.source !== req.params.id && e.target !== req.params.id);
  res.sendStatus(204);
});

// --- Edge routes ---
app.get('/edges', (req, res) => res.json(edges));

app.post('/edges', (req, res) => {
  const { source, target, weight } = req.body;
  const edge = { id: uuidv4(), source, target, weight };
  edges.push(edge);
  res.status(201).json(edge);
});

app.patch('/edges/:id', (req, res) => {
  const edge = edges.find(e => e.id === req.params.id);
  if (!edge) return res.sendStatus(404);
  Object.assign(edge, req.body || {});
  res.json(edge);
});

app.delete('/edges/:id', (req, res) => {
  edges = edges.filter(e => e.id !== req.params.id);
  res.sendStatus(204);
});

// --- Network routes ---
app.post('/api/networks', (req, res) => {
  const { name, nodes: netNodes, edges: netEdges } = req.body;
  const id = uuidv4();
  networks[id] = { id, name, nodes: netNodes, edges: netEdges };
  res.status(201).json(networks[id]);
});

app.get('/api/networks', (req, res) => res.json(Object.values(networks)));

app.get('/api/networks/:id', (req, res) => {
  const net = networks[req.params.id];
  if (!net) return res.sendStatus(404);
  res.json(net);
});

app.put('/api/networks/:id', (req, res) => {
  const { name, nodes: netNodes, edges: netEdges } = req.body;
  if (!networks[req.params.id]) return res.sendStatus(404);
  networks[req.params.id] = { id: req.params.id, name, nodes: netNodes, edges: netEdges };
  res.json(networks[req.params.id]);
});

// Global error handler (optional)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: err.message || 'Internal Server Error' });
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`API listening on port ${PORT}`));
