/**
 * API service for kvizAI backend communication
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Types for API requests and responses
export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    id: string;
    username: string;
    email: string;
    profile_picture?: string;
    bio?: string;
    total_score: number;
    quizzes_taken: number;
    quizzes_created: number;
    is_active: boolean;
    is_verified: boolean;
    created_at: string;
    last_login?: string;
  };
}

export interface User {
  id: string;
  username: string;
  email: string;
  profile_picture?: string;
  bio?: string;
  total_score: number;
  quizzes_taken: number;
  quizzes_created: number;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
}

export interface ApiError {
  detail: string;
}

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// Helper function to handle API responses
const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// Auth API functions
export const authAPI = {
  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse(response);
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};

// Questionnaire types and API
export interface QuestionnaireQuestion {
  question: string;
  context?: string;
  keywords?: string[];
  expected_answer_type?: string;
}

export interface QuestionnaireCreate {
  title: string;
  description?: string;
  subject: string;
  difficulty_level: 'easy' | 'medium' | 'hard';
  questions: QuestionnaireQuestion[];
  is_public: boolean;
}

export interface Questionnaire {
  id: string;
  creator_id: string;
  title: string;
  description?: string;
  subject: string;
  difficulty_level: string;
  questions: any[];
  version: number;
  is_public: boolean;
  is_template: boolean;
  times_used: number;
  average_score: number;
  question_count: number;
  created_at: string;
  updated_at: string;
  creator_username?: string;
}

export const questionnaireAPI = {
  create: async (data: QuestionnaireCreate): Promise<Questionnaire> => {
    const response = await fetch(`${API_BASE_URL}/questionnaires/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  getAll: async (params?: {
    skip?: number;
    limit?: number;
    subject?: string;
    difficulty?: string;
    search?: string;
  }): Promise<Questionnaire[]> => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.subject) queryParams.append('subject', params.subject);
    if (params?.difficulty) queryParams.append('difficulty', params.difficulty);
    if (params?.search) queryParams.append('search', params.search);

    const response = await fetch(`${API_BASE_URL}/questionnaires/?${queryParams}`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  getMy: async (): Promise<Questionnaire[]> => {
    const response = await fetch(`${API_BASE_URL}/questionnaires/my`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  getById: async (id: string): Promise<Questionnaire> => {
    const response = await fetch(`${API_BASE_URL}/questionnaires/${id}`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },
};

// Quiz types and API
export interface QuizCreate {
  questionnaire_id: string;
  title?: string;
  time_limit?: number;
  max_score: number;
  is_public: boolean;
  ai_model?: 'llama2' | 'gemini';
}

export interface Quiz {
  id: string;
  questionnaire_id?: string;
  creator_id?: string;
  title: string;
  description?: string;
  subject: string;
  questions: any[];
  time_limit?: number;
  difficulty: string;
  max_score: number;
  is_global: boolean;
  is_public: boolean;
  is_template: boolean;
  ai_model_used?: string;
  generation_time?: number;
  times_taken: number;
  average_score: number;
  average_time: number;
  expires_at?: string;
  created_at: string;
  updated_at: string;
  question_count: number;
  creator_username?: string;
}

export interface QuizAttempt {
  id: string;
  user_id: string;
  quiz_id: string;
  score: number;
  max_score: number;
  percentage: number;
  time_taken: number;
  started_at: string;
  completed_at?: string;
  is_completed: boolean;
  is_timed_out: boolean;
  correct_answers: number;
  incorrect_answers: number;
  skipped_answers: number;
  accuracy: number;
  speed: number;
  created_at: string;
  quiz_title?: string;
  quiz_subject?: string;
}

export const quizAPI = {
  generate: async (data: QuizCreate): Promise<Quiz> => {
    const response = await fetch(`${API_BASE_URL}/quizzes/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  getAll: async (params?: {
    skip?: number;
    limit?: number;
    subject?: string;
    difficulty?: string;
    search?: string;
  }): Promise<Quiz[]> => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.subject) queryParams.append('subject', params.subject);
    if (params?.difficulty) queryParams.append('difficulty', params.difficulty);
    if (params?.search) queryParams.append('search', params.search);

    const response = await fetch(`${API_BASE_URL}/quizzes/?${queryParams}`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  getById: async (quizId: string): Promise<Quiz> => {
    const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  startAttempt: async (quizId: string): Promise<QuizAttempt> => {
    const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}/start`, {
      method: 'POST',
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  submitQuiz: async (quizId: string, answers: number[], timeTaken: number): Promise<QuizAttempt> => {
    const response = await fetch(`${API_BASE_URL}/quizzes/${quizId}/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify({
        answers,
        time_taken: timeTaken
      }),
    });
    return handleResponse(response);
  },
};

// User statistics
export interface UserStats {
  total_score: number;
  quizzes_taken: number;
  quizzes_created: number;
  average_score: number;
  rank?: number;
  achievements_count: number;
}

export interface UserQuizAttempt {
  quiz_id: string;
  quiz_title: string;
  last_score: number;
  max_score: number;
  last_percentage: number;
  last_completed_at: string | null;
}

export const userAPI = {
  getStats: async (): Promise<UserStats> => {
    const response = await fetch(`${API_BASE_URL}/users/stats`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  getAchievements: async () => {
    const response = await fetch(`${API_BASE_URL}/users/achievements`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },

  getQuizAttempts: async (): Promise<UserQuizAttempt[]> => {
    const response = await fetch(`${API_BASE_URL}/users/quiz-attempts`, {
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  },
};

// Auth context helper functions
export const setAuthToken = (token: string) => {
  localStorage.setItem('access_token', token);
};

export const getAuthToken = () => {
  return localStorage.getItem('access_token');
};

export const setUser = (user: User) => {
  localStorage.setItem('user', JSON.stringify(user));
};

export const getUser = (): User | null => {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
};

export const isAuthenticated = () => {
  return !!getAuthToken();
};