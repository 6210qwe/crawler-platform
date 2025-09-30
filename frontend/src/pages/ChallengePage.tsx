import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { ArrowLeft, Calculator, Clock, Target, Trophy, CheckCircle, XCircle, AlertCircle, Play, Pause, RotateCcw } from 'lucide-react'
import * as challengeService from '@/services/challengeService'
import { ChallengeData } from '@/services/challengeService'

const ChallengePage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user, loading: authLoading } = useAuth()
  const [challengeData, setChallengeData] = useState<ChallengeData | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [pageData, setPageData] = useState<{
    pageNumber: number
    numbers: number[]
    startIndex: number
    endIndex: number
  } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
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
  const [selectedNumbers, setSelectedNumbers] = useState<number[]>([])

  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login')
      return
    }
  }, [user, authLoading, navigate])

  useEffect(() => {
    const fetchChallengeData = async () => {
      if (!id || !user) return
      
      setLoading(true)
      try {
        const data = await challengeService.getChallengeData(parseInt(id))
        setChallengeData(data)
        setPageData({
          pageNumber: 1,
          numbers: data.numbers[0],
          startIndex: 1,
          endIndex: 10
        })
        setIsTimerRunning(true)
      } catch (error) {
        console.error('Failed to fetch challenge data:', error)
        setError('加载挑战数据失败')
      } finally {
        setLoading(false)
      }
    }

    fetchChallengeData()
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

  const handlePageChange = (page: number) => {
    if (!challengeData) return
    
    setCurrentPage(page)
    setPageData({
      pageNumber: page,
      numbers: challengeData.numbers[page - 1],
      startIndex: (page - 1) * 10 + 1,
      endIndex: page * 10
    })
    setSelectedNumbers([])
    setUserAnswer('')
    setSubmitResult(null)
  }

  const handleNumberClick = (number: number) => {
    setSelectedNumbers(prev => {
      if (prev.includes(number)) {
        return prev.filter(n => n !== number)
      } else {
        return [...prev, number]
      }
    })
  }

  const calculateSum = () => {
    const sum = selectedNumbers.reduce((acc, num) => acc + num, 0)
    setUserAnswer(sum.toString())
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
      
      if (result.success) {
        // 更新挑战数据
        if (challengeData) {
          setChallengeData({
            ...challengeData,
            isCompleted: true,
            completedAt: result.completedAt || new Date().toISOString()
          })
        }
      }
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

  const resetChallenge = () => {
    setUserAnswer('')
    setSelectedNumbers([])
    setSubmitResult(null)
    setTimeSpent(0)
    setIsTimerRunning(true)
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

  if (!challengeData || !pageData) {
    return (
      <div className="text-center py-12 text-gray-600">
        <AlertCircle className="h-12 w-12 mx-auto mb-4" />
        <p className="text-lg mb-4">挑战数据不存在</p>
        <button 
          onClick={() => navigate('/exercises')} 
          className="btn btn-primary"
        >
          返回题目列表
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* 头部信息 */}
      <div className="mb-8">
        <button 
          onClick={() => navigate('/exercises')} 
          className="text-blue-600 hover:text-blue-700 flex items-center space-x-2 mb-6"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>返回题目列表</span>
        </button>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">数字求和挑战</h1>
              <p className="text-gray-600">题目 #{id} - 计算1000个数字的总和</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{challengeData.totalSum}</div>
                <div className="text-sm text-gray-500">正确答案</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg">
              <Clock className="h-6 w-6 text-blue-500" />
              <div>
                <p className="text-sm text-gray-600">用时</p>
                <p className="text-xl font-bold text-gray-900">{formatTime(timeSpent)}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg">
              <Target className="h-6 w-6 text-green-500" />
              <div>
                <p className="text-sm text-gray-600">当前页</p>
                <p className="text-xl font-bold text-gray-900">{currentPage}/100</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-4 bg-yellow-50 rounded-lg">
              <Calculator className="h-6 w-6 text-yellow-500" />
              <div>
                <p className="text-sm text-gray-600">已选数字</p>
                <p className="text-xl font-bold text-gray-900">{selectedNumbers.length}</p>
              </div>
            </div>
            <div className="flex items-center space-x-3 p-4 bg-purple-50 rounded-lg">
              <Trophy className="h-6 w-6 text-purple-500" />
              <div>
                <p className="text-sm text-gray-600">状态</p>
                <p className="text-xl font-bold text-gray-900">
                  {challengeData.isCompleted ? '已完成' : '进行中'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* 数字网格 */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                第 {currentPage} 页 - 数字 {pageData.startIndex} 到 {pageData.endIndex}
              </h2>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setIsTimerRunning(!isTimerRunning)}
                  className="p-2 text-gray-600 hover:text-blue-600 transition-colors"
                >
                  {isTimerRunning ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5" />}
                </button>
                <button
                  onClick={resetChallenge}
                  className="p-2 text-gray-600 hover:text-red-600 transition-colors"
                >
                  <RotateCcw className="h-5 w-5" />
                </button>
              </div>
            </div>

            <div className="grid grid-cols-5 gap-4 mb-6">
              {pageData.numbers.map((number, index) => (
                <button
                  key={index}
                  onClick={() => handleNumberClick(number)}
                  className={`p-4 text-center rounded-lg border-2 transition-all ${
                    selectedNumbers.includes(number)
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="text-2xl font-bold">{number}</div>
                </button>
              ))}
            </div>

            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-600">
                已选择 {selectedNumbers.length} 个数字，当前页总和: {selectedNumbers.reduce((sum, num) => sum + num, 0)}
              </div>
              <button
                onClick={calculateSum}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                计算选中数字之和
              </button>
            </div>
          </div>
        </div>

        {/* 侧边栏 */}
        <div className="space-y-6">
          {/* 答案提交 */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">提交答案</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  你的答案
                </label>
                <input
                  type="number"
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="输入1000个数字的总和"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              {submitResult && (
                <div className={`p-4 rounded-lg ${
                  submitResult.isCorrect 
                    ? 'bg-green-50 border border-green-200' 
                    : 'bg-red-50 border border-red-200'
                }`}>
                  <div className="flex items-center space-x-2">
                    {submitResult.isCorrect ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-500" />
                    )}
                    <span className={`font-medium ${
                      submitResult.isCorrect ? 'text-green-800' : 'text-red-800'
                    }`}>
                      {submitResult.message}
                    </span>
                  </div>
                  {submitResult.correctAnswer && !submitResult.isCorrect && (
                    <p className="text-sm text-red-700 mt-2">
                      正确答案是: {submitResult.correctAnswer}
                    </p>
                  )}
                  {submitResult.score && (
                    <p className="text-sm text-green-700 mt-2">
                      获得 {submitResult.score} 积分！
                    </p>
                  )}
                </div>
              )}

              <button
                onClick={handleSubmit}
                disabled={isSubmitting || !userAnswer.trim() || challengeData.isCompleted}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmitting ? '提交中...' : challengeData.isCompleted ? '已完成' : '提交答案'}
              </button>
            </div>
          </div>

          {/* 页面导航 */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">页面导航</h3>
            <div className="grid grid-cols-10 gap-1 max-h-64 overflow-y-auto">
              {Array.from({ length: 100 }, (_, i) => (
                <button
                  key={i + 1}
                  onClick={() => handlePageChange(i + 1)}
                  className={`p-2 text-xs rounded ${
                    currentPage === i + 1
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {i + 1}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChallengePage
