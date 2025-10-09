import { Download, Wrench, Package, Settings } from 'lucide-react'

export default function ToolsDownload() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">工具下载</h1>
        <p className="text-xl text-gray-600">下载各种爬虫开发工具和实用软件</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Download className="h-8 w-8 text-blue-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">爬虫框架</h3>
          </div>
          <p className="text-gray-600 mb-4">各种爬虫开发框架和库</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• Scrapy 框架</div>
            <div className="text-sm text-gray-500">• Selenium 自动化</div>
            <div className="text-sm text-gray-500">• Requests 库</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Wrench className="h-8 w-8 text-green-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">开发工具</h3>
          </div>
          <p className="text-gray-600 mb-4">爬虫开发必备的工具软件</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• Chrome DevTools</div>
            <div className="text-sm text-gray-500">• Postman API测试</div>
            <div className="text-sm text-gray-500">• Fiddler 抓包工具</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Package className="h-8 w-8 text-purple-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">扩展插件</h3>
          </div>
          <p className="text-gray-600 mb-4">浏览器扩展和实用插件</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 爬虫助手插件</div>
            <div className="text-sm text-gray-500">• 数据提取工具</div>
            <div className="text-sm text-gray-500">• 反反爬插件</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Settings className="h-8 w-8 text-orange-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">配置工具</h3>
          </div>
          <p className="text-gray-600 mb-4">环境配置和部署工具</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• Docker 容器</div>
            <div className="text-sm text-gray-500">• 环境配置脚本</div>
            <div className="text-sm text-gray-500">• 部署工具</div>
          </div>
        </div>
      </div>

      <div className="mt-12 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">下载分类</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">开发环境</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Python 开发环境</li>
              <li>• Node.js 运行环境</li>
              <li>• Java 开发工具</li>
              <li>• 数据库管理工具</li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">实用工具</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 代理IP管理工具</li>
              <li>• 验证码识别工具</li>
              <li>• 数据清洗工具</li>
              <li>• 性能监控工具</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
