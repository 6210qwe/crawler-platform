import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { notesService, StudyNote } from '@/services/notesService'
import { useAuth } from '@/contexts/AuthContext'
import { Plus, Calendar, Eye, Edit3, Trash2, User, Tag } from 'lucide-react'
import CrawlerSidebar from '@/components/XifengliSidebar'

export default function Notes() {
  const { user, loading } = useAuth()
  const [notes, setNotes] = useState<StudyNote[]>([])
  const [title, setTitle] = useState('')
  const [html, setHtml] = useState('')
  const [busy, setBusy] = useState(false)
  const [showEditor, setShowEditor] = useState(false)

  const load = async () => {
    setBusy(true)
    try {
      const data = await notesService.list()
      setNotes(data)
    } catch (e) {
      // 未登录或接口不可用时，不阻塞页面渲染
      setNotes([])
    } finally {
      setBusy(false)
    }
  }

  useEffect(() => {
    // 不再依赖登录态，进入即尝试拉取（未登录会静默失败，仍显示编辑器）
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // 进入页面时，若没有用户信息，先尝试刷新会话
  useEffect(() => {
    if (!user && !loading) {
      // 移除 refresh 调用，因为 AuthContext 中没有这个函数
      // 用户可以通过登录页面手动登录
    }
  }, [user, loading])

  const submit = async () => {
    if (!title.trim() || !html.trim()) return
    await notesService.create({ title, content_html: html })
    setTitle('')
    setHtml('')
    setShowEditor(false)
    load()
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  }

  const getContentPreview = (content: string) => {
    // 移除HTML标签，获取纯文本预览
    const textContent = content.replace(/<[^>]*>/g, '')
    return textContent.length > 200 ? textContent.substring(0, 200) + '...' : textContent
  }

  const getRandomThumbnail = (title: string) => {
    // 根据标题生成一个简单的缩略图
    const colors = [
      'bg-gradient-to-br from-blue-400 to-blue-600',
      'bg-gradient-to-br from-green-400 to-green-600', 
      'bg-gradient-to-br from-purple-400 to-purple-600',
      'bg-gradient-to-br from-pink-400 to-pink-600',
      'bg-gradient-to-br from-indigo-400 to-indigo-600',
      'bg-gradient-to-br from-teal-400 to-teal-600'
    ]
    const colorIndex = title.length % colors.length
    return colors[colorIndex]
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* 主要内容区域 */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex gap-8">
          {/* 左侧内容区域 */}
          <div className="flex-1">
            {/* 页面标题 */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">学习笔记</h1>
              <p className="text-gray-600">记录你的学习心得和技术总结</p>
            </div>

            {/* 新建笔记按钮 */}
            <div className="mb-8">
              <button
                onClick={() => setShowEditor(!showEditor)}
                className="btn btn-primary flex items-center space-x-2"
              >
                <Plus className="h-4 w-4" />
                <span>新建笔记</span>
              </button>
            </div>

            {/* 编辑器 */}
            {showEditor && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">新建学习笔记</h3>
                <div className="space-y-4">
                  <input 
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                    placeholder="请输入笔记标题..." 
                    value={title} 
                    onChange={e=>setTitle(e.target.value)} 
                  />
                  <textarea 
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent min-h-[200px]" 
                    value={html} 
                    onChange={e=>setHtml(e.target.value)} 
                    placeholder="请输入笔记内容..." 
                  />
                  <div className="flex justify-between items-center">
                    {!user && <span className="text-sm text-gray-500">未登录：可编辑但需登录后才能保存</span>}
                    <div className="flex space-x-2">
                      <button 
                        className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50" 
                        onClick={() => setShowEditor(false)}
                      >
                        取消
                      </button>
                      <button 
                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50" 
                        onClick={submit} 
                        disabled={busy || !user || !title.trim() || !html.trim()}
                      >
                        {busy ? '保存中...' : '保存'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 笔记列表 - 西枫里风格 */}
            <div className="space-y-6">
              {busy ? (
                <div className="flex justify-center items-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
              ) : notes.length > 0 ? (
                notes.map(note => (
                  <article key={note.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
                    <div className="flex">
                      {/* 左侧缩略图区域 */}
                      <div className="w-1/3 min-h-[200px] relative">
                        <div className={`w-full h-full ${getRandomThumbnail(note.title)} flex items-center justify-center`}>
                          <div className="text-center text-white p-6">
                            <div className="text-2xl font-bold mb-2 opacity-90">
                              {note.title.substring(0, 8)}
                            </div>
                   <div className="text-sm opacity-75">
                     技术笔记
                   </div>
                          </div>
                        </div>
                        {/* 装饰性元素 */}
                        <div className="absolute bottom-4 left-4 text-white text-xs opacity-75">
                          <div className="font-medium">TECH NOTES</div>
                        </div>
                      </div>

                      {/* 右侧内容区域 */}
                      <div className="w-2/3 p-6 flex flex-col justify-between">
                        <div>
                          <div className="flex items-start justify-between mb-3">
                            <Link 
                              to={`/notes/${note.id}`}
                              className="text-xl font-semibold text-gray-900 hover:text-blue-600 cursor-pointer line-clamp-2 flex-1 mr-4"
                            >
                              {note.title}
                            </Link>
                            {user && (
                              <div className="flex items-center space-x-2">
                                <button className="p-1 text-gray-400 hover:text-blue-600">
                                  <Edit3 className="h-4 w-4" />
                                </button>
                                <button className="p-1 text-gray-400 hover:text-red-600">
                                  <Trash2 className="h-4 w-4" />
                                </button>
                              </div>
                            )}
                          </div>
                          
                          <p className="text-gray-600 mb-4 line-clamp-3 text-sm leading-relaxed">
                            {getContentPreview(note.content_html)}
                          </p>
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <div className="flex items-center space-x-1">
                          <User className="h-3 w-3" />
                          <span>{user?.username || '爬虫工程师'}</span>
                        </div>
                            <div className="flex items-center space-x-1">
                              <Calendar className="h-3 w-3" />
                              <span>{formatDate(note.created_at)}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Eye className="h-3 w-3" />
                              <span>{note.view_count}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Tag className="h-3 w-3" />
                              <span>爬虫技术</span>
                            </div>
                          </div>
                          
                          <Link 
                            to={`/notes/${note.id}`}
                            className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700 transition-colors"
                          >
                            阅读全文
                          </Link>
                        </div>
                      </div>
                    </div>
                  </article>
                ))
              ) : (
                <div className="text-center py-12">
                  <div className="text-gray-400 mb-4">
                    <Edit3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p className="text-lg">{user ? '还没有笔记，创建第一篇吧！' : '未登录或暂无笔记'}</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* 右侧侧边栏 */}
          <div className="w-80">
            <CrawlerSidebar />
          </div>
        </div>
      </div>
    </div>
  )
}


