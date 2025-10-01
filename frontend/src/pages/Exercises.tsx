import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Play, Users, Star, Search, ChevronLeft, ChevronRight, Trophy, Target, Zap, Flame, Skull } from 'lucide-react'
import { exerciseService, Exercise, ExerciseStats } from '@/services/exerciseService'
import * as challengeService from '@/services/challengeService'

// 难度配置
const difficultyConfig = {
  '初级': {
    // 银色（金属感）
    badge: 'backdrop-blur bg-white/70 text-slate-800 ring-1 ring-white/40 shadow-sm',
    iconBg: 'bg-gradient-to-br from-slate-400/25 to-slate-600/10 text-slate-700',
    frame: 'bg-gradient-to-r from-slate-300/70 via-white to-slate-200/70',
    points: 10,
  },
  '中级': {
    // 钛灰（金属感偏冷）
    badge: 'backdrop-blur bg-white/70 text-slate-800 ring-1 ring-white/40 shadow-sm',
    iconBg: 'bg-gradient-to-br from-zinc-400/25 to-zinc-600/10 text-zinc-700',
    frame: 'bg-gradient-to-r from-zinc-300/70 via-white to-zinc-200/70',
    points: 35,
  },
  '高级': {
    // 玫瑰金
    badge: 'backdrop-blur bg-white/70 text-slate-800 ring-1 ring-white/40 shadow-sm',
    iconBg: 'bg-gradient-to-br from-rose-400/25 to-amber-400/10 text-rose-600',
    frame: 'bg-gradient-to-r from-rose-200/70 via-white to-amber-100/70',
    points: 60,
  },
  '困难': {
    // 黄金
    badge: 'backdrop-blur bg-white/70 text-slate-800 ring-1 ring-white/40 shadow-sm',
    iconBg: 'bg-gradient-to-br from-amber-500/25 to-yellow-500/10 text-amber-600',
    frame: 'bg-gradient-to-r from-amber-200/70 via-white to-yellow-100/70',
    points: 100,
  },
  '地狱': {
    // 钛紫金（冷冽高阶）
    badge: 'backdrop-blur bg-white/70 text-slate-800 ring-1 ring-white/40 shadow-sm',
    iconBg: 'bg-gradient-to-br from-violet-500/25 to-indigo-500/10 text-violet-600',
    frame: 'bg-gradient-to-r from-violet-200/70 via-white to-indigo-100/70',
    points: 150,
  },
}

const PAGINATION_SIZE = 9

export default function Exercises() {
  const { loading } = useAuth()
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [stats, setStats] = useState<ExerciseStats | null>(null)
  const [filteredTotal, setFilteredTotal] = useState<number | null>(null)
  const [completedIds, setCompletedIds] = useState<number[]>([])
  const [loadingExercises, setLoadingExercises] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [difficultyFilter, setDifficultyFilter] = useState('all')
  const [sortBy, setSortBy] = useState('sort_order')
  const [currentPage, setCurrentPage] = useState(1)

  // 获取题目数据 - 初始加载
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoadingExercises(true)
        const [exercisesData, statsData, progress, count] = await Promise.all([
          exerciseService.getExercises({
            search: searchTerm || undefined,
            difficulty: difficultyFilter !== 'all' ? difficultyFilter : undefined,
            sort_by: sortBy,
            skip: (currentPage - 1) * PAGINATION_SIZE,
            limit: PAGINATION_SIZE
          }),
          exerciseService.getStatistics(),
          challengeService.getUserProgress(),
          exerciseService.countExercises({
            search: searchTerm || undefined,
            difficulty: difficultyFilter !== 'all' ? difficultyFilter : undefined,
          })
        ])
        console.log('Fetched exercises:', exercisesData)
        console.log('Fetched stats:', statsData)
        console.log('Fetched progress:', progress)
        console.log('Fetched filtered total:', count)
        setExercises(exercisesData || [])
        setStats(statsData)
        setCompletedIds(progress?.completedChallenges || [])
        setFilteredTotal(count)
      } catch (error) {
        console.error('Failed to fetch exercises:', error)
        setError(error instanceof Error ? error.message : '获取数据失败')
        // 设置空数据避免页面空白
        setExercises([])
        setStats({ total: 0, by_difficulty: {} })
      } finally {
        setLoadingExercises(false)
      }
    }

    fetchInitialData()
  }, []) // 只执行一次初始加载

  // 处理搜索和筛选变化
  useEffect(() => {
    if (loadingExercises) return // 避免在初始加载时重复请求
    
    const fetchFilteredData = async () => {
      try {
        setLoadingExercises(true)
        const [exercisesData, count] = await Promise.all([
          exerciseService.getExercises({
            search: searchTerm || undefined,
            difficulty: difficultyFilter !== 'all' ? difficultyFilter : undefined,
            sort_by: sortBy,
            skip: (currentPage - 1) * PAGINATION_SIZE,
            limit: PAGINATION_SIZE
          }),
          exerciseService.countExercises({
            search: searchTerm || undefined,
            difficulty: difficultyFilter !== 'all' ? difficultyFilter : undefined,
          })
        ])
        console.log('Fetched filtered exercises:', exercisesData)
        console.log('Fetched filtered total:', count)
        setExercises(exercisesData || [])
        setFilteredTotal(count)
      } catch (error) {
        console.error('Failed to fetch filtered exercises:', error)
        setError(error instanceof Error ? error.message : '获取筛选数据失败')
        setExercises([])
      } finally {
        setLoadingExercises(false)
      }
    }

    fetchFilteredData()
  }, [searchTerm, difficultyFilter, sortBy, currentPage])

  const totalPages = Math.ceil(((filteredTotal ?? stats?.total) || 0) / PAGINATION_SIZE)
  const startIndex = (currentPage - 1) * PAGINATION_SIZE

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

  const getDifficultyBadge = (difficulty: string) => {
    const cfg = difficultyConfig[difficulty as keyof typeof difficultyConfig]
    return cfg?.badge || 'backdrop-blur bg-white/70 text-slate-800 ring-1 ring-white/40 shadow-sm'
  }

  const getDifficultyIconBg = (difficulty: string) => {
    const cfg = difficultyConfig[difficulty as keyof typeof difficultyConfig]
    return cfg?.iconBg || 'bg-gray-500/10 text-gray-600'
  }

  const getDifficultyFrame = (difficulty: string) => {
    const cfg = difficultyConfig[difficulty as keyof typeof difficultyConfig] as any
    return cfg?.frame || 'bg-gradient-to-r from-slate-200/60 via-white to-slate-200/60'
  }

  if (loadingExercises) {
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

  console.log('Exercises render:', { 
    loading, 
    loadingExercises, 
    exercisesCount: exercises.length, 
    stats,
    searchTerm,
    difficultyFilter,
    sortBy,
    currentPage
  })

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">爬虫逆向挑战赛</h1>
        <div className="text-sm text-gray-500 mb-4">
          调试信息: 题目数量={exercises.length}, 统计={stats?.total || 0}
        </div>
        <p className="text-gray-600">100道精心设计的爬虫逆向题目，从初级到地狱难度，挑战你的技术极限</p>
      </div>

      {/* 统计信息 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-gray-900">{stats?.total || 0}</div>
          <div className="text-sm text-gray-500">总题目数</div>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-green-600">{completedIds.length}</div>
          <div className="text-sm text-gray-500">已解决题目</div>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-blue-600">{stats?.by_difficulty?.['初级'] || 0}</div>
          <div className="text-sm text-gray-500">初级题目</div>
        </div>
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 text-center">
          <div className="text-2xl font-bold text-purple-600">{stats?.by_difficulty?.['地狱'] || 0}</div>
          <div className="text-sm text-gray-500">地狱题目</div>
        </div>
      </div>

      {/* 搜索和筛选 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex flex-col md:flex-row gap-4 items-center">
          <div className="flex-1 w-full">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="搜索题目..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value)
                  setCurrentPage(1) // 搜索时重置页码
                }}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2 w-full md:w-auto">
            <label htmlFor="difficulty-filter" className="sr-only">难度筛选</label>
            <select
              id="difficulty-filter"
              value={difficultyFilter}
              onChange={(e) => {
                setDifficultyFilter(e.target.value)
                setCurrentPage(1) // 筛选时重置页码
              }}
              className="input w-full md:w-32"
            >
              <option value="all">全部难度</option>
              {Object.keys(difficultyConfig).map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>
          <div className="flex items-center space-x-2 w-full md:w-auto">
            <label htmlFor="sort-by" className="sr-only">排序方式</label>
            <select
              id="sort-by"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="input w-full md:w-32"
            >
              <option value="sort_order">默认排序</option>
              <option value="points">按积分排序</option>
              <option value="solved">按解决人数</option>
            </select>
          </div>
        </div>
      </div>

      {/* 题目列表 */}
      {exercises.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-500 text-lg mb-4">暂无题目数据</div>
          <div className="text-gray-400 text-sm">请检查数据库连接或联系管理员</div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {exercises.map((exercise, index) => {
            const displayNumber = (currentPage - 1) * PAGINATION_SIZE + index + 1
            return (
          <div key={exercise.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className="text-sm font-medium text-gray-500">#{displayNumber.toString().padStart(2, '0')}</span>
                    <span className={`group inline-flex rounded-full p-[1px] transition-all duration-200 ease-out ${getDifficultyFrame(exercise.difficulty)} hover:shadow-[0_0_18px_-6px_rgba(0,0,0,0.25)] hover:scale-[1.02]` }>
                      <span className={`px-3 py-1.5 rounded-full text-[11px] font-medium inline-flex items-center gap-1.5 transition-all duration-200 ease-out ${getDifficultyBadge(exercise.difficulty)} hover:shadow-md` }>
                        <span className={`inline-flex items-center justify-center h-4 w-4 rounded-full shadow-sm transition-transform duration-200 ${getDifficultyIconBg(exercise.difficulty)} group-hover:scale-110`}>
                          {getDifficultyIcon(exercise.difficulty)}
                        </span>
                        <span className="tracking-wide">{exercise.difficulty}</span>
                      </span>
                    </span>
                    {completedIds.includes(exercise.id) && (
                      <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">已通关</span>
                    )}
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                    {exercise.title}
                  </h3>
                  <p className="text-gray-600 text-sm line-clamp-3 mb-3">
                    {exercise.description}
                  </p>
                </div>
              </div>
              
              
              <div className="border-t border-gray-100 pt-4 mt-4">
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-1">
                      <Star className="h-4 w-4 text-yellow-500" />
                      <span>{exercise.points}分</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Users className="h-4 w-4" />
                      <span>{exercise.success_count}人解决</span>
                    </div>
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
          </div>
          )
          })}
        </div>
      )}

      {/* 分页 */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-700">
            显示 {startIndex + 1} 到 {Math.min(startIndex + PAGINATION_SIZE, (filteredTotal ?? stats?.total) || 0)}，共 {(filteredTotal ?? stats?.total) || 0} 条
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
              className="p-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>

            {Array.from({ length: totalPages }, (_, i) => {
              const page = i + 1
              return (
                <button
                  key={page}
                  onClick={() => setCurrentPage(page)}
                  className={`px-3 py-2 text-sm font-medium rounded-md ${
                    currentPage === page
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-700 hover:bg-gray-50 border border-gray-300'
                  }`}
                >
                  {page}
                </button>
              )
            })}

            <button
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
              className="p-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}