import { useEffect, useState } from 'react'
import { leaderboardService, LeaderboardRow } from '../services/leaderboardService'
import { Crown, ChevronDown } from 'lucide-react'

export default function Leaderboard() {
  const [rows, setRows] = useState<LeaderboardRow[]>([])
  const [loading, setLoading] = useState(false)
  const [sortBy, setSortBy] = useState<'score' | 'solved'>('score')

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      try {
        const data = await leaderboardService.list(sortBy)
        setRows(data)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [sortBy])

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">解题排行榜</h1>
          <p className="text-gray-500 mt-1">高端大气又简洁优雅的实力榜单</p>
        </div>
        <div className="relative inline-block text-left">
          <button
            onClick={() => setSortBy(prev => (prev === 'score' ? 'solved' : 'score'))}
            className="inline-flex items-center px-4 py-2 rounded-md border shadow-sm bg-white hover:bg-gray-50 text-sm font-medium text-gray-700"
          >
            {sortBy === 'score' ? '按积分' : '按解题数'} 排序
            <ChevronDown className="ml-2 h-4 w-4 text-gray-500" />
          </button>
        </div>
      </div>

      <div className="bg-gradient-to-br from-gray-50 to-white rounded-2xl shadow-sm border border-gray-200">
        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr className="text-left text-gray-600 border-b">
                  <th className="py-3 pr-4">排名</th>
                  <th className="py-3 pr-4">用户</th>
                  <th className="py-3 pr-4">荣誉称号</th>
                  <th className="py-3 pr-4">总分</th>
                  <th className="py-3 pr-4">通过题数</th>
                  <th className="py-3 pr-4">最近提交</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, idx) => (
                  <tr key={r.user_id} className="border-b hover:bg-gray-50">
                    <td className="py-3 pr-4">
                      <div className="inline-flex items-center px-2.5 py-1 rounded-full bg-gray-100 text-gray-800 text-xs font-medium">
                        #{idx + 1}
                      </div>
                    </td>
                    <td className="py-3 pr-4">
                      <div className="flex items-center space-x-3">
                        {r.avatar_url ? (
                          <img src={r.avatar_url} alt={r.username} className="h-8 w-8 rounded-full object-cover" />
                        ) : (
                          <div className="h-8 w-8 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center text-white text-xs font-bold">
                            {r.username.slice(0, 1).toUpperCase()}
                          </div>
                        )}
                        <div>
                          <div className="font-semibold text-gray-900">{r.full_name || r.username}</div>
                          <div className="text-xs text-gray-500">@{r.username}</div>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 pr-4">
                      <div className="inline-flex items-center space-x-1 px-2.5 py-1 rounded-full bg-yellow-50 text-yellow-700 border border-yellow-200">
                        <Crown className="h-4 w-4" />
                        <span className="text-xs font-medium">{r.honor_title}</span>
                      </div>
                    </td>
                    <td className="py-3 pr-4 font-semibold text-gray-900">{r.total_score}</td>
                    <td className="py-3 pr-4 text-gray-900">{r.solved_count}</td>
                    <td className="py-3 pr-4 text-gray-500">{r.last_submission_at ? new Date(r.last_submission_at).toLocaleString() : '-'}</td>
                  </tr>
                ))}
                {!loading && rows.length === 0 && (
                  <tr>
                    <td colSpan={6} className="py-10 text-center text-gray-500">暂无数据</td>
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


