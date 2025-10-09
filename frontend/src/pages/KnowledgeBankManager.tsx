import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { 
  ArrowLeft, 
  Plus, 
  Edit, 
  Trash2, 
  Save, 
  X,
  BookOpen,
  AlertCircle
} from 'lucide-react'
import * as knowledgeBaseService from '@/services/knowledgeBaseService'
import type { QuestionBank, Question } from '@/services/knowledgeBaseService'

const KnowledgeBankManager: React.FC = () => {
  const { bankId } = useParams<{ bankId: string }>()
  const navigate = useNavigate()
  const isEdit = bankId !== 'new'
  
  console.log('KnowledgeBankManager render:', { bankId, isEdit })
  
  const [bank, setBank] = useState<QuestionBank | null>(null)
  const [questions, setQuestions] = useState<Question[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null)
  const [showQuestionForm, setShowQuestionForm] = useState(false)
  
  // 表单状态
  const [bankForm, setBankForm] = useState({
    name: '',
    description: ''
  })
  
  const [questionForm, setQuestionForm] = useState({
    type: '单选题',
    question: '',
    options: ['', '', '', ''],
    answer: '',
    explanation: '',
    score: 1,
    difficulty: '简单'
  })

  useEffect(() => {
    console.log('KnowledgeBankManager useEffect:', { bankId, isEdit })
    if (isEdit) {
      fetchBankData()
    } else {
      console.log('Setting loading to false for new bank')
      setLoading(false)
    }
  }, [bankId, isEdit])

  const fetchBankData = async () => {
    if (!bankId) return
    
    try {
      setLoading(true)
      const [bankData, questionsData] = await Promise.all([
        knowledgeBaseService.getQuestionBank(parseInt(bankId)),
        knowledgeBaseService.getQuestions(parseInt(bankId))
      ])
      setBank(bankData)
      setQuestions(questionsData)
      setBankForm({
        name: bankData.name,
        description: bankData.description || ''
      })
    } catch (error) {
      console.error('Failed to fetch bank data:', error)
      setError('加载数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleSaveBank = async () => {
    try {
      if (isEdit) {
        await knowledgeBaseService.updateQuestionBank(parseInt(bankId!), bankForm)
        alert('题库更新成功')
      } else {
        const newBank = await knowledgeBaseService.createQuestionBank(bankForm)
        navigate(`/knowledge/banks/${newBank.id}/edit`)
      }
    } catch (error) {
      console.error('Failed to save bank:', error)
      alert('保存失败')
    }
  }

  const handleAddQuestion = () => {
    setEditingQuestion(null)
    setQuestionForm({
      type: '单选题',
      question: '',
      options: ['', '', '', ''],
      answer: '',
      explanation: '',
      score: 1,
      difficulty: '简单'
    })
    setShowQuestionForm(true)
  }

  const handleEditQuestion = (question: Question) => {
    setEditingQuestion(question)
    setQuestionForm({
      type: question.type,
      question: question.question,
      options: question.options || ['', '', '', ''],
      answer: question.answer,
      explanation: question.explanation || '',
      score: question.score,
      difficulty: question.difficulty
    })
    setShowQuestionForm(true)
  }

  const handleSaveQuestion = async () => {
    try {
      const questionData = {
        type: questionForm.type,
        question: questionForm.question,
        options: questionForm.type === '填空题' || questionForm.type === '问答题' 
          ? undefined 
          : questionForm.options.filter(opt => opt.trim() !== ''),
        answer: questionForm.answer,
        explanation: questionForm.explanation,
        score: questionForm.score,
        difficulty: questionForm.difficulty
      }

      if (editingQuestion) {
        await knowledgeBaseService.updateQuestion(editingQuestion.id, questionData)
        alert('题目更新成功')
      } else {
        await knowledgeBaseService.createQuestion(parseInt(bankId!), questionData)
        alert('题目添加成功')
      }
      
      setShowQuestionForm(false)
      fetchBankData()
    } catch (error) {
      console.error('Failed to save question:', error)
      alert('保存失败')
    }
  }

  const handleDeleteQuestion = async (questionId: number) => {
    if (window.confirm('确定要删除这个题目吗？')) {
      try {
        await knowledgeBaseService.deleteQuestion(questionId)
        setQuestions(questions.filter(q => q.id !== questionId))
        alert('题目删除成功')
      } catch (error) {
        console.error('Failed to delete question:', error)
        alert('删除失败')
      }
    }
  }

  const handleOptionChange = (index: number, value: string) => {
    const newOptions = [...questionForm.options]
    newOptions[index] = value
    setQuestionForm({ ...questionForm, options: newOptions })
  }

  const getAnswerOptions = () => {
    if (questionForm.type === '单选题' || questionForm.type === '多选题') {
      return questionForm.options.map((_, index) => String.fromCharCode(65 + index))
    } else if (questionForm.type === '判断题') {
      return ['正确', '错误']
    }
    return []
  }

  if (loading) {
    console.log('KnowledgeBankManager loading state:', { loading, bankId, isEdit })
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="ml-4">Loading... bankId: {bankId}, isEdit: {isEdit.toString()}</p>
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
            <h1 className="text-3xl font-bold text-gray-900">
              {isEdit ? '编辑题库' : '新建题库'}
            </h1>
          </div>
          <button
            onClick={handleSaveBank}
            className="btn btn-primary flex items-center"
          >
            <Save className="h-4 w-4 mr-2" />
            保存题库
          </button>
        </div>

        {/* 题库信息表单 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">题库信息</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                题库名称 *
              </label>
              <input
                type="text"
                value={bankForm.name}
                onChange={(e) => setBankForm({ ...bankForm, name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入题库名称"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                难度等级
              </label>
              <select
                value={bankForm.description}
                onChange={(e) => setBankForm({ ...bankForm, description: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">选择难度等级</option>
                <option value="初级">初级</option>
                <option value="中级">中级</option>
                <option value="高级">高级</option>
                <option value="专家">专家</option>
              </select>
            </div>
          </div>
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              题库描述
            </label>
            <textarea
              value={bankForm.description}
              onChange={(e) => setBankForm({ ...bankForm, description: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="请输入题库描述"
            />
          </div>
        </div>

        {/* 题目列表 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">题目列表</h2>
            <button
              onClick={handleAddQuestion}
              className="btn btn-primary flex items-center"
            >
              <Plus className="h-4 w-4 mr-2" />
              添加题目
            </button>
          </div>
          
          {questions.length === 0 ? (
            <div className="text-center py-12">
              <BookOpen className="h-12 w-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500 mb-4">还没有题目，点击上方按钮添加第一个题目吧！</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {questions.map((question, index) => (
                <div key={question.id} className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <span className="text-sm font-medium text-gray-500 mr-4">
                          第 {index + 1} 题
                        </span>
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                          {question.type}
                        </span>
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full ml-2">
                          {question.difficulty}
                        </span>
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full ml-2">
                          {question.score}分
                        </span>
                      </div>
                      <p className="text-gray-900 mb-2">{question.question}</p>
                      {question.options && question.options.length > 0 && (
                        <div className="text-sm text-gray-600 mb-2">
                          {question.options.map((option, idx) => (
                            <div key={idx}>
                              {String.fromCharCode(65 + idx)}. {option}
                            </div>
                          ))}
                        </div>
                      )}
                      <p className="text-sm text-green-600">
                        答案: {question.answer}
                      </p>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => handleEditQuestion(question)}
                        className="p-2 text-yellow-600 hover:bg-yellow-100 rounded-lg transition-colors"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteQuestion(question.id)}
                        className="p-2 text-red-600 hover:bg-red-100 rounded-lg transition-colors"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 题目编辑表单模态框 */}
        {showQuestionForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">
                  {editingQuestion ? '编辑题目' : '添加题目'}
                </h3>
                <button
                  onClick={() => setShowQuestionForm(false)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      题型 *
                    </label>
                    <select
                      value={questionForm.type}
                      onChange={(e) => setQuestionForm({ ...questionForm, type: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="单选题">单选题</option>
                      <option value="多选题">多选题</option>
                      <option value="判断题">判断题</option>
                      <option value="填空题">填空题</option>
                      <option value="问答题">问答题</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      难度 *
                    </label>
                    <select
                      value={questionForm.difficulty}
                      onChange={(e) => setQuestionForm({ ...questionForm, difficulty: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="简单">简单</option>
                      <option value="中等">中等</option>
                      <option value="困难">困难</option>
                    </select>
                  </div>
                </div>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    题目内容 *
                  </label>
                  <textarea
                    value={questionForm.question}
                    onChange={(e) => setQuestionForm({ ...questionForm, question: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                    placeholder="请输入题目内容"
                  />
                </div>
                
                {(questionForm.type === '单选题' || questionForm.type === '多选题') && (
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      选项 *
                    </label>
                    {questionForm.options.map((option, index) => (
                      <div key={index} className="flex items-center mb-2">
                        <span className="w-8 text-sm font-medium text-gray-700">
                          {String.fromCharCode(65 + index)}.
                        </span>
                        <input
                          type="text"
                          value={option}
                          onChange={(e) => handleOptionChange(index, e.target.value)}
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                          placeholder={`选项 ${String.fromCharCode(65 + index)}`}
                        />
                      </div>
                    ))}
                  </div>
                )}
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    正确答案 *
                  </label>
                  {questionForm.type === '单选题' || questionForm.type === '多选题' ? (
                    <div className="flex flex-wrap gap-2">
                      {getAnswerOptions().map((option) => (
                        <label key={option} className="flex items-center">
                          <input
                            type={questionForm.type === '单选题' ? 'radio' : 'checkbox'}
                            name="answer"
                            value={option}
                            checked={questionForm.answer.includes(option)}
                            onChange={(e) => {
                              if (questionForm.type === '单选题') {
                                setQuestionForm({ ...questionForm, answer: option })
                              } else {
                                const currentAnswers = questionForm.answer.split(',').filter(a => a.trim())
                                if (e.target.checked) {
                                  currentAnswers.push(option)
                                } else {
                                  const index = currentAnswers.indexOf(option)
                                  if (index > -1) currentAnswers.splice(index, 1)
                                }
                                setQuestionForm({ ...questionForm, answer: currentAnswers.join(',') })
                              }
                            }}
                            className="mr-2"
                          />
                          {option}
                        </label>
                      ))}
                    </div>
                  ) : (
                    <input
                      type="text"
                      value={questionForm.answer}
                      onChange={(e) => setQuestionForm({ ...questionForm, answer: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="请输入正确答案"
                    />
                  )}
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      分值
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="10"
                      value={questionForm.score}
                      onChange={(e) => setQuestionForm({ ...questionForm, score: parseInt(e.target.value) })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    解析
                  </label>
                  <textarea
                    value={questionForm.explanation}
                    onChange={(e) => setQuestionForm({ ...questionForm, explanation: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                    placeholder="请输入题目解析（可选）"
                  />
                </div>
              </div>
              
              <div className="px-6 py-4 border-t border-gray-200 flex justify-end space-x-3">
                <button
                  onClick={() => setShowQuestionForm(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
                >
                  取消
                </button>
                <button
                  onClick={handleSaveQuestion}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  保存
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default KnowledgeBankManager

