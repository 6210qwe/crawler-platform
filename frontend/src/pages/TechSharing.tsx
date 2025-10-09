import { Users, MessageCircle, BookOpen, Award } from 'lucide-react'

export default function TechSharing() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">技术分享</h1>
        <p className="text-xl text-gray-600">与社区分享爬虫技术和经验心得</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Users className="h-8 w-8 text-blue-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">技术交流</h3>
          </div>
          <p className="text-gray-600 mb-4">与同行交流爬虫技术心得和解决方案</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 技术问题讨论</div>
            <div className="text-sm text-gray-500">• 经验分享</div>
            <div className="text-sm text-gray-500">• 最佳实践</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <MessageCircle className="h-8 w-8 text-green-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">案例分享</h3>
          </div>
          <p className="text-gray-600 mb-4">分享真实的爬虫项目案例和解决方案</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 项目实战案例</div>
            <div className="text-sm text-gray-500">• 技术难点突破</div>
            <div className="text-sm text-gray-500">• 性能优化经验</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <BookOpen className="h-8 w-8 text-purple-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">学习资源</h3>
          </div>
          <p className="text-gray-600 mb-4">推荐优质的学习资源和工具</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 技术文档</div>
            <div className="text-sm text-gray-500">• 开源项目</div>
            <div className="text-sm text-gray-500">• 学习教程</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Award className="h-8 w-8 text-orange-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">技术竞赛</h3>
          </div>
          <p className="text-gray-600 mb-4">参与技术竞赛，提升技能水平</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 爬虫挑战赛</div>
            <div className="text-sm text-gray-500">• 技术PK</div>
            <div className="text-sm text-gray-500">• 创新项目</div>
          </div>
        </div>
      </div>

      <div className="mt-12 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">社区活动</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">线上活动</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 技术直播分享</li>
              <li>• 在线技术讨论</li>
              <li>• 代码审查活动</li>
              <li>• 技术问答</li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">线下聚会</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 技术沙龙</li>
              <li>• 开发者聚会</li>
              <li>• 技术培训</li>
              <li>• 项目展示</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
