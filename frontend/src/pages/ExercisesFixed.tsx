import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Play, Users, Star, Search, ChevronLeft, ChevronRight, Trophy, Target, Zap, Flame, Skull } from 'lucide-react'
import { exerciseService, Exercise, ExerciseStats } from '@/services/exerciseService'

// 难度配置
const difficultyConfig = {
  '初级': { color: 'bg-green-100 text-green-800', points: 10 },
  '中级': { color: 'bg-blue-100 text-blue-800', points: 35 },
  '高级': { color: 'bg-orange-100 text-orange-800', points: 60 },
  '困难': { color: 'bg-red-100 text-red-800', points: 100 },
  '地狱': { color: 'bg-purple-100 text-purple-800', points: 150 }
}

const PAGINATION_SIZE = 12

export default function ExercisesFixed() {
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [stats, setStats] = useState<ExerciseStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 只执行一次的useEffect
  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('开始获取数据...')
        setLoading(true)
        setError(null)
        
        const [exercisesData, statsData] = await Promise.all([
          exerciseService.getExercises({ limit: PAGINATION_SIZE }),
          exerciseService.getStatistics()
        ])
        
        console.log('获取到的题目数据:', exercisesData)
        console.log('获取到的统计数据:', statsData)
        
        setExercises(exercisesData || [])
        setStats(statsData)
      } catch (err) {
        console.error('获取数据失败:', err)
        setError(err instanceof Error ? err.message : '获取数据失败')
        setExercises([])
        setStats({ total: 0, by_difficulty: {} })
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, []) // 空依赖数组，只执行一次

  const getDifficultyIcon = (difficulty: string) => {
    switch (difficulty) {
      case '初级':
        return <Target className="h-4 w-4" />
      case '中级':
        return <Zap className="h-4 w-4" />
      case '高级':
        return <Flame className="h-4 w-4" />
      case '困难':
        return <Trophy className="h-4 w-4" />
      case '地狱':
        return <Skull className="h-4 w-4" />
      default:
        return <Target className="h-4 w-4" />
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    return difficultyConfig[difficulty as keyof typeof difficultyConfig]?.color || 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-2">加载题目中...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-4">加载失败</h1>
          <p className="text-red-500 mb-4">错误信息: {error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            重新加载
          </button>
        </div>
      </div>
    )
  }

  console.log('ExercisesFixed render:', { 
    loading, 
    exercisesCount: exercises.length, 
    stats,
    exercises: exercises.slice(0, 2) // 只显示前2个用于调试
  })

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">爬虫逆向挑战赛 (修复版)</h1>
        <div className="text-sm text-gray-500 mb-4">
          调试信息: 题目数量={exercises.length}, 统计={stats?.total || 0}
        </div>
        <p className="text-gray-600">100道精心设计的爬虫逆向题目，从初级到地狱难度，挑战你的技术极限</p>
      </div>

      {/* 统计信息 */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <Trophy className="h-8 w-8 text-yellow-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">总题目数</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              </div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <Target className="h-8 w-8 text-green-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">初级题目</p>
                <p className="text-2xl font-bold text-gray-900">{stats.by_difficulty['初级'] || 0}</p>
              </div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <Zap className="h-8 w-8 text-blue-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">中级题目</p>
                <p className="text-2xl font-bold text-gray-900">{stats.by_difficulty['中级'] || 0}</p>
              </div>
            </div>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <Flame className="h-8 w-8 text-orange-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">高级题目</p>
                <p className="text-2xl font-bold text-gray-900">{stats.by_difficulty['高级'] || 0}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 题目列表 */}
      {exercises.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg mb-4">暂无题目数据</div>
          <div className="text-gray-400 text-sm">请检查数据库连接或联系管理员</div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-sm font-medium text-gray-500">#{exercise.id}</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center space-x-1 ${getDifficultyColor(exercise.difficulty)}`}>
                        {getDifficultyIcon(exercise.difficulty)}
                        <span>{exercise.difficulty}</span>
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                      {exercise.title}
                    </h3>
                    <p className="text-gray-600 text-sm mb-3 line-clamp-3">
                      {exercise.description}
                    </p>
                  </div>
                </div>
                
                <div className="flex flex-wrap gap-1 mb-3">
                  {exercise.tags.map((tag, index) => (
                    <span key={index} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 text-yellow-500" />
                    <span>{exercise.points}分</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Users className="h-4 w-4" />
                    <span>{exercise.success_count}人解决</span>
                  </div>
                </div>
                
                <Link
                  to={`/exercises/${exercise.id}`}
                  className="w-full inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
                >
                  <Play className="h-4 w-4 mr-2" />
                  开始挑战
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

