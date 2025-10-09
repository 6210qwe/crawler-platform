import { Code, Shield, Eye, Search } from 'lucide-react'

export default function ReverseAnalysis() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">逆向分析</h1>
        <p className="text-xl text-gray-600">深入分析网络协议、加密算法和安全机制</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Code className="h-8 w-8 text-blue-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">协议分析</h3>
          </div>
          <p className="text-gray-600 mb-4">分析HTTP、HTTPS、WebSocket等网络协议的数据包结构和通信机制</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• HTTP/HTTPS 协议解析</div>
            <div className="text-sm text-gray-500">• WebSocket 实时通信</div>
            <div className="text-sm text-gray-500">• API 接口逆向</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Shield className="h-8 w-8 text-green-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">加密算法</h3>
          </div>
          <p className="text-gray-600 mb-4">研究各种加密算法的实现原理和破解方法</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• AES/DES 对称加密</div>
            <div className="text-sm text-gray-500">• RSA 非对称加密</div>
            <div className="text-sm text-gray-500">• 哈希算法分析</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Eye className="h-8 w-8 text-purple-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">安全机制</h3>
          </div>
          <p className="text-gray-600 mb-4">分析网站的安全防护措施和绕过技术</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 反调试技术</div>
            <div className="text-sm text-gray-500">• 代码混淆分析</div>
            <div className="text-sm text-gray-500">• 安全策略绕过</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Search className="h-8 w-8 text-orange-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">漏洞挖掘</h3>
          </div>
          <p className="text-gray-600 mb-4">发现和分析Web应用中的安全漏洞</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• SQL注入漏洞</div>
            <div className="text-sm text-gray-500">• XSS跨站脚本</div>
            <div className="text-sm text-gray-500">• CSRF攻击防护</div>
          </div>
        </div>
      </div>

      <div className="mt-12 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">学习路径</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">基础阶段</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 网络协议基础</li>
              <li>• HTTP/HTTPS 详解</li>
              <li>• 浏览器开发者工具</li>
              <li>• 抓包工具使用</li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">进阶阶段</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• JavaScript逆向</li>
              <li>• 加密算法分析</li>
              <li>• 反调试技术</li>
              <li>• 自动化工具开发</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
