import { api } from './api'

export interface StudyNote {
  id: number
  user_id: number
  title: string
  content_html: string
  content_text?: string
  tags?: string[]
  is_private: boolean
  created_at: string
  updated_at?: string
}

export interface StudyNoteCreate {
  title: string
  content_html: string
  content_text?: string
  tags?: string[]
  is_private?: boolean
}

export interface StudyNoteUpdate extends Partial<StudyNoteCreate> {}

export const notesService = {
  async list(params?: { skip?: number; limit?: number }): Promise<StudyNote[]> {
    const res = await api.get('/notes', { params })
    return res.data
  },
  async create(data: StudyNoteCreate): Promise<StudyNote> {
    const res = await api.post('/notes', data)
    return res.data
  },
  async get(id: number): Promise<StudyNote> {
    const res = await api.get(`/notes/${id}`)
    return res.data
  },
  async update(id: number, data: StudyNoteUpdate): Promise<StudyNote> {
    const res = await api.put(`/notes/${id}`, data)
    return res.data
  },
  async remove(id: number): Promise<void> {
    await api.delete(`/notes/${id}`)
  },
}


