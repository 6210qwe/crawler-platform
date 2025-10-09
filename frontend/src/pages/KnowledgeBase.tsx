import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  BookOpen, 
  Plus, 
  Edit, 
  Trash2, 
  Play, 
  BarChart3, 
  AlertCircle,
  CheckCircle,
  Clock,
  Target
} from 'lucide-react'
import * as knowledgeBaseService from '@/services/knowledgeBaseService'
import type { QuestionBank, StudyStatsSummary } from '@/services/knowledgeBaseService'

const KnowledgeBase: React.FC = () => {
  const navigate = useNavigate()
  const [banks, setBanks] = useState<QuestionBank[]>([])
  const [stats, setStats] = useState<StudyStatsSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [banksData, statsData] = await Promise.all([
        knowledgeBaseService.getQuestionBanks(),
        knowledgeBaseService.getStudyStats()
      ])
      setBanks(banksData)
      setStats(statsData)
    } catch (error) {
      console.error('Failed to fetch data:', error)
      setError('加载数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateBank = () => {
    console.log('Navigating to new bank page')
    navigate('/knowledge/banks/new')
  }

  const handleEditBank = (bankId: number) => {
    navigate(`/knowledge/banks/${bankId}/edit`)
  }

  const handleDeleteBank = async (bankId: number) => {
    if (window.confirm('确定要删除这个题库吗？')) {
      try {
        await knowledgeBaseService.deleteQuestionBank(bankId)
        setBanks(banks.filter(bank => bank.id !== bankId))
      } catch (error) {
        console.error('Failed to delete bank:', error)
        alert('删除失败')
      }
    }
  }

  const handleStartExam = (bankId: number) => {
    navigate(`/knowledge/exam/setup/${bankId}`)
  }

  const handleStartPractice = (bankId: number) => {
    navigate(`/knowledge/practice/setup/${bankId}`)
  }

  const handleViewStats = () => {
    navigate('/knowledge/stats')
  }

  const handleViewWrongQuestions = () => {
    navigate('/knowledge/wrong-questions')
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* 页面标题 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center justify-center">
            <BookOpen className="h-10 w-10 mr-3 text-blue-600" />
            爬虫基础知识复习
          </h1>
          <p className="text-lg text-gray-600">
            系统化学习爬虫相关知识，提升技能水平
          </p>
        </div>

        {/* 统计卡片 */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-sm border border-blue-200 p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <BookOpen className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">总题库数</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_banks}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-green-200 p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Target className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">已答题数</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.answered_questions}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-yellow-200 p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">正确率</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.accuracy.toFixed(1)}%</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-purple-200 p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Clock className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">学习时间</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {Math.floor(stats.study_time / 3600)}h {Math.floor((stats.study_time % 3600) / 60)}m
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 快速操作 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <button
            onClick={handleCreateBank}
            className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-lg flex items-center justify-center transition-colors"
          >
            <Plus className="h-5 w-5 mr-2" />
            新建题库
          </button>
          
          <button
            onClick={handleViewStats}
            className="bg-green-600 hover:bg-green-700 text-white p-4 rounded-lg flex items-center justify-center transition-colors"
          >
            <BarChart3 className="h-5 w-5 mr-2" />
            学习统计
          </button>
          
          <button
            onClick={handleViewWrongQuestions}
            className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg flex items-center justify-center transition-colors"
          >
            <AlertCircle className="h-5 w-5 mr-2" />
            错题集
          </button>
          
          <button
            onClick={() => navigate('/knowledge/import')}
            className="bg-purple-600 hover:bg-purple-700 text-white p-4 rounded-lg flex items-center justify-center transition-colors"
          >
            <BookOpen className="h-5 w-5 mr-2" />
            导入题库
          </button>
        </div>

        {/* 题库列表 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">题库列表</h2>
          </div>
          
          {banks.length === 0 ? (
            <div className="text-center py-12">
              <BookOpen className="h-12 w-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-500 mb-4">还没有题库，点击上方按钮创建第一个题库吧！</p>
              <button
                onClick={handleCreateBank}
                className="btn btn-primary"
              >
                创建题库
              </button>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {banks.map((bank) => (
                <div key={bank.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-gray-900 mb-2">
                        {bank.name}
                      </h3>
                      {bank.description && (
                        <p className="text-gray-600 mb-2">{bank.description}</p>
                      )}
                      <div className="flex items-center text-sm text-gray-500">
                        <span className="mr-4">题目数量: {bank.question_count || 0}</span>
                        <span>创建时间: {new Date(bank.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleStartExam(bank.id)}
                        className="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors flex items-center"
                      >
                        <Play className="h-4 w-4 mr-1" />
                        考试
                      </button>
                      
                      <button
                        onClick={() => handleStartPractice(bank.id)}
                        className="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors flex items-center"
                      >
                        <Target className="h-4 w-4 mr-1" />
                        刷题
                      </button>
                      
                      <button
                        onClick={() => handleEditBank(bank.id)}
                        className="px-3 py-2 bg-yellow-600 text-white rounded-md hover:bg-yellow-700 transition-colors flex items-center"
                      >
                        <Edit className="h-4 w-4 mr-1" />
                        编辑
                      </button>
                      
                      <button
                        onClick={() => handleDeleteBank(bank.id)}
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

export default KnowledgeBase

