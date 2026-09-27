const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const buildHeaders = (token = '', includeJson = true) => {
  const headers = {};
  if (includeJson) headers['Content-Type'] = 'application/json';
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
};

export const api = {
  signup: async (payload, token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/auth/signup`, {
        method: 'POST',
        headers: buildHeaders(token),
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error signing up:', err);
      return { status: 'error', message: 'Unable to create account.' };
    }
  },

  signin: async (payload, token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/auth/signin`, {
        method: 'POST',
        headers: buildHeaders(token),
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error signing in:', err);
      return { status: 'error', message: 'Unable to sign in.' };
    }
  },

  getCurrentUser: async (token) => {
    try {
      const response = await fetch(`${API_BASE}/api/auth/me`, {
        headers: buildHeaders(token, false),
      });
      return response.json();
    } catch (err) {
      console.error('Error fetching user:', err);
      return { status: 'error', message: 'Unable to load user profile.' };
    }
  },

  getDatasets: async (token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/datasets`, {
        headers: buildHeaders(token, false),
      });
      return response.json();
    } catch (err) {
      console.error('Error fetching datasets:', err);
      return { datasets: [] };
    }
  },

  getRegions: async (token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/regions`, {
        headers: buildHeaders(token, false),
      });
      return response.json();
    } catch (err) {
      console.error('Error fetching regions:', err);
      return { regions: {} };
    }
  },

  analyze: async (payload, token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        headers: buildHeaders(token),
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error analyzing:', err);
      return { status: 'error', message: 'Analysis failed' };
    }
  },

  detectTrends: async (payload, token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/trend-detect`, {
        method: 'POST',
        headers: buildHeaders(token),
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error detecting trends:', err);
      return { status: 'error', results: [] };
    }
  },

  compare: async (payload, token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/compare`, {
        method: 'POST',
        headers: buildHeaders(token),
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error comparing:', err);
      return { status: 'error', message: 'Comparison failed' };
    }
  },

  explain: async (payload, token = '') => {
    try {
      const response = await fetch(`${API_BASE}/api/explain`, {
        method: 'POST',
        headers: buildHeaders(token),
        body: JSON.stringify(payload),
      });
      return response.json();
    } catch (err) {
      console.error('Error generating explanation:', err);
      return { status: 'error', summary: 'Explanation unavailable' };
    }
  },
};
