import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Code, Target, Trophy, Users, ArrowRight } from 'lucide-react'

const Home: React.FC = () => {
  const { user } = useAuth()

  const features = [
    {
      icon: Target,
      title: '实战学习',
      description: '基于真实网站的爬虫逆向挑战，提升实战能力'
    },
    {
      icon: Code,
      title: '技术栈',
      description: '涵盖JavaScript逆向、反爬虫技术、加密算法等'
    },
    {
      icon: Trophy,
      title: '学习进度',
      description: '跟踪学习进度，展示你的技术实力'
    },
    {
      icon: Users,
      title: '社区交流',
      description: '与同行交流经验，共同成长进步'
    }
  ]

  const stats = [
    { label: '学习案例', value: '100+' },
    { label: '活跃用户', value: '1000+' },
    { label: '完成率', value: '85%' },
    { label: '满意度', value: '4.8/5' }
  ]

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-20">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          爬虫逆向学习平台
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          通过实战学习提升爬虫逆向技能，掌握JavaScript逆向、反爬虫技术等核心能力
        </p>
        <div className="flex justify-center space-x-4">
          {user ? (
            <Link
              to="/exercises"
              className="btn btn-primary btn-lg flex items-center space-x-2"
            >
              <span>开始学习</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          ) : (
            <>
              <Link
                to="/register"
                className="btn btn-primary btn-lg flex items-center space-x-2"
              >
                <span>立即注册</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link
                to="/login"
                className="btn btn-outline btn-lg"
              >
                登录
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-8 py-16">
        {stats.map((stat, index) => (
          <div key={index} className="text-center">
            <div className="text-3xl font-bold text-primary-600 mb-2">
              {stat.value}
            </div>
            <div className="text-gray-600">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Features Section */}
      <div className="py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            为什么选择我们
          </h2>
          <p className="text-lg text-gray-600">
            专业的爬虫逆向学习平台，助你快速提升技能
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="card p-6 text-center hover:shadow-lg transition-shadow">
              <div className="flex justify-center mb-4">
                <div className="p-3 bg-primary-100 rounded-full">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary-600 rounded-2xl p-12 text-center text-white mb-20">
        <h2 className="text-3xl font-bold mb-4">
          准备好开始你的爬虫逆向学习之旅了吗？
        </h2>
        <p className="text-xl mb-8 opacity-90">
          加入我们的学习社区，与同行一起成长进步
        </p>
        {!user && (
          <Link
            to="/register"
            className="btn bg-white text-primary-600 hover:bg-gray-100 btn-lg"
          >
            免费注册
          </Link>
        )}
      </div>
    </div>
  )
}

export default Home

