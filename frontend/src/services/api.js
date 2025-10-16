import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const generateDocumentation = async (repoUrl) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/v1/generate`, {
      repo_url: repoUrl,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error
      throw new Error(error.response.data.detail || 'Server error');
    } else if (error.request) {
      // Request made but no response
      throw new Error('No response from server. Is the backend running?');
    } else {
      // Something else happened
      throw new Error(error.message);
    }
  }
};

export const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/v1/health`);
    return response.data;
  } catch (error) {
    throw new Error('Backend is not reachable');
  }
};
