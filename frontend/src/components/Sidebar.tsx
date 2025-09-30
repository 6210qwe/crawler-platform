import { Link, useLocation } from 'react-router-dom'
import { BookOpen, User, BarChart3, Settings } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Sidebar: React.FC = () => {
  const location = useLocation()
  const { user } = useAuth()

  const navigation = [
    { name: '学习案例', href: '/exercises', icon: BookOpen },
    { name: '学习笔记', href: '/notes', icon: BookOpen },
    { name: '学习进度', href: '/leaderboard', icon: BarChart3 },
    { name: '个人资料', href: '/profile', icon: User },
    { name: '学习仪表板', href: '/dashboard', icon: BarChart3 },
  ]

  // 如果是管理员，添加管理功能
  if (user?.is_superuser) {
    navigation.push({ name: '系统设置', href: '/admin', icon: Settings })
  }

  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
      <div className="p-6">
        <nav className="space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <item.icon className="h-5 w-5" />
                <span>{item.name}</span>
              </Link>
            )
          })}
        </nav>
      </div>
    </div>
  )
}

export default Sidebar

