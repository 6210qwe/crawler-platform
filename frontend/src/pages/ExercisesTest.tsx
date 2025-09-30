import { useState, useEffect } from 'react'
import { exerciseService, Exercise } from '@/services/exerciseService'

export default function ExercisesTest() {
  const [exercises, setExercises] = useState<Exercise[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('开始获取数据...')
        setLoading(true)
        setError(null)
        
        const data = await exerciseService.getExercises({ limit: 5 })
        console.log('获取到的数据:', data)
        
        setExercises(data)
      } catch (err) {
        console.error('获取数据失败:', err)
        setError(err instanceof Error ? err.message : '未知错误')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">测试页面 - 加载中...</h1>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4 text-red-600">测试页面 - 错误</h1>
        <p className="text-red-500">错误信息: {error}</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          重新加载
        </button>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">测试页面 - 数据获取成功</h1>
      <p className="mb-4">找到 {exercises.length} 道题目</p>
      
      {exercises.length === 0 ? (
        <div className="text-gray-500">没有数据</div>
      ) : (
        <div className="space-y-4">
          {exercises.map((exercise) => (
            <div key={exercise.id} className="p-4 border rounded-lg">
              <h3 className="font-bold">{exercise.title}</h3>
              <p className="text-gray-600">{exercise.description}</p>
              <p className="text-sm text-blue-600">难度: {exercise.difficulty}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

