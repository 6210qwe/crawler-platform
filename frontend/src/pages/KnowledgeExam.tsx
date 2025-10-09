import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  ArrowLeft, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Play, 
  Pause,
  ChevronRight,
  ChevronLeft,
  Flag
} from 'lucide-react'
import * as knowledgeBaseService from '@/services/knowledgeBaseService'
import type { Question, ExamSession, UserAnswer } from '@/services/knowledgeBaseService'

const KnowledgeExam: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>()
  const navigate = useNavigate()
  
  const [session, setSession] = useState<ExamSession | null>(null)
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [userAnswers, setUserAnswers] = useState<{ [key: number]: string }>({})
  const [timeSpent, setTimeSpent] = useState(0)
  const [isTimerRunning, setIsTimerRunning] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [lastAnswer, setLastAnswer] = useState<UserAnswer | null>(null)
  
  const isExam = session?.exam_type === 'exam'
  const currentQuestion = questions[currentIndex]
  const isLastQuestion = currentIndex === questions.length - 1
  const isFirstQuestion = currentIndex === 0

  useEffect(() => {
    if (sessionId) {
      fetchData()
    }
  }, [sessionId])

  useEffect(() => {
    let interval: NodeJS.Timeout
    if (isTimerRunning) {
      interval = setInterval(() => {
        setTimeSpent(prev => prev + 1)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [isTimerRunning])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [sessionData, questionsData] = await Promise.all([
        knowledgeBaseService.getExamSession(sessionId!),
        knowledgeBaseService.getSessionQuestions(sessionId!)
      ])
      setSession(sessionData)
      setQuestions(questionsData)
      setIsTimerRunning(true)
    } catch (error) {
      console.error('Failed to fetch data:', error)
      setError('加载数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerChange = (answer: string) => {
    if (currentQuestion) {
      setUserAnswers(prev => ({
        ...prev,
        [currentQuestion.id]: answer
      }))
    }
  }

  const handleSubmitAnswer = async () => {
    if (!currentQuestion || !sessionId) return
    
    const answer = userAnswers[currentQuestion.id] || ''
    if (!answer.trim()) {
      alert('请先选择答案')
      return
    }

    try {
      const result = await knowledgeBaseService.submitAnswer(sessionId, {
        question_id: currentQuestion.id,
        answer: answer,
        time_spent: timeSpent
      })
      
      setLastAnswer(result)
      setTimeSpent(0) // 重置当前题目计时
      
      if (isExam) {
        // 考试模式：自动进入下一题
        if (!isLastQuestion) {
          setCurrentIndex(prev => prev + 1)
        } else {
          // 最后一题，完成考试
          await handleCompleteExam()
        }
      } else {
        // 刷题模式：显示答案反馈
        setShowResult(true)
      }
    } catch (error) {
      console.error('Failed to submit answer:', error)
      alert('提交答案失败')
    }
  }

  const handleNextQuestion = () => {
    if (!isLastQuestion) {
      setCurrentIndex(prev => prev + 1)
      setShowResult(false)
      setLastAnswer(null)
    }
  }

  const handlePrevQuestion = () => {
    if (!isFirstQuestion) {
      setCurrentIndex(prev => prev - 1)
      setShowResult(false)
      setLastAnswer(null)
    }
  }

  const handleCompleteExam = async () => {
    if (!sessionId) return
    
    try {
      setIsTimerRunning(false)
      const result = await knowledgeBaseService.completeExam(sessionId)
      navigate(`/knowledge/exam/result/${sessionId}`, { state: { result } })
    } catch (error) {
      console.error('Failed to complete exam:', error)
      alert('完成考试失败')
    }
  }

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const getAnswerOptions = () => {
    if (!currentQuestion) return []
    
    if (currentQuestion.type === '单选题' || currentQuestion.type === '多选题') {
      return currentQuestion.options?.map((option, index) => ({
        value: String.fromCharCode(65 + index),
        label: `${String.fromCharCode(65 + index)}. ${option}`
      })) || []
    } else if (currentQuestion.type === '判断题') {
      return [
        { value: '正确', label: '正确' },
        { value: '错误', label: '错误' }
      ]
    }
    return []
  }

  const renderQuestionContent = () => {
    if (!currentQuestion) return null

    const currentAnswer = userAnswers[currentQuestion.id] || ''
    const options = getAnswerOptions()

    return (
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {currentQuestion.question}
          </h2>
        </div>

        {currentQuestion.type === '单选题' && (
          <div className="space-y-3">
            {options.map((option) => (
              <label key={option.value} className="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                <input
                  type="radio"
                  name={`question_${currentQuestion.id}`}
                  value={option.value}
                  checked={currentAnswer === option.value}
                  onChange={(e) => handleAnswerChange(e.target.value)}
                  className="mr-3"
                />
                <span>{option.label}</span>
              </label>
            ))}
          </div>
        )}

        {currentQuestion.type === '多选题' && (
          <div className="space-y-3">
            {options.map((option) => (
              <label key={option.value} className="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                <input
                  type="checkbox"
                  checked={currentAnswer.includes(option.value)}
                  onChange={(e) => {
                    const currentAnswers = currentAnswer.split(',').filter(a => a.trim())
                    if (e.target.checked) {
                      currentAnswers.push(option.value)
                    } else {
                      const index = currentAnswers.indexOf(option.value)
                      if (index > -1) currentAnswers.splice(index, 1)
                    }
                    handleAnswerChange(currentAnswers.join(','))
                  }}
                  className="mr-3"
                />
                <span>{option.label}</span>
              </label>
            ))}
          </div>
        )}

        {currentQuestion.type === '判断题' && (
          <div className="space-y-3">
            {options.map((option) => (
              <label key={option.value} className="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                <input
                  type="radio"
                  name={`question_${currentQuestion.id}`}
                  value={option.value}
                  checked={currentAnswer === option.value}
                  onChange={(e) => handleAnswerChange(e.target.value)}
                  className="mr-3"
                />
                <span>{option.label}</span>
              </label>
            ))}
          </div>
        )}

        {(currentQuestion.type === '填空题' || currentQuestion.type === '问答题') && (
          <div>
            <textarea
              value={currentAnswer}
              onChange={(e) => handleAnswerChange(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={currentQuestion.type === '问答题' ? 6 : 3}
              placeholder={currentQuestion.type === '填空题' ? '请输入答案' : '请详细回答'}
            />
          </div>
        )}
      </div>
    )
  }

  if (loading) {
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
          onClick={() => navigate('/knowledge')} 
          className="btn btn-primary"
        >
          返回
        </button>
      </div>
    )
  }

  if (!session || !currentQuestion) {
    return (
      <div className="text-center py-12 text-gray-600">
        <p className="text-lg">没有找到题目</p>
        <button 
          onClick={() => navigate('/knowledge')} 
          className="btn btn-primary mt-4"
        >
          返回
        </button>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* 头部信息 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => navigate('/knowledge')}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                第 {currentIndex + 1} 题 / 共 {questions.length} 题
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <Clock className="h-4 w-4 mr-1" />
                {formatTime(timeSpent)}
              </div>
            </div>
          </div>
          
          {/* 进度条 */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>

        {/* 题目内容 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                {currentQuestion.type}
              </span>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                {currentQuestion.difficulty}
              </span>
              <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-sm rounded-full">
                {currentQuestion.score}分
              </span>
            </div>
          </div>
          
          {renderQuestionContent()}
        </div>

        {/* 答案反馈（刷题模式） */}
        {showResult && lastAnswer && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <div className={`flex items-center mb-4 ${
              lastAnswer.is_correct ? 'text-green-600' : 'text-red-600'
            }`}>
              {lastAnswer.is_correct ? (
                <CheckCircle className="h-6 w-6 mr-2" />
              ) : (
                <XCircle className="h-6 w-6 mr-2" />
              )}
              <span className="text-lg font-semibold">
                {lastAnswer.is_correct ? '回答正确！' : '回答错误'}
              </span>
            </div>
            
            <div className="space-y-3">
              <div>
                <span className="font-medium text-gray-700">你的答案：</span>
                <span className="ml-2">{lastAnswer.answer}</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">正确答案：</span>
                <span className="ml-2 text-green-600">{currentQuestion.answer}</span>
              </div>
              {currentQuestion.explanation && (
                <div>
                  <span className="font-medium text-gray-700">解析：</span>
                  <p className="mt-1 text-gray-600">{currentQuestion.explanation}</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* 操作按钮 */}
        <div className="flex items-center justify-between">
          <div className="flex space-x-3">
            <button
              onClick={handlePrevQuestion}
              disabled={isFirstQuestion}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              上一题
            </button>
            
            <button
              onClick={handleNextQuestion}
              disabled={isLastQuestion}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              下一题
              <ChevronRight className="h-4 w-4 ml-1" />
            </button>
          </div>
          
          <div className="flex space-x-3">
            {isExam ? (
              <button
                onClick={handleCompleteExam}
                className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center"
              >
                <Flag className="h-4 w-4 mr-1" />
                交卷
              </button>
            ) : (
              <button
                onClick={handleSubmitAnswer}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center"
              >
                <CheckCircle className="h-4 w-4 mr-1" />
                提交答案
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default KnowledgeExam
