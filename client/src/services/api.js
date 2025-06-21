// client/src/services/api.js
import axios from 'axios';

// 1) Create an Axios instance pointing at your Express server
const api = axios.create({
  baseURL: 'http://localhost:4000',      // <-- match your server URL/port
  headers: { 'Content-Type': 'application/json' },
});

// 2) Export one function per REST endpoint:

// --- Nodes ---
export function fetchNodes() {
  // GET /nodes → returns Promise resolving to { data: [ ...nodes ] }
  return api.get('/nodes');
}

export function createNode({ description, prior_probability }) {
  // POST /nodes with a JSON body → new node returned in data
  return api.post('/nodes', { description, prior_probability });
}

export function updateNode(id, updates) {
  // PATCH /nodes/:id → updates = { description?, prior_probability? }
  return api.patch(`/nodes/${id}`, updates);
}

export function deleteNode(id) {
  // DELETE /nodes/:id
  return api.delete(`/nodes/${id}`);
}

// --- Edges ---
export function fetchEdges() {
  return api.get('/edges');
}

export function createEdge({ source, target, weight }) {
  return api.post('/edges', { source, target, weight });
}

export function updateEdge(id, updates) {
  // updates = { weight }
  return api.patch(`/edges/${id}`, updates);
}

export function deleteEdge(id) {
  return api.delete(`/edges/${id}`);
}

export function saveNetwork({ name, nodes, edges }) {
  return axios.post('/api/networks', { name, nodes, edges });
}

export function listNetworks() {
  return axios.get('/api/networks');
}

export function loadNetwork(id) {
  return axios.get(`/api/networks/${id}`);
}

export function updateNetwork(id, { name, nodes, edges }) {
  return axios.put(`/api/networks/${id}`, { name, nodes, edges });
}
