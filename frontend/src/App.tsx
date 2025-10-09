import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/ProtectedRoute'
import Layout from './components/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Exercises from './pages/Exercises'
import ExerciseDetail from './pages/ExerciseDetail'
import ChallengePage from './pages/ChallengePage'
import Profile from './pages/Profile'
import Dashboard from './pages/Dashboard'
import Notes from './pages/Notes'
import NoteDetail from './pages/NoteDetail'
import ExercisesTest from './pages/ExercisesTest'
import SimpleTest from './pages/SimpleTest'
import ExercisesFixed from './pages/ExercisesFixed'
import KnowledgeBase from './pages/KnowledgeBase'
import KnowledgeBankManager from './pages/KnowledgeBankManager'
import Leaderboard from './pages/Leaderboard'
import ReverseAnalysis from './pages/ReverseAnalysis'
import DataCollection from './pages/DataCollection'
import AntiCrawler from './pages/AntiCrawler'
import TechSharing from './pages/TechSharing'
import ToolsDownload from './pages/ToolsDownload'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="exercises" element={<Exercises />} />
          <Route path="exercises-test" element={<ExercisesTest />} />
          <Route path="simple-test" element={<SimpleTest />} />
          <Route path="exercises-fixed" element={<ExercisesFixed />} />
          <Route path="exercises/:id" element={<ExerciseDetail />} />
          <Route 
            path="challenge/:id" 
            element={
              <ProtectedRoute>
                <ChallengePage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="profile" 
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route path="notes" element={<Notes />} />
          <Route path="notes/:id" element={<NoteDetail />} />
          <Route 
            path="knowledge" 
            element={
              <ProtectedRoute>
                <KnowledgeBase />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="knowledge/banks/new" 
            element={
              <ProtectedRoute>
                <KnowledgeBankManager />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="knowledge/banks/:bankId/edit" 
            element={
              <ProtectedRoute>
                <KnowledgeBankManager />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="leaderboard" 
            element={
              <ProtectedRoute>
                <Leaderboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="admin" 
            element={
              <ProtectedRoute>
                <div className="p-8">
                  <h1 className="text-2xl font-bold mb-4">系统设置</h1>
                  <p className="text-gray-600">管理员功能开发中...</p>
                </div>
              </ProtectedRoute>
            } 
          />
          <Route path="reverse-analysis" element={<ReverseAnalysis />} />
          <Route path="data-collection" element={<DataCollection />} />
          <Route path="anti-crawler" element={<AntiCrawler />} />
          <Route path="tech-sharing" element={<TechSharing />} />
          <Route path="tools-download" element={<ToolsDownload />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App

