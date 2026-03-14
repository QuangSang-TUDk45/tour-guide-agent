import axios from 'axios';

const api = axios.create({
  // Use a relative base URL so that the frontend can be served through ngrok
  // and proxy API calls to the backend via Vite dev server.
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('authToken');
    }
    return Promise.reject(error);
  }
);

export default api;

// API endpoints
export const chatAPI = {
  sendMessage: (message: string, conversationId?: string) =>
    api.post('/api/chat', { user_prompt: message }),
  
  getConversationHistory: (conversationId: string) =>
    api.get(`/api/chat/history/${conversationId}`),
};


export const tripAPI = {
  getSuggestions: (params: any) =>
    api.post('/api/suggestions', params),
  
  saveItinerary: (itinerary: any) =>
    api.post('/api/itinerary', itinerary),
  
  getItinerary: (id: string) =>
    api.get(`/api/itinerary/${id}`),
};
