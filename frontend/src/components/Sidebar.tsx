import { Link, useLocation } from 'react-router-dom'
import { BookOpen, User, BarChart3, Settings, Trophy, Target, CheckCircle, GraduationCap } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useEffect, useState } from 'react'
import { leaderboardService, LeaderboardRow } from '@/services/leaderboardService'

const Sidebar: React.FC = () => {
  const location = useLocation()
  const { user } = useAuth()
  const [isLeaderboardOpen, setIsLeaderboardOpen] = useState(false)
  const [sortBy, setSortBy] = useState<'score' | 'solved'>('solved')
  const [rows, setRows] = useState<LeaderboardRow[]>([])
  const [loading, setLoading] = useState(false)
  const [recent, setRecent] = useState<Array<{
    challenge_id: number
    completed_at?: string
    score: number
    user_id: number
    username: string
    full_name?: string
    avatar_url?: string
    exercise_id: number
    exercise_title: string
  }>>([])

  useEffect(() => {
    if (!isLeaderboardOpen) return
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
  }, [isLeaderboardOpen, sortBy])

  useEffect(() => {
    let timer: number | undefined
    const fetchRecent = async () => {
      const data = await leaderboardService.recent(6)
      setRecent(data)
    }
    fetchRecent()
    timer = window.setInterval(fetchRecent, 15000)
    return () => {
      if (timer) window.clearInterval(timer)
    }
  }, [])

  const navigation = [
    { name: '学习案例', href: '/exercises', icon: Target },
    { name: '基础知识', href: '/knowledge', icon: GraduationCap },
    { name: '学习笔记', href: '/notes', icon: BookOpen },
    { name: '学习进度', href: '/leaderboard', icon: BarChart3 },
    { name: '个人资料', href: '/profile', icon: User },
    { name: '学习仪表板', href: '/dashboard', icon: BarChart3 },
  ]

  // 如果是管理员，添加管理功能
  if (user?.is_superuser) {
    navigation.push({ name: '系统设置', href: '/admin', icon: Settings })
  }

  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen flex flex-col">
      <div className="p-6">
        <nav className="space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <item.icon className="h-5 w-5" />
                <span>{item.name}</span>
              </Link>
            )
          })}

          <button
            onClick={() => setIsLeaderboardOpen(true)}
            className="w-full flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors"
          >
            <Trophy className="h-5 w-5 text-yellow-600" />
            <span>排行榜</span>
          </button>
        </nav>
      </div>

      <div className="mt-auto sticky bottom-0 z-10 p-4 bg-white border-t border-gray-200">
        <div className="bg-gradient-to-br from-green-50 to-white border border-green-200 rounded-xl p-3">
          <div className="flex items-center justify-between mb-2">
            <div className="text-xs font-semibold text-green-700">最新通关</div>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </div>
          <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
            {recent.map((r) => (
              <div key={r.challenge_id} className="flex items-center space-x-2 text-xs">
                <div className="h-6 w-6 rounded-full bg-green-600 text-white flex items-center justify-center font-bold">
                  {r.username.slice(0,1).toUpperCase()}
                </div>
                <div className="flex-1 truncate">
                  <div className="truncate text-gray-800"><span className="font-medium">{r.full_name || r.username}</span> 通过了 <span className="font-medium">#{r.exercise_id}</span></div>
                  <div className="text-[10px] text-gray-500">{r.completed_at ? new Date(r.completed_at).toLocaleString() : ''}</div>
                </div>
              </div>
            ))}
            {recent.length === 0 && (
              <div className="text-[11px] text-gray-500">暂无最新通关</div>
            )}
          </div>
        </div>
      </div>

      {isLeaderboardOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/40">
          <div className="bg-white w-full max-w-4xl rounded-2xl shadow-xl border border-gray-200">
            <div className="p-6 border-b flex items-center justify-between">
              <div>
                <h3 className="text-xl font-bold text-gray-900">解题排行榜</h3>
                <p className="text-sm text-gray-500 mt-1">高端大气，低调奢华</p>
              </div>
              <button onClick={() => setIsLeaderboardOpen(false)} className="text-gray-500 hover:text-gray-700">关闭</button>
            </div>

            <div className="px-6 pt-4">
              <div className="inline-flex rounded-lg overflow-hidden border">
                <button
                  onClick={() => setSortBy('solved')}
                  className={`px-4 py-2 text-sm font-medium ${sortBy === 'solved' ? 'bg-gray-900 text-white' : 'bg-white text-gray-700'}`}
                >
                  解题数量排行
                </button>
                <button
                  onClick={() => setSortBy('score')}
                  className={`px-4 py-2 text-sm font-medium ${sortBy === 'score' ? 'bg-gray-900 text-white' : 'bg-white text-gray-700'}`}
                >
                  积分数量排行
                </button>
              </div>
            </div>

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
                          <div className="inline-flex items-center px-2.5 py-1 rounded-full bg-gray-100 text-gray-800 text-xs font-medium">#{idx + 1}</div>
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
                            <Trophy className="h-4 w-4" />
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
      )}
    </div>
  )
}

export default Sidebar

