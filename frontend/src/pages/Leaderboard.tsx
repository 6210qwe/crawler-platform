import { useEffect, useState } from 'react'
import { leaderboardService, LeaderboardRow } from '../services/leaderboardService'

export default function Leaderboard() {
  const [rows, setRows] = useState<LeaderboardRow[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const data = await leaderboardService.list()
        setRows(data)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="max-w-5xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">闯关排行榜</h1>
      <div className="card">
        <div className="card-content">
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-gray-600">
                  <th className="py-2 pr-4">排名</th>
                  <th className="py-2 pr-4">用户</th>
                  <th className="py-2 pr-4">总分</th>
                  <th className="py-2 pr-4">通过题数</th>
                  <th className="py-2 pr-4">最近提交</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, idx) => (
                  <tr key={r.user_id} className="border-t">
                    <td className="py-2 pr-4">{idx + 1}</td>
                    <td className="py-2 pr-4">{r.full_name || r.username}</td>
                    <td className="py-2 pr-4">{r.total_score}</td>
                    <td className="py-2 pr-4">{r.solved_count}</td>
                    <td className="py-2 pr-4">{r.last_submission_at ? new Date(r.last_submission_at).toLocaleString() : '-'}</td>
                  </tr>
                ))}
                {!loading && rows.length === 0 && (
                  <tr>
                    <td colSpan={5} className="py-6 text-center text-gray-500">暂无数据</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}


