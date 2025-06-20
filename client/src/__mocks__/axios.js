// client/src/__mocks__/axios.js

// A very minimal axios mock that just lets your code call
// axios.create().get().post() etc. without throwing.
const mockResponse = { data: [] };

const axiosInstance = {
  get: jest.fn(() => Promise.resolve(mockResponse)),
  post: jest.fn(() => Promise.resolve(mockResponse)),
  patch: jest.fn(() => Promise.resolve(mockResponse)),
  delete: jest.fn(() => Promise.resolve(mockResponse)),
};

const axios = {
  create: jest.fn(() => axiosInstance),
  // also allow `import axios from 'axios'`
  ...axiosInstance,
};

module.exports = axios;
