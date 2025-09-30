import { useEffect, useState } from 'react'
import { notesService, StudyNote } from '@/services/notesService'
import { useAuth } from '@/contexts/AuthContext'

export default function Notes() {
  const { user, loading } = useAuth()
  const [notes, setNotes] = useState<StudyNote[]>([])
  const [title, setTitle] = useState('')
  const [html, setHtml] = useState('')
  const [busy, setBusy] = useState(false)

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
    load()
  }

  // 不再强制要求登录。未登录时允许编辑但保存会提示先登录。

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="card">
        <div className="card-header">
          <div className="card-title">新建学习笔记</div>
        </div>
        <div className="card-content space-y-3">
          <input className="input" placeholder="标题" value={title} onChange={e=>setTitle(e.target.value)} />
          <textarea 
            className="input min-h-[160px]" 
            value={html} 
            onChange={e=>setHtml(e.target.value)} 
            placeholder="输入笔记内容..." 
          />
          <div className="flex justify-between items-center">
            {!user && <span className="text-xs text-gray-500">未登录：可编辑但需登录后才能保存</span>}
            <button className="btn btn-primary btn-sm" onClick={submit} disabled={busy || !user}>保存</button>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {notes.map(n => (
          <div key={n.id} className="card">
            <div className="card-header">
            <div className="card-title text-xl">{n.title}</div>
              <div className="card-description">{new Date(n.created_at).toLocaleString()}</div>
            </div>
            <div className="card-content">
              <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: n.content_html }} />
            </div>
          </div>
        ))}
        {!busy && notes.length === 0 && <div className="text-gray-500">{user ? '暂无笔记' : '未登录或暂无笔记'}</div>}
      </div>
    </div>
  )
}


