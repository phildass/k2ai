export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  source?: string;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  suggestions?: string[];
  answer_source?: string;
  metadata?: {
    language?: string;
    model?: string;
    timestamp?: string;
    source?: string;
  };
}

export interface Service {
  id: string;
  name: string;
  description: string;
  key_features: string[];
  use_cases: string[];
}

export interface LeadFormData {
  name: string;
  email: string;
  phone?: string;
  company?: string;
  service_interest: string;
  message?: string;
}

export interface FeedbackData {
  conversation_id: string;
  rating: number;
  comment?: string;
}
