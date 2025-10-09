import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  ArrowLeft, 
  AlertCircle, 
  CheckCircle, 
  Trash2, 
  BookOpen,
  Filter,
  Search
} from 'lucide-react'
import * as knowledgeBaseService from '@/services/knowledgeBaseService'
import type { WrongQuestion, QuestionBank } from '@/services/knowledgeBaseService'

const KnowledgeWrongQuestions: React.FC = () => {
  const navigate = useNavigate()
  
  const [wrongQuestions, setWrongQuestions] = useState<WrongQuestion[]>([])
  const [banks, setBanks] = useState<QuestionBank[]>([])
  const [selectedBankId, setSelectedBankId] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [showMastered, setShowMastered] = useState(false)

  useEffect(() => {
    fetchData()
  }, [])

  useEffect(() => {
    if (selectedBankId !== null) {
      fetchWrongQuestions()
    }
  }, [selectedBankId])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [banksData, wrongQuestionsData] = await Promise.all([
        knowledgeBaseService.getQuestionBanks(),
        knowledgeBaseService.getWrongQuestions()
      ])
      setBanks(banksData)
      setWrongQuestions(wrongQuestionsData)
    } catch (error) {
      console.error('Failed to fetch data:', error)
      setError('加载数据失败')
    } finally {
      setLoading(false)
    }
  }

  const fetchWrongQuestions = async () => {
    try {
      const data = await knowledgeBaseService.getWrongQuestions(selectedBankId || undefined)
      setWrongQuestions(data)
    } catch (error) {
      console.error('Failed to fetch wrong questions:', error)
      setError('加载错题失败')
    }
  }

  const handleMasterQuestion = async (wrongQuestionId: number) => {
    try {
      await knowledgeBaseService.masterQuestion(wrongQuestionId)
      setWrongQuestions(prev => 
        prev.map(q => 
          q.id === wrongQuestionId 
            ? { ...q, is_mastered: true, mastered_at: new Date().toISOString() }
            : q
        )
      )
      alert('题目已标记为掌握')
    } catch (error) {
      console.error('Failed to master question:', error)
      alert('操作失败')
    }
  }

  const handleDeleteQuestion = async (wrongQuestionId: number) => {
    if (window.confirm('确定要删除这个错题吗？')) {
      try {
        await knowledgeBaseService.deleteWrongQuestion(wrongQuestionId)
        setWrongQuestions(prev => prev.filter(q => q.id !== wrongQuestionId))
        alert('错题删除成功')
      } catch (error) {
        console.error('Failed to delete wrong question:', error)
        alert('删除失败')
      }
    }
  }

  const filteredQuestions = wrongQuestions.filter(question => {
    const matchesSearch = question.question?.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         question.question?.answer.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesMastered = showMastered ? true : !question.is_mastered
    return matchesSearch && matchesMastered
  })

  const getQuestionTypeColor = (type: string) => {
    switch (type) {
      case '单选题': return 'bg-blue-100 text-blue-800'
      case '多选题': return 'bg-green-100 text-green-800'
      case '判断题': return 'bg-yellow-100 text-yellow-800'
      case '填空题': return 'bg-purple-100 text-purple-800'
      case '问答题': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case '简单': return 'bg-green-100 text-green-800'
      case '中等': return 'bg-yellow-100 text-yellow-800'
      case '困难': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
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
          onClick={fetchData} 
          className="btn btn-primary"
        >
          重试
        </button>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* 头部 */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center">
            <button
              onClick={() => navigate('/knowledge')}
              className="mr-4 p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center">
                <AlertCircle className="h-8 w-8 mr-3 text-red-600" />
                错题集
              </h1>
              <p className="text-lg text-gray-600 mt-2">
                复习错题，巩固知识点
              </p>
            </div>
          </div>
        </div>

        {/* 筛选和搜索 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                选择题库
              </label>
              <select
                value={selectedBankId || ''}
                onChange={(e) => setSelectedBankId(e.target.value ? parseInt(e.target.value) : null)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">全部题库</option>
                {banks.map(bank => (
                  <option key={bank.id} value={bank.id}>
                    {bank.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                搜索题目
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="搜索题目内容或答案"
                  className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                显示选项
              </label>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="showMastered"
                  checked={showMastered}
                  onChange={(e) => setShowMastered(e.target.checked)}
                  className="mr-2"
                />
                <label htmlFor="showMastered" className="text-sm text-gray-700">
                  显示已掌握的题目
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* 统计信息 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-red-200 p-6">
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <AlertCircle className="h-6 w-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">总错题数</p>
                <p className="text-2xl font-bold text-gray-900">
                  {wrongQuestions.filter(q => !q.is_mastered).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-green-200 p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">已掌握</p>
                <p className="text-2xl font-bold text-gray-900">
                  {wrongQuestions.filter(q => q.is_mastered).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-blue-200 p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <BookOpen className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">掌握率</p>
                <p className="text-2xl font-bold text-gray-900">
                  {wrongQuestions.length > 0 
                    ? ((wrongQuestions.filter(q => q.is_mastered).length / wrongQuestions.length) * 100).toFixed(1)
                    : 0}%
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* 错题列表 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              错题列表 ({filteredQuestions.length})
            </h2>
          </div>
          
          {filteredQuestions.length === 0 ? (
            <div className="text-center py-12">
              <BookOpen className="h-12 w-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500 mb-4">
                {wrongQuestions.length === 0 ? '还没有错题' : '没有找到匹配的错题'}
              </p>
              {wrongQuestions.length === 0 && (
                <button
                  onClick={() => navigate('/knowledge')}
                  className="btn btn-primary"
                >
                  去刷题
                </button>
              )}
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredQuestions.map((wrongQuestion) => (
                <div key={wrongQuestion.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-3">
                        <span className={`px-2 py-1 text-xs rounded-full mr-2 ${getQuestionTypeColor(wrongQuestion.question?.type || '')}`}>
                          {wrongQuestion.question?.type}
                        </span>
                        <span className={`px-2 py-1 text-xs rounded-full mr-2 ${getDifficultyColor(wrongQuestion.question?.difficulty || '')}`}>
                          {wrongQuestion.question?.difficulty}
                        </span>
                        <span className="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800 mr-2">
                          {wrongQuestion.question?.score}分
                        </span>
                        {wrongQuestion.is_mastered && (
                          <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                            已掌握
                          </span>
                        )}
                        <span className="text-sm text-gray-500 ml-auto">
                          错误 {wrongQuestion.wrong_count} 次
                        </span>
                      </div>
                      
                      <h3 className="text-lg font-medium text-gray-900 mb-3">
                        {wrongQuestion.question?.question}
                      </h3>
                      
                      {wrongQuestion.question?.options && wrongQuestion.question.options.length > 0 && (
                        <div className="text-sm text-gray-600 mb-3">
                          {wrongQuestion.question.options.map((option, idx) => (
                            <div key={idx} className="mb-1">
                              {String.fromCharCode(65 + idx)}. {option}
                            </div>
                          ))}
                        </div>
                      )}
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-medium text-red-600">你的答案：</span>
                          <span className="ml-2">{wrongQuestion.user_answer}</span>
                        </div>
                        <div>
                          <span className="font-medium text-green-600">正确答案：</span>
                          <span className="ml-2">{wrongQuestion.question?.answer}</span>
                        </div>
                      </div>
                      
                      {wrongQuestion.question?.explanation && (
                        <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                          <span className="font-medium text-blue-800">解析：</span>
                          <p className="mt-1 text-blue-700">{wrongQuestion.question.explanation}</p>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      {!wrongQuestion.is_mastered && (
                        <button
                          onClick={() => handleMasterQuestion(wrongQuestion.id)}
                          className="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors flex items-center"
                        >
                          <CheckCircle className="h-4 w-4 mr-1" />
                          掌握
                        </button>
                      )}
                      
                      <button
                        onClick={() => handleDeleteQuestion(wrongQuestion.id)}
                        className="px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors flex items-center"
                      >
                        <Trash2 className="h-4 w-4 mr-1" />
                        删除
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default KnowledgeWrongQuestions

