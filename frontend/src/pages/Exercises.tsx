import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { exerciseService, Exercise } from '../services/exerciseService'
import { Clock, Star, Target, Filter, Search } from 'lucide-react'

const Exercises: React.FC = () => {
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [difficultyFilter, setDifficultyFilter] = useState('')
  const [filteredExercises, setFilteredExercises] = useState<Exercise[]>([])

  useEffect(() => {
    const fetchExercises = async () => {
      try {
        const data = await exerciseService.getExercises()
        setExercises(data)
        setFilteredExercises(data)
      } catch (error) {
        console.error('Failed to fetch exercises:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchExercises()
  }, [])

  useEffect(() => {
    let filtered = exercises

    if (searchTerm) {
      filtered = filtered.filter(exercise =>
        exercise.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        exercise.description.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (difficultyFilter) {
      filtered = filtered.filter(exercise => exercise.difficulty === difficultyFilter)
    }

    setFilteredExercises(filtered)
  }, [exercises, searchTerm, difficultyFilter])

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

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">练习题</h1>
        <p className="text-gray-600">通过实战练习提升你的爬虫逆向技能</p>
      </div>

      {/* 搜索和筛选 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="搜索练习题..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-500" />
            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="input w-32"
            >
              <option value="">全部难度</option>
              <option value="beginner">初级</option>
              <option value="intermediate">中级</option>
              <option value="advanced">高级</option>
              <option value="hard">困难</option>
              <option value="hell">地狱</option>
            </select>
          </div>
        </div>
      </div>

      {/* 练习题列表 */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredExercises.map((exercise) => (
          <div key={exercise.id} className="card hover:shadow-lg transition-shadow">
            <div className="card-header">
              <div className="flex items-start justify-between">
                <h3 className="card-title text-lg">{exercise.title}</h3>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(exercise.difficulty)}`}>
                  {getDifficultyText(exercise.difficulty)}
                </span>
              </div>
              <p className="card-description text-sm mt-2 line-clamp-3">
                {exercise.description}
              </p>
            </div>
            
            <div className="card-content">
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4" />
                  <span>{exercise.points} 分</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span>{exercise.time_limit}秒</span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="text-xs text-gray-500">
                  创建于 {new Date(exercise.created_at).toLocaleDateString()}
                </div>
                <Link
                  to={`/exercises/${exercise.id}`}
                  className="btn btn-primary btn-sm flex items-center space-x-1"
                >
                  <Target className="h-4 w-4" />
                  <span>开始练习</span>
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredExercises.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-500 mb-4">
            <Target className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>没有找到匹配的练习题</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Exercises

