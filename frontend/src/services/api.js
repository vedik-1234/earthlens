const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  getDatasets: async () => {
    const response = await fetch(`${API_BASE}/api/datasets`);
    return response.json();
  },
  analyze: async (payload) => {
    const response = await fetch(`${API_BASE}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  detectTrends: async (payload) => {
    const response = await fetch(`${API_BASE}/api/trend-detect`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  compare: async (payload) => {
    const response = await fetch(`${API_BASE}/api/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
  explain: async (payload) => {
    const response = await fetch(`${API_BASE}/api/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return response.json();
  },
};
