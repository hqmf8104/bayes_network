const axios = require('axios');

const api = axios.create({ baseURL: 'http://localhost:4000' });

describe('Nodes & Edges API', () => {
  let node;
  let edge;

  beforeAll(async () => {
    // ensure server is running
    // You must start the server manually before running tests
  });

  it('creates, reads, updates, and deletes a node', async () => {
    // Create
    let res = await api.post('/nodes', { description: 'T', prior_probability: 0.2 });
    expect(res.status).toBe(201);
    node = res.data;

    // Read
    res = await api.get('/nodes');
    expect(res.data.find(n => n.id === node.id)).toBeDefined();

    // Update
    res = await api.patch(`/nodes/${node.id}`, { description: 'T2' });
    expect(res.data.description).toBe('T2');

    // Delete
    res = await api.delete(`/nodes/${node.id}`);
    expect(res.status).toBe(204);
  });

  it('creates, reads, updates, and deletes an edge', async () => {
    // First create two nodes
    const a = (await api.post('/nodes', { description: 'A', prior_probability: 0.1 })).data;
    const b = (await api.post('/nodes', { description: 'B', prior_probability: 0.3 })).data;

    // Create edge
    let res = await api.post('/edges', { source: a.id, target: b.id, weight: 0.5 });
    expect(res.status).toBe(201);
    edge = res.data;

    // Read
    res = await api.get('/edges');
    expect(res.data.find(e => e.id === edge.id)).toBeDefined();

    // Update
    res = await api.patch(`/edges/${edge.id}`, { weight: 0.8 });
    expect(res.data.weight).toBe(0.8);

    // Delete
    res = await api.delete(`/edges/${edge.id}`);
    expect(res.status).toBe(204);

    // Clean up nodes
    await api.delete(`/nodes/${a.id}`);
    await api.delete(`/nodes/${b.id}`);
  });
});
