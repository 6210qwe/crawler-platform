import { api } from './api'

export interface LeaderboardRow {
  user_id: number
  username: string
  full_name?: string
  avatar_url?: string
  total_score: number
  solved_count: number
  honor_title: string
  last_submission_at?: string
}

export const leaderboardService = {
  async list(sortBy: 'score' | 'solved' = 'score'): Promise<LeaderboardRow[]> {
    const res = await api.get(`/challenges/leaderboard?sort_by=${sortBy}`)
    return res.data
  },
  async recent(limit = 10): Promise<Array<{
    challenge_id: number
    completed_at?: string
    score: number
    user_id: number
    username: string
    full_name?: string
    avatar_url?: string
    exercise_id: number
    exercise_title: string
  }>> {
    const res = await api.get(`/challenges/recent-completions?limit=${limit}`)
    return res.data
  }
}


