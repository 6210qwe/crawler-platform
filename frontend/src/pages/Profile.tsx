import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { User, Mail, Calendar, Edit3, Save, X } from 'lucide-react'

const Profile: React.FC = () => {
  const { user, logout } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    full_name: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username,
        email: user.email,
        full_name: user.full_name || ''
      })
    }
  }, [user])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSave = async () => {
    setLoading(true)
    setError('')
    setSuccess('')

    try {
      // 这里应该调用更新用户信息的API
      // await userService.updateUser(user.id, formData)
      setSuccess('个人信息更新成功')
      setIsEditing(false)
    } catch (err: any) {
      setError(err.response?.data?.detail || '更新失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = () => {
    setFormData({
      username: user?.username || '',
      email: user?.email || '',
      full_name: user?.full_name || ''
    })
    setIsEditing(false)
    setError('')
    setSuccess('')
  }

  if (!user) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">请先登录</p>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">个人资料</h1>
        <p className="text-gray-600">管理你的个人信息和账户设置</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* 左侧：基本信息 */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="card-header">
              <div className="flex items-center justify-between">
                <h2 className="card-title text-xl">基本信息</h2>
                {!isEditing ? (
                  <button
                    onClick={() => setIsEditing(true)}
                    className="btn btn-outline btn-sm flex items-center space-x-1"
                  >
                    <Edit3 className="h-4 w-4" />
                    <span>编辑</span>
                  </button>
                ) : (
                  <div className="flex space-x-2">
                    <button
                      onClick={handleCancel}
                      className="btn btn-outline btn-sm flex items-center space-x-1"
                    >
                      <X className="h-4 w-4" />
                      <span>取消</span>
                    </button>
                    <button
                      onClick={handleSave}
                      disabled={loading}
                      className="btn btn-primary btn-sm flex items-center space-x-1"
                    >
                      <Save className="h-4 w-4" />
                      <span>{loading ? '保存中...' : '保存'}</span>
                    </button>
                  </div>
                )}
              </div>
            </div>

            <div className="card-content">
              {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              )}

              {success && (
                <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-green-700 text-sm">{success}</p>
                </div>
              )}

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    用户名
                  </label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      className="input"
                    />
                  ) : (
                    <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-md">
                      <User className="h-4 w-4 text-gray-500" />
                      <span>{user.username}</span>
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    邮箱
                  </label>
                  {isEditing ? (
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      className="input"
                    />
                  ) : (
                    <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-md">
                      <Mail className="h-4 w-4 text-gray-500" />
                      <span>{user.email}</span>
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    姓名
                  </label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleChange}
                      className="input"
                      placeholder="请输入真实姓名"
                    />
                  ) : (
                    <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-md">
                      <User className="h-4 w-4 text-gray-500" />
                      <span>{user.full_name || '未设置'}</span>
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    注册时间
                  </label>
                  <div className="flex items-center space-x-2 p-3 bg-gray-50 rounded-md">
                    <Calendar className="h-4 w-4 text-gray-500" />
                    <span>{new Date(user.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 右侧：统计信息 */}
        <div className="lg:col-span-1">
          <div className="card">
            <div className="card-header">
              <h3 className="card-title text-lg">统计信息</h3>
            </div>
            <div className="card-content">
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">完成练习</span>
                  <span className="font-semibold">0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">总得分</span>
                  <span className="font-semibold">0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">正确率</span>
                  <span className="font-semibold">0%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">排名</span>
                  <span className="font-semibold">-</span>
                </div>
              </div>
            </div>
          </div>

          <div className="card mt-6">
            <div className="card-header">
              <h3 className="card-title text-lg">账户操作</h3>
            </div>
            <div className="card-content">
              <button
                onClick={logout}
                className="w-full btn btn-outline btn-sm text-red-600 border-red-300 hover:bg-red-50"
              >
                退出登录
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile

