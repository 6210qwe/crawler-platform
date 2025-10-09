import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Play, Target, Clock, BookOpen, AlertCircle } from 'lucide-react'
import * as knowledgeBaseService from '@/services/knowledgeBaseService'
import type { QuestionBank } from '@/services/knowledgeBaseService'

const KnowledgeExamSetup: React.FC = () => {
  const { bankId, type } = useParams<{ bankId: string; type: string }>()
  const navigate = useNavigate()
  const isExam = type === 'exam'
  
  const [bank, setBank] = useState<QuestionBank | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  
  // 考试设置
  const [examSettings, setExamSettings] = useState({
    total_questions: 10,
    single_ratio: 40,
    multi_ratio: 30,
    bool_ratio: 30,
    time_limit: 30
  })
  
  // 刷题设置
  const [practiceSettings, setPracticeSettings] = useState({
    order: '顺序'
  })

  useEffect(() => {
    if (bankId) {
      fetchBankData()
    }
  }, [bankId])

  const fetchBankData = async () => {
    try {
      setLoading(true)
      const bankData = await knowledgeBaseService.getQuestionBank(parseInt(bankId!))
      setBank(bankData)
    } catch (error) {
      console.error('Failed to fetch bank data:', error)
      setError('加载题库数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleStart = async () => {
    try {
      if (isExam) {
        const session = await knowledgeBaseService.setupExam({
          bank_id: parseInt(bankId!),
          ...examSettings
        })
        navigate(`/knowledge/exam/${session.session_id}`)
      } else {
        const session = await knowledgeBaseService.setupPractice({
          bank_id: parseInt(bankId!),
          ...practiceSettings
        })
        navigate(`/knowledge/practice/${session.session_id}`)
      }
    } catch (error) {
      console.error('Failed to start:', error)
      alert('启动失败，请重试')
    }
  }

  const validateSettings = () => {
    if (isExam) {
      const totalRatio = examSettings.single_ratio + examSettings.multi_ratio + examSettings.bool_ratio
      if (totalRatio !== 100) {
        alert('题型比例总和必须为100%')
        return false
      }
      if (examSettings.total_questions < 1 || examSettings.total_questions > 100) {
        alert('题目数量必须在1-100之间')
        return false
      }
    }
    return true
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
        <AlertCircle className="h-12 w-12 mx-auto mb-4" />
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* 头部 */}
        <div className="flex items-center mb-8">
          <button
            onClick={() => navigate('/knowledge')}
            className="mr-4 p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              {isExam ? (
                <>
                  <Play className="h-8 w-8 mr-3 text-blue-600" />
                  考试设置
                </>
              ) : (
                <>
                  <Target className="h-8 w-8 mr-3 text-green-600" />
                  刷题设置
                </>
              )}
            </h1>
            {bank && (
              <p className="text-lg text-gray-600 mt-2">
                题库: {bank.name} ({bank.question_count || 0} 题)
              </p>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          {isExam ? (
            // 考试设置表单
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-6">考试参数设置</h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    题目数量
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="100"
                    value={examSettings.total_questions}
                    onChange={(e) => setExamSettings({
                      ...examSettings,
                      total_questions: parseInt(e.target.value) || 1
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-3">
                    题型分布
                  </label>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm text-gray-600 mb-1">单选题</label>
                      <div className="flex items-center">
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={examSettings.single_ratio}
                          onChange={(e) => setExamSettings({
                            ...examSettings,
                            single_ratio: parseInt(e.target.value) || 0
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-600">%</span>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm text-gray-600 mb-1">多选题</label>
                      <div className="flex items-center">
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={examSettings.multi_ratio}
                          onChange={(e) => setExamSettings({
                            ...examSettings,
                            multi_ratio: parseInt(e.target.value) || 0
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-600">%</span>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm text-gray-600 mb-1">判断题</label>
                      <div className="flex items-center">
                        <input
                          type="number"
                          min="0"
                          max="100"
                          value={examSettings.bool_ratio}
                          onChange={(e) => setExamSettings({
                            ...examSettings,
                            bool_ratio: parseInt(e.target.value) || 0
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <span className="ml-2 text-sm text-gray-600">%</span>
                      </div>
                    </div>
                  </div>
                  <p className="text-sm text-gray-500 mt-2">
                    当前比例总和: {examSettings.single_ratio + examSettings.multi_ratio + examSettings.bool_ratio}%
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    时间限制（分钟）
                  </label>
                  <div className="flex items-center">
                    <Clock className="h-5 w-5 text-gray-400 mr-2" />
                    <input
                      type="number"
                      min="1"
                      max="300"
                      value={examSettings.time_limit}
                      onChange={(e) => setExamSettings({
                        ...examSettings,
                        time_limit: parseInt(e.target.value) || 30
                      })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          ) : (
            // 刷题设置表单
            <div>
              <h2 className="text-xl font-semibold text-gray-900 mb-6">刷题参数设置</h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    刷题顺序
                  </label>
                  <select
                    value={practiceSettings.order}
                    onChange={(e) => setPracticeSettings({
                      ...practiceSettings,
                      order: e.target.value
                    })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="顺序">顺序刷题</option>
                    <option value="逆序">逆序刷题</option>
                    <option value="随机">随机刷题</option>
                  </select>
                  <p className="text-sm text-gray-500 mt-2">
                    选择题目出现的顺序，随机模式会打乱题目顺序
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* 操作按钮 */}
          <div className="mt-8 flex justify-center space-x-4">
            <button
              onClick={() => navigate('/knowledge')}
              className="px-6 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              取消
            </button>
            <button
              onClick={() => {
                if (validateSettings()) {
                  handleStart()
                }
              }}
              className={`px-8 py-3 text-white rounded-lg transition-colors flex items-center ${
                isExam 
                  ? 'bg-blue-600 hover:bg-blue-700' 
                  : 'bg-green-600 hover:bg-green-700'
              }`}
            >
              {isExam ? (
                <>
                  <Play className="h-5 w-5 mr-2" />
                  开始考试
                </>
              ) : (
                <>
                  <Target className="h-5 w-5 mr-2" />
                  开始刷题
                </>
              )}
            </button>
          </div>
        </div>

        {/* 说明信息 */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3 flex items-center">
            <BookOpen className="h-5 w-5 mr-2" />
            {isExam ? '考试说明' : '刷题说明'}
          </h3>
          <div className="text-blue-800 space-y-2">
            {isExam ? (
              <>
                <p>• 考试采用计时模式，时间到后自动交卷</p>
                <p>• 可以随时查看剩余时间</p>
                <p>• 支持单选题、多选题、判断题三种题型</p>
                <p>• 考试结束后会显示详细成绩和错题分析</p>
                <p>• 错题会自动加入错题集，方便后续复习</p>
              </>
            ) : (
              <>
                <p>• 刷题模式没有时间限制，可以慢慢思考</p>
                <p>• 每道题提交后立即显示正确答案和解析</p>
                <p>• 支持所有题型，包括填空题和问答题</p>
                <p>• 答错的题目会自动加入错题集</p>
                <p>• 可以随时暂停和继续刷题</p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default KnowledgeExamSetup

