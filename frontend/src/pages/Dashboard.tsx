import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { exerciseService, ExerciseSubmission } from '../services/exerciseService'
import { Trophy, Target, Clock, TrendingUp, Award, BarChart3 } from 'lucide-react'

const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const [submissions, setSubmissions] = useState<ExerciseSubmission[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        // 这里应该调用获取用户提交记录的API
        // const data = await exerciseService.getUserSubmissions()
        // setSubmissions(data)
      } catch (error) {
        console.error('Failed to fetch submissions:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchSubmissions()
  }, [])

  const stats = [
    {
      title: '完成练习',
      value: submissions.filter(s => s.status === 'correct').length,
      icon: Target,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: '总得分',
      value: submissions.reduce((sum, s) => sum + s.score, 0),
      icon: Trophy,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100'
    },
    {
      title: '正确率',
      value: submissions.length > 0 
        ? Math.round((submissions.filter(s => s.status === 'correct').length / submissions.length) * 100)
        : 0,
      suffix: '%',
      icon: TrendingUp,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: '平均用时',
      value: '2:30',
      icon: Clock,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    }
  ]

  const recentSubmissions = submissions.slice(0, 5)

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">仪表板</h1>
        <p className="text-gray-600">欢迎回来，{user?.username}！查看你的学习进度和成就</p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <div key={index} className="card">
            <div className="card-content">
              <div className="flex items-center">
                <div className={`p-3 rounded-full ${stat.bgColor}`}>
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stat.value}{stat.suffix}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* 最近提交 */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="card-header">
              <h2 className="card-title text-xl">最近提交</h2>
            </div>
            <div className="card-content">
              {recentSubmissions.length > 0 ? (
                <div className="space-y-4">
                  {recentSubmissions.map((submission) => (
                    <div key={submission.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="flex-shrink-0">
                          {submission.status === 'correct' ? (
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                              <Award className="h-4 w-4 text-green-600" />
                            </div>
                          ) : (
                            <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                              <Target className="h-4 w-4 text-red-600" />
                            </div>
                          )}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">练习题 #{submission.exercise_id}</p>
                          <p className="text-sm text-gray-500">
                            {new Date(submission.submitted_at).toLocaleString()}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900">{submission.score} 分</p>
                        <p className={`text-sm ${
                          submission.status === 'correct' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {submission.status === 'correct' ? '正确' : '错误'}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">还没有提交记录</p>
                  <p className="text-sm text-gray-400 mt-1">开始你的第一个练习吧！</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 学习进度 */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title text-lg">学习进度</h3>
            </div>
            <div className="card-content">
              <div className="space-y-6">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">JavaScript逆向</span>
                    <span className="text-gray-900">0%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-primary-600 h-2 rounded-full" style={{ width: '0%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">反爬虫技术</span>
                    <span className="text-gray-900">0%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-primary-600 h-2 rounded-full" style={{ width: '0%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">加密算法</span>
                    <span className="text-gray-900">0%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-primary-600 h-2 rounded-full" style={{ width: '0%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="card mt-6">
            <div className="card-header">
              <h3 className="card-title text-lg">成就徽章</h3>
            </div>
            <div className="card-content">
              <div className="text-center py-8">
                <Trophy className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">还没有获得徽章</p>
                <p className="text-sm text-gray-400 mt-1">继续努力，解锁更多成就！</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

