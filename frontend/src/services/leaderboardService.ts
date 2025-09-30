import { api } from './api'

export interface LeaderboardRow {
  user_id: number
  username: string
  full_name?: string
  total_score: number
  solved_count: number
  last_submission_at?: string
}

export const leaderboardService = {
  async list(): Promise<LeaderboardRow[]> {
    const res = await api.get('/leaderboard')
    return res.data
  },
}


