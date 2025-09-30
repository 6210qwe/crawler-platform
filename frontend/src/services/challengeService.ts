import { api } from './api'

export interface ChallengeData {
  id: number
  userId: number
  exerciseId: number
  numbers: number[][]
  totalSum: number
  isCompleted: boolean
  completedAt?: string
  attempts: number
  bestTime?: number
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
export const generateChallengeData = (exerciseId: number, userId: number): ChallengeData => {
  const numbers: number[][] = []
  let totalSum = 0
  
  // 生成100页，每页10个数字
  for (let page = 0; page < 100; page++) {
    const pageNumbers: number[] = []
    for (let i = 0; i < 10; i++) {
      // 使用用户ID和题目ID作为种子，确保每个用户的数据不同
      const seed = (userId * 1000 + exerciseId * 100 + page * 10 + i) % 200 + 1
      pageNumbers.push(seed)
      totalSum += seed
    }
    numbers.push(pageNumbers)
  }
  
  return {
    id: 0,
    userId,
    exerciseId,
    numbers,
    totalSum,
    isCompleted: false,
    attempts: 0
  }
}

// 获取挑战数据
export const getChallengeData = async (exerciseId: number): Promise<ChallengeData> => {
  try {
    const response = await api.get(`/challenges/${exerciseId}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch challenge data:', error)
    throw error
  }
}

// 获取挑战页面数据
export const getChallengePage = async (exerciseId: number, pageNumber: number): Promise<ChallengePage> => {
  try {
    const response = await api.get(`/challenges/${exerciseId}/page/${pageNumber}`)
    return response.data
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
    const response = await api.post('/challenges/submit', submission)
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
    return response.data
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
