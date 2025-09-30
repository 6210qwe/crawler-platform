import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { notesService, StudyNote } from '@/services/notesService'
import { useAuth } from '@/contexts/AuthContext'
import { ArrowLeft, Calendar, Eye, Edit3, Trash2, Clock, User } from 'lucide-react'

export default function NoteDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [note, setNote] = useState<StudyNote | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchNote = async () => {
      if (!id) return
      
      try {
        setLoading(true)
        const data = await notesService.get(parseInt(id))
        setNote(data)
      } catch (e) {
        setError('笔记不存在或无权访问')
      } finally {
        setLoading(false)
      }
    }

    fetchNote()
  }, [id])

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getReadingTime = (content: string) => {
    // 简单的阅读时间计算：每200字约1分钟
    const textLength = content.replace(/<[^>]*>/g, '').length
    const minutes = Math.ceil(textLength / 200)
    return `${minutes} 分钟阅读`
  }

  const handleDelete = async () => {
    if (!note || !window.confirm('确定要删除这篇笔记吗？')) return
    
    try {
      await notesService.remove(note.id)
      navigate('/notes')
    } catch (e) {
      alert('删除失败')
    }
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    )
  }

  if (error || !note) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Edit3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p className="text-lg">{error || '笔记不存在'}</p>
          </div>
          <Link to="/notes" className="btn btn-primary">
            返回笔记列表
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* 返回按钮 */}
      <div className="mb-6">
        <Link 
          to="/notes" 
          className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>返回笔记列表</span>
        </Link>
      </div>

      {/* 文章头部 */}
      <header className="mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4 leading-tight">
          {note.title}
        </h1>
        
        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-6">
          <div className="flex items-center space-x-1">
            <Calendar className="h-4 w-4" />
            <span>{formatDate(note.created_at)}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Clock className="h-4 w-4" />
            <span>{getReadingTime(note.content_html)}</span>
          </div>
          <div className="flex items-center space-x-1">
            <Eye className="h-4 w-4" />
            <span>{note.view_count} 次阅读</span>
          </div>
          {note.updated_at && note.updated_at !== note.created_at && (
            <div className="flex items-center space-x-1">
              <Edit3 className="h-4 w-4" />
              <span>更新于 {formatDate(note.updated_at)}</span>
            </div>
          )}
        </div>

        {/* 操作按钮 */}
        {user && (
          <div className="flex items-center space-x-3 pb-6 border-b border-gray-200">
            <button className="flex items-center space-x-1 text-blue-600 hover:text-blue-700 transition-colors">
              <Edit3 className="h-4 w-4" />
              <span>编辑</span>
            </button>
            <button 
              onClick={handleDelete}
              className="flex items-center space-x-1 text-red-600 hover:text-red-700 transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              <span>删除</span>
            </button>
          </div>
        )}
      </header>

      {/* 文章内容 */}
      <article className="prose prose-lg max-w-none">
        <div 
          className="text-gray-800 leading-relaxed"
          dangerouslySetInnerHTML={{ __html: note.content_html }}
        />
      </article>

      {/* 文章底部 */}
      <footer className="mt-12 pt-8 border-t border-gray-200">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-4 md:mb-0">
            <div className="flex items-center space-x-1">
              <User className="h-4 w-4" />
              <span>作者：{user?.username || '匿名用户'}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Calendar className="h-4 w-4" />
              <span>创建于 {formatDate(note.created_at)}</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Link 
              to="/notes" 
              className="btn btn-outline btn-sm"
            >
              返回列表
            </Link>
            {user && (
              <button className="btn btn-primary btn-sm">
                编辑笔记
              </button>
            )}
          </div>
        </div>
      </footer>
    </div>
  )
}
