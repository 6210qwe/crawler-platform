import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { exerciseService, Exercise, ExerciseSubmission } from '../services/exerciseService'
import { Clock, Star, Target, ArrowLeft, CheckCircle, XCircle, AlertCircle } from 'lucide-react'

const ExerciseDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [exercise, setExercise] = useState<Exercise | null>(null)
  const [submission, setSubmission] = useState<ExerciseSubmission | null>(null)
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [timeLeft, setTimeLeft] = useState(0)
  const [timerActive, setTimerActive] = useState(false)

  useEffect(() => {
    const fetchExercise = async () => {
      if (!id) return
      
      try {
        const data = await exerciseService.getExercise(parseInt(id))
        setExercise(data)
        setTimeLeft(data.time_limit)
      } catch (error) {
        console.error('Failed to fetch exercise:', error)
        setError('练习题加载失败')
      } finally {
        setLoading(false)
      }
    }

    fetchExercise()
  }, [id])

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null

    if (timerActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((time) => time - 1)
      }, 1000)
    } else if (timeLeft === 0) {
      setTimerActive(false)
      handleSubmit()
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [timerActive, timeLeft])

  const startTimer = () => {
    setTimerActive(true)
  }

  const handleSubmit = async () => {
    if (!exercise || !answer.trim()) return

    setSubmitting(true)
    setError('')

    try {
      const result = await exerciseService.submitExercise(exercise.id, { answer })
      setSubmission(result)
      setTimerActive(false)
    } catch (err: any) {
      setError(err.response?.data?.detail || '提交失败，请重试')
    } finally {
      setSubmitting(false)
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'bg-green-100 text-green-800'
      case 'intermediate':
        return 'bg-lime-100 text-lime-800'
      case 'advanced':
        return 'bg-yellow-100 text-yellow-800'
      case 'hard':
        return 'bg-red-100 text-red-800'
      case 'hell':
        return 'bg-orange-100 text-orange-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getDifficultyText = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return '初级'
      case 'intermediate':
        return '中级'
      case 'advanced':
        return '高级'
      case 'hard':
        return '困难'
      case 'hell':
        return '地狱'
      default:
        return difficulty
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'correct':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'incorrect':
        return <XCircle className="h-5 w-5 text-red-500" />
      case 'timeout':
        return <AlertCircle className="h-5 w-5 text-yellow-500" />
      default:
        return <Clock className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'correct':
        return '正确'
      case 'incorrect':
        return '错误'
      case 'timeout':
        return '超时'
      default:
        return '待评判'
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!exercise) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">练习题不存在</p>
        <button
          onClick={() => navigate('/exercises')}
          className="btn btn-primary btn-sm mt-4"
        >
          返回练习题列表
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* 返回按钮 */}
      <button
        onClick={() => navigate('/exercises')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="h-4 w-4" />
        <span>返回练习题列表</span>
      </button>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* 左侧：题目信息 */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="card-header">
              <div className="flex items-start justify-between mb-4">
                <h1 className="card-title text-2xl">{exercise.title}</h1>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(exercise.difficulty)}`}>
                  {getDifficultyText(exercise.difficulty)}
                </span>
              </div>
              
              <div className="flex items-center space-x-6 text-sm text-gray-500 mb-4">
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4" />
                  <span>{exercise.points} 分</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span>{exercise.time_limit} 秒</span>
                </div>
              </div>
            </div>

            <div className="card-content">
              <div className="prose max-w-none">
                <h3 className="text-lg font-semibold mb-3">题目描述</h3>
                <div className="whitespace-pre-wrap text-gray-700 mb-6">
                  {exercise.description}
                </div>

                <h3 className="text-lg font-semibold mb-3">目标网站</h3>
                <div className="bg-gray-50 p-4 rounded-lg mb-6">
                  <a
                    href={exercise.target_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary-600 hover:text-primary-700 break-all"
                  >
                    {exercise.target_url}
                  </a>
                </div>

                {exercise.hints && (
                  <>
                    <h3 className="text-lg font-semibold mb-3">提示</h3>
                    <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg mb-6">
                      <div className="whitespace-pre-wrap text-gray-700">
                        {exercise.hints}
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* 右侧：答题区域 */}
        <div className="lg:col-span-1">
          <div className="card sticky top-6">
            <div className="card-header">
              <h3 className="card-title text-lg">提交答案</h3>
            </div>

            <div className="card-content">
              {submission ? (
                <div className="text-center">
                  <div className="mb-4">
                    {getStatusIcon(submission.status)}
                  </div>
                  <h4 className="text-lg font-semibold mb-2">
                    {getStatusText(submission.status)}
                  </h4>
                  <p className="text-gray-600 mb-4">
                    得分: {submission.score} / {exercise.points}
                  </p>
                  <p className="text-sm text-gray-500">
                    提交时间: {new Date(submission.submitted_at).toLocaleString()}
                  </p>
                </div>
              ) : (
                <>
                  {timerActive && (
                    <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                      <div className="flex items-center justify-center space-x-2">
                        <Clock className="h-4 w-4 text-red-500" />
                        <span className="text-red-700 font-medium">
                          剩余时间: {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}
                        </span>
                      </div>
                    </div>
                  )}

                  {error && (
                    <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                      <p className="text-red-700 text-sm">{error}</p>
                    </div>
                  )}

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        你的答案
                      </label>
                      <textarea
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        placeholder="请输入你的答案..."
                        className="input min-h-[120px] resize-none"
                        disabled={submitting}
                      />
                    </div>

                    <div className="flex space-x-3">
                      {!timerActive && (
                        <button
                          onClick={startTimer}
                          className="btn btn-secondary btn-sm flex-1"
                        >
                          开始计时
                        </button>
                      )}
                      <button
                        onClick={handleSubmit}
                        disabled={submitting || !answer.trim() || timerActive}
                        className="btn btn-primary btn-sm flex-1"
                      >
                        {submitting ? (
                          <div className="flex items-center justify-center">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            提交中...
                          </div>
                        ) : (
                          '提交答案'
                        )}
                      </button>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ExerciseDetail

