const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  getDatasets: async () => {
    try {
      const response = await fetch(`${API_BASE}/api/datasets`);
      return response.json();
    } catch (err) {
      console.error('Error fetching datasets:', err);
      return { datasets: [] };
    }
  },

  getRegions: async () => {
    try {
      const response = await fetch(`${API_BASE}/api/regions`);
      return response.json();
    } catch (err) {
      console.error('Error fetching regions:', err);
      return { regions: {} };
    }
  },

  analyze: async (payload) => {
    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error analyzing:', err);
      return { status: 'error', message: 'Analysis failed' };
    }
  },

  detectTrends: async (payload) => {
    try {
      const response = await fetch(`${API_BASE}/api/trend-detect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error detecting trends:', err);
      return { status: 'error', results: [] };
    }
  },

  compare: async (payload) => {
    try {
      const response = await fetch(`${API_BASE}/api/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error comparing:', err);
      return { status: 'error', message: 'Comparison failed' };
    }
  },

  explain: async (payload) => {
    try {
      const response = await fetch(`${API_BASE}/api/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error generating explanation:', err);
      return { status: 'error', summary: 'Explanation unavailable' };
    }
  },
};
