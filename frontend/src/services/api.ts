/**
 * API service for interacting with the Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Type definitions for API requests and responses
 */
export interface Influencer {
  id: number;
  name: string;
  username?: string;
  profileImage?: string;
  followers: number | string;
  hearts?: number;
  videos?: number;
  engagementRate?: string;
  niche?: string;
  platform: string;
  location?: string;
  email?: string;
  leadStage?: string;
  contractVideo?: string;
  createdAt?: string;
  contractShares?: number;
  contractPlays?: number;
  contractComments?: number;
}

export interface ClientBrief {
  id: number;
  name: string;
  type: string;
  clientName: string;
  productService: string;
  targetAudience: string;
  campaignGoal: string;
  influencerType: string;
  date: string;
}

export interface ContactRequest {
  influencerId: number;
  message: string;
}

export interface SearchRequest {
  query: string;
  limit?: number;
}

/**
 * Generic function to make API requests
 */
async function apiRequest<T>(
  endpoint: string,
  method = 'GET',
  data?: any
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json() as T;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * API functions for influencers
 */
export const influencersApi = {
  getAll: (): Promise<Influencer[]> => {
    return apiRequest<Influencer[]>('/influencers');
  },
  
  search: (searchParams: SearchRequest): Promise<Influencer[]> => {
    return apiRequest<Influencer[]>('/influencers/search', 'POST', searchParams);
  },
  
  contact: (contactRequest: ContactRequest): Promise<{success: boolean, message: string}> => {
    return apiRequest<{success: boolean, message: string}>('/contact', 'POST', contactRequest);
  },
};

/**
 * API functions for client briefs
 */
export const briefsApi = {
  create: (brief: Partial<ClientBrief>): Promise<ClientBrief> => {
    return apiRequest<ClientBrief>('/briefs', 'POST', brief);
  },
};

/**
 * Health check function
 */
export const checkApiHealth = (): Promise<{status: string, message: string}> => {
  return apiRequest<{status: string, message: string}>('/health');
};
