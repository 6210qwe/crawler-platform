import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { ArrowLeft, Target, Zap, Flame, Trophy, Skull, CheckCircle, XCircle, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react'
import { exercises, difficultyConfig } from '@/data/exercises'
import * as challengeService from '@/services/challengeService'

const ExerciseDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user, loading: authLoading } = useAuth()
  const [exercise, setExercise] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [pageData, setPageData] = useState<{
    pageNumber: number
    numbers: number[]
    startIndex: number
    endIndex: number
  } | null>(null)
  const [totalSum, setTotalSum] = useState(0)
  const [userAnswer, setUserAnswer] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitResult, setSubmitResult] = useState<{
    success: boolean
    message: string
    isCorrect: boolean
    correctAnswer?: number
    score?: number
  } | null>(null)
  const [timeSpent, setTimeSpent] = useState(0)
  const [isTimerRunning, setIsTimerRunning] = useState(false)

  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login')
      return
    }
  }, [user, authLoading, navigate])

  useEffect(() => {
    const fetchData = async () => {
      if (!id || !user) return
      
      setLoading(true)
      try {
        // 获取题目信息
        const exerciseId = parseInt(id)
        const foundExercise = exercises.find(e => e.id === exerciseId)
        
        if (!foundExercise) {
          setError('题目不存在')
          setLoading(false)
          return
        }
        
        setExercise(foundExercise)
        
        // 获取挑战基本信息
        const challengeData = await challengeService.getChallengeData(exerciseId)
        setTotalSum(challengeData.totalSum)
        
        // 获取第一页数据
        const firstPageData = await challengeService.getChallengePage(exerciseId, 1)
        setPageData(firstPageData)
        setIsTimerRunning(true)
      } catch (error) {
        console.error('Failed to fetch data:', error)
        setError('加载数据失败')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [id, user])

  // 计时器
  useEffect(() => {
    let interval: number
    if (isTimerRunning) {
      interval = window.setInterval(() => {
        setTimeSpent(prev => prev + 1)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [isTimerRunning])

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const handlePageChange = async (page: number) => {
    if (page < 1 || page > 100 || !id) return
    
    setCurrentPage(page)
    setSubmitResult(null)
    
    try {
      // 使用分页API获取指定页面的数据
      const pageData = await challengeService.getChallengePage(parseInt(id), page)
      setPageData(pageData)
    } catch (error) {
      console.error('Failed to fetch page data:', error)
      setError('加载页面数据失败')
    }
  }

  const handleSubmit = async () => {
    if (!userAnswer.trim() || !id) return

    setIsSubmitting(true)
    try {
      const result = await challengeService.submitChallenge({
        exerciseId: parseInt(id),
        answer: parseInt(userAnswer),
        timeSpent
      })
      
      setSubmitResult(result)
      setIsTimerRunning(false)
    } catch (error) {
      console.error('Failed to submit challenge:', error)
      setSubmitResult({
        success: false,
        message: '提交失败，请重试',
        isCorrect: false
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const getDifficultyIcon = (difficulty: string) => {
    switch (difficulty) {
      case '初级':
        return <Target className="h-5 w-5" />
      case '中级':
        return <Zap className="h-5 w-5" />
      case '高级':
        return <Flame className="h-5 w-5" />
      case '困难':
        return <Trophy className="h-5 w-5" />
      case '地狱':
        return <Skull className="h-5 w-5" />
      default:
        return <Target className="h-5 w-5" />
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    return difficultyConfig[difficulty as keyof typeof difficultyConfig]?.color || 'bg-gray-100 text-gray-800'
  }

  if (authLoading || loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-600">
        <XCircle className="h-12 w-12 mx-auto mb-4" />
        <p className="text-lg mb-4">{error}</p>
        <button 
          onClick={() => navigate('/exercises')} 
          className="btn btn-primary"
        >
          返回题目列表
        </button>
      </div>
    )
  }

  if (!exercise || !pageData) {
    return (
      <div className="text-center py-12 text-gray-600">
        <AlertCircle className="h-12 w-12 mx-auto mb-4" />
        <p className="text-lg mb-4">数据不存在</p>
        <button 
          onClick={() => navigate('/exercises')} 
          className="btn btn-primary"
        >
          返回题目列表
        </button>
      </div>
    )
  }

  const currentPageNumbers = pageData.numbers

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-red-100">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* 返回按钮 */}
        <button 
          onClick={() => navigate('/exercises')} 
          className="text-red-600 hover:text-red-700 flex items-center space-x-2 mb-6"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>返回题目列表</span>
        </button>

        {/* 题目标题 */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <span className="text-sm font-medium text-red-600">#{exercise.id}</span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-2 ${getDifficultyColor(exercise.difficulty)}`}>
              {getDifficultyIcon(exercise.difficulty)}
              <span>{exercise.difficulty}</span>
            </span>
          </div>
          <h1 className="text-4xl font-bold text-yellow-400 mb-2">
            任务{exercise.id}: {exercise.title}
          </h1>
          <p className="text-lg text-red-600 mb-4">
            抓取这100页的数字，计算加和并提交结果，另外，祝大家2025年得偿所愿，心想事成❤
          </p>
        </div>

        {/* 统计信息 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-red-200 p-4 text-center">
            <div className="text-2xl font-bold text-red-600">{totalSum}</div>
            <div className="text-sm text-gray-600">正确答案</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-red-200 p-4 text-center">
            <div className="text-2xl font-bold text-blue-600">{formatTime(timeSpent)}</div>
            <div className="text-sm text-gray-600">用时</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-red-200 p-4 text-center">
            <div className="text-2xl font-bold text-green-600">{currentPage}/100</div>
            <div className="text-sm text-gray-600">当前页</div>
          </div>
          <div className="bg-white rounded-lg shadow-sm border border-red-200 p-4 text-center">
            <div className="text-2xl font-bold text-purple-600">1000</div>
            <div className="text-sm text-gray-600">总数字</div>
          </div>
        </div>

        {/* 数字显示区域 */}
        <div className="bg-white rounded-lg shadow-sm border border-red-200 p-8 mb-6">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              第 {pageData.pageNumber} 页 - 数字 {pageData.startIndex} 到 {pageData.endIndex}
            </h2>
          </div>
          
          {/* 数字网格 */}
          <div className="grid grid-cols-5 gap-4 mb-8">
            {currentPageNumbers.map((number, index) => (
              <div
                key={index}
                className="p-6 text-center rounded-lg border-2 border-blue-200 bg-blue-50 hover:bg-blue-100 transition-colors"
              >
                <div className="text-3xl font-bold text-blue-600">{number}</div>
              </div>
            ))}
          </div>

          {/* 分页导航 */}
          <div className="flex items-center justify-center space-x-2">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="p-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            
            {/* 显示页码逻辑 - 显示10个页码 */}
            {(() => {
              const pages = []
              const totalPages = 100
              const maxVisiblePages = 10
              
              // 计算显示的页码范围
              let start = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2))
              let end = Math.min(totalPages, start + maxVisiblePages - 1)
              
              // 如果接近末尾，调整起始位置
              if (end === totalPages) {
                start = Math.max(1, end - maxVisiblePages + 1)
              }
              
              // 显示页码按钮
              for (let page = start; page <= end; page++) {
                pages.push(
                  <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`px-3 py-2 text-sm font-medium rounded-md ${
                      currentPage === page
                        ? 'bg-green-600 text-white'
                        : 'text-gray-700 hover:bg-gray-50 border border-gray-300'
                    }`}
                  >
                    {page}
                  </button>
                )
              }
              
              return pages
            })()}
            
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === 100}
              className="p-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* 答案提交区域 */}
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="text-center mb-4">
            <h3 className="text-xl font-bold text-yellow-400 mb-2">请此处输入答案</h3>
          </div>
          
          <div className="flex items-center space-x-4">
            <input
              type="number"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="请输入1000个数字的总和"
              className="flex-1 px-4 py-3 bg-gray-700 text-white border border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
            />
            <button
              onClick={handleSubmit}
              disabled={isSubmitting || !userAnswer.trim()}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {isSubmitting ? '提交中...' : '提交答案'}
            </button>
          </div>

          {submitResult && (
            <div className={`mt-4 p-4 rounded-lg ${
              submitResult.isCorrect 
                ? 'bg-green-900 border border-green-600' 
                : 'bg-red-900 border border-red-600'
            }`}>
              <div className="flex items-center space-x-2">
                {submitResult.isCorrect ? (
                  <CheckCircle className="h-5 w-5 text-green-400" />
                ) : (
                  <XCircle className="h-5 w-5 text-red-400" />
                )}
                <span className={`font-medium ${
                  submitResult.isCorrect ? 'text-green-300' : 'text-red-300'
                }`}>
                  {submitResult.message}
                </span>
              </div>
              {submitResult.correctAnswer && !submitResult.isCorrect && (
                <p className="text-sm text-red-300 mt-2">
                  正确答案是: {submitResult.correctAnswer}
                </p>
              )}
              {submitResult.score && (
                <p className="text-sm text-green-300 mt-2">
                  获得 {submitResult.score} 积分！
                </p>
              )}
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default ExerciseDetail