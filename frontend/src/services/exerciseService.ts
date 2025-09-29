import { api } from './api'

export interface Exercise {
  id: number
  title: string
  description: string
  target_url: string
  difficulty: 'beginner' | 'intermediate' | 'advanced' | 'hard' | 'hell'
  status: 'draft' | 'published' | 'archived'
  points: number
  time_limit: number
  hints?: string
  created_by: number
  created_at: string
  updated_at?: string
}

export interface ExerciseSubmission {
  id: number
  user_id: number
  exercise_id: number
  answer: string
  status: 'pending' | 'correct' | 'incorrect' | 'timeout'
  score: number
  submitted_at: string
}

export interface CreateExerciseData {
  title: string
  description: string
  target_url: string
  difficulty: 'beginner' | 'intermediate' | 'advanced' | 'hard' | 'hell'
  points: number
  time_limit: number
  hints?: string
}

export interface SubmitExerciseData {
  answer: string
}

export const exerciseService = {
  async getExercises(params?: {
    skip?: number
    limit?: number
    difficulty?: string
  }): Promise<Exercise[]> {
    const response = await api.get('/exercises', { params })
    return response.data
  },

  async getExercise(id: number): Promise<Exercise> {
    const response = await api.get(`/exercises/${id}`)
    return response.data
  },

  async createExercise(data: CreateExerciseData): Promise<Exercise> {
    const response = await api.post('/exercises', data)
    return response.data
  },

  async updateExercise(id: number, data: Partial<CreateExerciseData>): Promise<Exercise> {
    const response = await api.put(`/exercises/${id}`, data)
    return response.data
  },

  async submitExercise(id: number, data: SubmitExerciseData): Promise<ExerciseSubmission> {
    const response = await api.post(`/exercises/${id}/submit`, data)
    return response.data
  },

  async getExerciseSubmissions(id: number): Promise<ExerciseSubmission[]> {
    const response = await api.get(`/exercises/${id}/submissions`)
    return response.data
  },
}

