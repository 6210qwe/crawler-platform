import { api } from './api'

export interface ChallengeData {
  id: number
  userId: number
  exerciseId: number
  totalSum: number
  isCompleted: boolean
  completedAt?: string
  attempts: number
  bestTime?: number
  score?: number
  totalPages: number
}

export interface ChallengeSubmission {
  exerciseId: number
  answer: number
  timeSpent: number
}

export interface ChallengePage {
  pageNumber: number
  numbers: number[]
  startIndex: number
  endIndex: number
}

// 生成用户特定的挑战数据
// 本地生成逻辑不再暴露给页面使用，保留需要时可开关

// 获取挑战数据
export const getChallengeData = async (exerciseId: number): Promise<ChallengeData> => {
  try {
    const response = await api.get(`/challenges/${exerciseId}`)
    const d = response.data
    // 转换为 camelCase
    const mapped: ChallengeData = {
      id: d.id,
      userId: d.user_id,
      exerciseId: d.exercise_id,
      totalSum: d.total_sum,
      isCompleted: d.is_completed,
      completedAt: d.completed_at ?? undefined,
      attempts: d.attempts,
      bestTime: d.best_time ?? undefined,
      score: d.score ?? undefined,
      totalPages: d.total_pages,
    }
    return mapped
  } catch (error) {
    console.error('Failed to fetch challenge data:', error)
    throw error
  }
}

// 获取挑战页面数据
export const getChallengePage = async (exerciseId: number, pageNumber: number): Promise<ChallengePage> => {
  try {
    const response = await api.get(`/challenges/${exerciseId}/page/${pageNumber}`)
    const d = response.data
    const mapped: ChallengePage = {
      pageNumber: d.page_number,
      numbers: d.numbers,
      startIndex: d.start_index,
      endIndex: d.end_index,
    }
    return mapped
  } catch (error) {
    console.error('Failed to fetch challenge page:', error)
    throw error
  }
}

// 提交挑战答案
export const submitChallenge = async (submission: ChallengeSubmission): Promise<{
  success: boolean
  message: string
  isCorrect: boolean
  correctAnswer?: number
  score?: number
  completedAt?: string
}> => {
  try {
    // 转换字段名为后端期望的格式
    const backendSubmission = {
      exercise_id: submission.exerciseId,
      answer: submission.answer,
      time_spent: submission.timeSpent
    }
    
    const response = await api.post('/challenges/submit', backendSubmission)
    return response.data
  } catch (error) {
    console.error('Failed to submit challenge:', error)
    throw error
  }
}

// 获取用户挑战进度
export const getUserProgress = async (): Promise<{
  completedChallenges: number[]
  totalScore: number
  totalAttempts: number
  averageTime: number
}> => {
  try {
    const response = await api.get('/challenges/progress')
    const d = response.data
    return {
      completedChallenges: d.completed_challenges || [],
      totalScore: d.total_score || 0,
      totalAttempts: d.total_attempts || 0,
      averageTime: d.average_time || 0,
    }
  } catch (error) {
    console.error('Failed to fetch user progress:', error)
    throw error
  }
}

// 获取挑战排行榜
export const getChallengeLeaderboard = async (exerciseId?: number): Promise<{
  rank: number
  username: string
  score: number
  completedAt: string
  timeSpent: number
}[]> => {
  try {
    const url = exerciseId ? `/challenges/leaderboard/${exerciseId}` : '/challenges/leaderboard'
    const response = await api.get(url)
    return response.data
  } catch (error) {
    console.error('Failed to fetch leaderboard:', error)
    throw error
  }
}
