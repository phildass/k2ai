import axios from 'axios';
import type { ChatResponse, Service, LeadFormData, FeedbackData } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatApi = {
  sendMessage: async (
    message: string,
    conversationId?: string,
    language: string = 'en',
    context?: any
  ): Promise<ChatResponse> => {
    const response = await api.post('/api/chat/message', {
      message,
      conversation_id: conversationId,
      language,
      context,
    });
    return response.data;
  },

  getConversationHistory: async (conversationId: string) => {
    const response = await api.get(`/api/chat/conversation/${conversationId}`);
    return response.data;
  },
};

export const servicesApi = {
  getAll: async (): Promise<Service[]> => {
    const response = await api.get('/api/services/');
    return response.data;
  },

  getById: async (serviceId: string): Promise<Service> => {
    const response = await api.get(`/api/services/${serviceId}`);
    return response.data;
  },
};

export const feedbackApi = {
  submitFeedback: async (feedback: FeedbackData) => {
    const response = await api.post('/api/feedback/submit', feedback);
    return response.data;
  },

  captureLead: async (lead: LeadFormData) => {
    const response = await api.post('/api/feedback/lead', lead);
    return response.data;
  },
};

export default api;
