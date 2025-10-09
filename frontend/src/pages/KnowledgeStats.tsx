import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  ArrowLeft, 
  BarChart3, 
  BookOpen, 
  Target, 
  CheckCircle, 
  Clock,
  TrendingUp,
  Award
} from 'lucide-react'
import * as knowledgeBaseService from '@/services/knowledgeBaseService'
import type { StudyStatsSummary, StudyStats, QuestionBank } from '@/services/knowledgeBaseService'

const KnowledgeStats: React.FC = () => {
  const navigate = useNavigate()
  
  const [overallStats, setOverallStats] = useState<StudyStatsSummary | null>(null)
  const [bankStats, setBankStats] = useState<StudyStats[]>([])
  const [banks, setBanks] = useState<QuestionBank[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [statsData, banksData] = await Promise.all([
        knowledgeBaseService.getStudyStats(),
        knowledgeBaseService.getQuestionBanks()
      ])
      setOverallStats(statsData)
      setBanks(banksData)
      
      // 获取各题库的详细统计
      const bankStatsPromises = banksData.map(bank => 
        knowledgeBaseService.getBankStats(bank.id).catch(() => null)
      )
      const bankStatsResults = await Promise.all(bankStatsPromises)
      setBankStats(bankStatsResults.filter(Boolean) as StudyStats[])
    } catch (error) {
      console.error('Failed to fetch stats:', error)
      setError('加载统计数据失败')
    } finally {
      setLoading(false)
    }
  }

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    if (hours > 0) {
      return `${hours}小时${minutes}分钟`
    }
    return `${minutes}分钟`
  }

  const getAccuracyColor = (accuracy: number) => {
    if (accuracy >= 80) return 'text-green-600'
    if (accuracy >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getAccuracyLevel = (accuracy: number) => {
    if (accuracy >= 90) return '优秀'
    if (accuracy >= 80) return '良好'
    if (accuracy >= 60) return '及格'
    return '需努力'
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
        <BarChart3 className="h-12 w-12 mx-auto mb-4" />
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
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
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
              <BarChart3 className="h-8 w-8 mr-3 text-green-600" />
              学习统计
            </h1>
            <p className="text-lg text-gray-600 mt-2">
              查看你的学习进度和成绩分析
            </p>
          </div>
        </div>

        {overallStats && (
          <>
            {/* 总体统计 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-sm border border-blue-200 p-6">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <BookOpen className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">总题库数</p>
                    <p className="text-2xl font-bold text-gray-900">{overallStats.total_banks}</p>
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
                    <p className="text-2xl font-bold text-gray-900">{overallStats.answered_questions}</p>
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
                    <p className={`text-2xl font-bold ${getAccuracyColor(overallStats.accuracy)}`}>
                      {overallStats.accuracy.toFixed(1)}%
                    </p>
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
                      {formatTime(overallStats.study_time)}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* 详细统计 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2 text-blue-600" />
                  学习进度
                </h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">总题目数</span>
                    <span className="font-medium">{overallStats.total_questions}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">已答题数</span>
                    <span className="font-medium text-blue-600">{overallStats.answered_questions}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">正确题数</span>
                    <span className="font-medium text-green-600">{overallStats.correct_questions}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ 
                        width: overallStats.total_questions > 0 
                          ? `${(overallStats.answered_questions / overallStats.total_questions) * 100}%` 
                          : '0%' 
                      }}
                    />
                  </div>
                  <p className="text-xs text-gray-500 text-center">
                    完成进度: {overallStats.total_questions > 0 
                      ? ((overallStats.answered_questions / overallStats.total_questions) * 100).toFixed(1)
                      : 0}%
                  </p>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Award className="h-5 w-5 mr-2 text-yellow-600" />
                  成绩分析
                </h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">总得分</span>
                    <span className="font-medium text-yellow-600">{overallStats.total_score}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">错题数</span>
                    <span className="font-medium text-red-600">{overallStats.wrong_questions_count}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">已掌握题数</span>
                    <span className="font-medium text-green-600">{overallStats.mastered_questions_count}</span>
                  </div>
                  <div className="text-center">
                    <div className={`text-3xl font-bold ${getAccuracyColor(overallStats.accuracy)}`}>
                      {overallStats.accuracy.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-600">
                      学习等级: {getAccuracyLevel(overallStats.accuracy)}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 各题库统计 */}
            {bankStats.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">各题库学习情况</h3>
                </div>
                <div className="divide-y divide-gray-200">
                  {bankStats.map((stat) => {
                    const bank = banks.find(b => b.id === stat.bank_id)
                    const accuracy = stat.answered_questions > 0 
                      ? (stat.correct_questions / stat.answered_questions) * 100 
                      : 0
                    
                    return (
                      <div key={stat.id} className="p-6">
                        <div className="flex items-center justify-between mb-4">
                          <div>
                            <h4 className="text-lg font-medium text-gray-900">
                              {bank?.name || '未知题库'}
                            </h4>
                            <p className="text-sm text-gray-600">
                              {bank?.description || '暂无描述'}
                            </p>
                          </div>
                          <div className="text-right">
                            <div className={`text-2xl font-bold ${getAccuracyColor(accuracy)}`}>
                              {accuracy.toFixed(1)}%
                            </div>
                            <div className="text-sm text-gray-600">
                              {getAccuracyLevel(accuracy)}
                            </div>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div>
                            <span className="text-gray-600">总题数:</span>
                            <span className="ml-1 font-medium">{stat.total_questions}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">已答:</span>
                            <span className="ml-1 font-medium text-blue-600">{stat.answered_questions}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">正确:</span>
                            <span className="ml-1 font-medium text-green-600">{stat.correct_questions}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">学习时间:</span>
                            <span className="ml-1 font-medium">{formatTime(stat.study_time)}</span>
                          </div>
                        </div>
                        
                        <div className="mt-4">
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                              style={{ 
                                width: stat.total_questions > 0 
                                  ? `${(stat.answered_questions / stat.total_questions) * 100}%` 
                                  : '0%' 
                              }}
                            />
                          </div>
                          <p className="text-xs text-gray-500 mt-1">
                            完成进度: {stat.total_questions > 0 
                              ? ((stat.answered_questions / stat.total_questions) * 100).toFixed(1)
                              : 0}%
                          </p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default KnowledgeStats

