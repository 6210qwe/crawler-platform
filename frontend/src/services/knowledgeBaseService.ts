import { api } from './api'

// 类型定义
export interface QuestionBank {
  id: number
  name: string
  description?: string
  is_active: boolean
  created_at: string
  updated_at?: string
  question_count?: number
}

export interface Question {
  id: number
  bank_id: number
  type: string
  question: string
  options?: string[]
  answer: string
  explanation?: string
  score: number
  difficulty: string
  is_active: boolean
  created_at: string
  updated_at?: string
}

export interface UserAnswer {
  id: number
  user_id: number
  question_id: number
  answer: string
  is_correct: boolean
  score: number
  time_spent: number
  session_id?: string
  created_at: string
}

export interface WrongQuestion {
  id: number
  user_id: number
  question_id: number
  user_answer: string
  wrong_count: number
  last_wrong_at: string
  is_mastered: boolean
  mastered_at?: string
  created_at: string
  question?: Question
}

export interface ExamSession {
  id: number
  user_id: number
  bank_id: number
  session_id: string
  exam_type: string
  total_questions: number
  answered_questions: number
  correct_questions: number
  total_score: number
  user_score: number
  time_limit?: number
  time_spent: number
  is_completed: boolean
  started_at: string
  completed_at?: string
}

export interface StudyStats {
  id: number
  user_id: number
  bank_id: number
  total_questions: number
  answered_questions: number
  correct_questions: number
  total_score: number
  study_time: number
  last_study_at?: string
  created_at: string
  updated_at?: string
}

export interface StudyStatsSummary {
  total_banks: number
  total_questions: number
  answered_questions: number
  correct_questions: number
  total_score: number
  study_time: number
  accuracy: number
  wrong_questions_count: number
  mastered_questions_count: number
}

export interface ExamSetupRequest {
  bank_id: number
  total_questions: number
  single_ratio: number
  multi_ratio: number
  bool_ratio: number
  time_limit?: number
}

export interface PracticeSetupRequest {
  bank_id: number
  order: string
}

export interface ExamResult {
  session_id: string
  total_questions: number
  correct_questions: number
  total_score: number
  user_score: number
  accuracy: number
  time_spent: number
  is_completed: boolean
}

// 题库管理API
export const getQuestionBanks = async (skip = 0, limit = 100): Promise<QuestionBank[]> => {
  try {
    const response = await api.get(`/knowledge/banks?skip=${skip}&limit=${limit}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch question banks:', error)
    throw error
  }
}

export const createQuestionBank = async (bankData: { name: string; description?: string }): Promise<QuestionBank> => {
  try {
    const response = await api.post('/knowledge/banks', bankData)
    return response.data
  } catch (error) {
    console.error('Failed to create question bank:', error)
    throw error
  }
}

export const getQuestionBank = async (bankId: number): Promise<QuestionBank> => {
  try {
    const response = await api.get(`/knowledge/banks/${bankId}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch question bank:', error)
    throw error
  }
}

export const updateQuestionBank = async (bankId: number, bankData: { name?: string; description?: string; is_active?: boolean }): Promise<QuestionBank> => {
  try {
    const response = await api.put(`/knowledge/banks/${bankId}`, bankData)
    return response.data
  } catch (error) {
    console.error('Failed to update question bank:', error)
    throw error
  }
}

export const deleteQuestionBank = async (bankId: number): Promise<void> => {
  try {
    await api.delete(`/knowledge/banks/${bankId}`)
  } catch (error) {
    console.error('Failed to delete question bank:', error)
    throw error
  }
}

// 题目管理API
export const getQuestions = async (bankId: number, skip = 0, limit = 100): Promise<Question[]> => {
  try {
    const response = await api.get(`/knowledge/banks/${bankId}/questions?skip=${skip}&limit=${limit}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch questions:', error)
    throw error
  }
}

export const createQuestion = async (bankId: number, questionData: {
  type: string
  question: string
  options?: string[]
  answer: string
  explanation?: string
  score?: number
  difficulty?: string
}): Promise<Question> => {
  try {
    const response = await api.post(`/knowledge/banks/${bankId}/questions`, questionData)
    return response.data
  } catch (error) {
    console.error('Failed to create question:', error)
    throw error
  }
}

export const getQuestion = async (questionId: number): Promise<Question> => {
  try {
    const response = await api.get(`/knowledge/questions/${questionId}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch question:', error)
    throw error
  }
}

export const updateQuestion = async (questionId: number, questionData: {
  type?: string
  question?: string
  options?: string[]
  answer?: string
  explanation?: string
  score?: number
  difficulty?: string
  is_active?: boolean
}): Promise<Question> => {
  try {
    const response = await api.put(`/knowledge/questions/${questionId}`, questionData)
    return response.data
  } catch (error) {
    console.error('Failed to update question:', error)
    throw error
  }
}

export const deleteQuestion = async (questionId: number): Promise<void> => {
  try {
    await api.delete(`/knowledge/questions/${questionId}`)
  } catch (error) {
    console.error('Failed to delete question:', error)
    throw error
  }
}

// 考试功能API
export const setupExam = async (setupData: ExamSetupRequest): Promise<ExamSession> => {
  try {
    const response = await api.post('/knowledge/exam/setup', setupData)
    return response.data
  } catch (error) {
    console.error('Failed to setup exam:', error)
    throw error
  }
}

export const setupPractice = async (setupData: PracticeSetupRequest): Promise<ExamSession> => {
  try {
    const response = await api.post('/knowledge/practice/setup', setupData)
    return response.data
  } catch (error) {
    console.error('Failed to setup practice:', error)
    throw error
  }
}

export const getSessionQuestions = async (sessionId: string): Promise<Question[]> => {
  try {
    const response = await api.get(`/knowledge/sessions/${sessionId}/questions`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch session questions:', error)
    throw error
  }
}

export const submitAnswer = async (sessionId: string, answerData: {
  question_id: number
  answer: string
  time_spent: number
}): Promise<UserAnswer> => {
  try {
    const response = await api.post(`/knowledge/sessions/${sessionId}/submit`, answerData)
    return response.data
  } catch (error) {
    console.error('Failed to submit answer:', error)
    throw error
  }
}

export const completeExam = async (sessionId: string): Promise<ExamResult> => {
  try {
    const response = await api.post(`/knowledge/sessions/${sessionId}/complete`)
    return response.data
  } catch (error) {
    console.error('Failed to complete exam:', error)
    throw error
  }
}

// 错题集API
export const getWrongQuestions = async (bankId?: number): Promise<WrongQuestion[]> => {
  try {
    const url = bankId ? `/knowledge/wrong-questions?bank_id=${bankId}` : '/knowledge/wrong-questions'
    const response = await api.get(url)
    return response.data
  } catch (error) {
    console.error('Failed to fetch wrong questions:', error)
    throw error
  }
}

export const masterQuestion = async (wrongQuestionId: number): Promise<void> => {
  try {
    await api.post(`/knowledge/wrong-questions/${wrongQuestionId}/master`)
  } catch (error) {
    console.error('Failed to master question:', error)
    throw error
  }
}

export const deleteWrongQuestion = async (wrongQuestionId: number): Promise<void> => {
  try {
    await api.delete(`/knowledge/wrong-questions/${wrongQuestionId}`)
  } catch (error) {
    console.error('Failed to delete wrong question:', error)
    throw error
  }
}

// 学习统计API
export const getStudyStats = async (): Promise<StudyStatsSummary> => {
  try {
    const response = await api.get('/knowledge/stats')
    return response.data
  } catch (error) {
    console.error('Failed to fetch study stats:', error)
    throw error
  }
}

export const getBankStats = async (bankId: number): Promise<StudyStats> => {
  try {
    const response = await api.get(`/knowledge/stats/${bankId}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch bank stats:', error)
    throw error
  }
}

