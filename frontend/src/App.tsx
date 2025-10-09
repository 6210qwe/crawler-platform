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
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App

