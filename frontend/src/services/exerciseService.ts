import { api } from './api'

export interface Exercise {
  id: number
  title: string
  difficulty: '初级' | '中级' | '高级' | '困难' | '地狱'
  description: string
  challenge_points: string
  tags: string[]
  points: number
  is_active: boolean
  sort_order: number
  view_count: number
  attempt_count: number
  success_count: number
  avg_time?: number
  created_at: string
  updated_at?: string
}

export interface ExerciseSubmission {
  id: number
  exercise_id: number
  user_id: number
  answer?: string
  is_correct: boolean
  score?: number
  time_spent?: number
  submitted_at: string
}

export interface ExerciseStats {
  total: number
  by_difficulty: {
    [key: string]: number
  }
}

export interface UserProgress {
  total_attempts: number
  completed_exercises: number
  total_score: number
}

export interface ExerciseFilters {
  skip?: number
  limit?: number
  difficulty?: string
  search?: string
  sort_by?: string
}

class ExerciseService {
  // 获取题目列表
  async getExercises(filters: ExerciseFilters = {}): Promise<Exercise[]> {
    try {
      const params = new URLSearchParams()
      if (filters.skip) params.append('skip', filters.skip.toString())
      if (filters.limit) params.append('limit', filters.limit.toString())
      if (filters.difficulty) params.append('difficulty', filters.difficulty)
      if (filters.search) params.append('search', filters.search)
      if (filters.sort_by) params.append('sort_by', filters.sort_by)

      const response = await api.get(`/exercises/?${params.toString()}`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch exercises:', error)
      throw error
    }
  }

  // 获取单个题目
  async getExercise(id: number): Promise<Exercise> {
    try {
      const response = await api.get(`/exercises/${id}`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch exercise:', error)
      throw error
    }
  }

  // 获取题目统计
  async getStatistics(): Promise<ExerciseStats> {
    try {
      const response = await api.get('/exercises/statistics/overview')
      return response.data
    } catch (error) {
      console.error('Failed to fetch statistics:', error)
      throw error
    }
  }

  // 提交答案
  async submitAnswer(exerciseId: number, answer: string, timeSpent?: number): Promise<ExerciseSubmission> {
    try {
      const response = await api.post(`/exercises/${exerciseId}/submit`, {
        answer,
        time_spent: timeSpent
      })
      return response.data
    } catch (error) {
      console.error('Failed to submit answer:', error)
      throw error
    }
  }

  // 获取用户进度
  async getUserProgress(): Promise<UserProgress> {
    try {
      const response = await api.get('/exercises/user/progress')
      return response.data
    } catch (error) {
      console.error('Failed to fetch user progress:', error)
      throw error
    }
  }
}

export const exerciseService = new ExerciseService()