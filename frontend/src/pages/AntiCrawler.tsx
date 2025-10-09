import { Shield, Lock, Eye, Zap } from 'lucide-react'

export default function AntiCrawler() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">反爬技术</h1>
        <p className="text-xl text-gray-600">了解现代反爬虫技术，提升爬虫对抗能力</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Shield className="h-8 w-8 text-blue-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">验证码识别</h3>
          </div>
          <p className="text-gray-600 mb-4">突破各种验证码防护机制</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 图形验证码识别</div>
            <div className="text-sm text-gray-500">• 滑块验证码</div>
            <div className="text-sm text-gray-500">• 点选验证码</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Lock className="h-8 w-8 text-green-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">加密防护</h3>
          </div>
          <p className="text-gray-600 mb-4">分析并绕过各种加密保护措施</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• JavaScript 加密</div>
            <div className="text-sm text-gray-500">• 参数签名验证</div>
            <div className="text-sm text-gray-500">• Token 动态生成</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Eye className="h-8 w-8 text-purple-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">行为检测</h3>
          </div>
          <p className="text-gray-600 mb-4">模拟真实用户行为，绕过行为检测</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 鼠标轨迹模拟</div>
            <div className="text-sm text-gray-500">• 键盘输入模拟</div>
            <div className="text-sm text-gray-500">• 页面停留时间</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Zap className="h-8 w-8 text-orange-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">IP限制</h3>
          </div>
          <p className="text-gray-600 mb-4">突破IP限制和频率控制</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 代理IP池</div>
            <div className="text-sm text-gray-500">• IP轮换策略</div>
            <div className="text-sm text-gray-500">• 请求频率控制</div>
          </div>
        </div>
      </div>

      <div className="mt-12 bg-gradient-to-r from-red-50 to-pink-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">对抗策略</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">技术手段</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 浏览器指纹伪造</li>
              <li>• User-Agent 轮换</li>
              <li>• Cookie 管理策略</li>
              <li>• 请求头伪装</li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">高级技巧</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 分布式爬虫架构</li>
              <li>• 机器学习识别</li>
              <li>• 深度学习破解</li>
              <li>• 人工干预策略</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
