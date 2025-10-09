import { Database, Download, BarChart3, Globe } from 'lucide-react'

export default function DataCollection() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">数据采集</h1>
        <p className="text-xl text-gray-600">高效、稳定、智能的数据采集解决方案</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Database className="h-8 w-8 text-blue-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">数据库采集</h3>
          </div>
          <p className="text-gray-600 mb-4">从各种数据库系统中采集结构化数据</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• MySQL/PostgreSQL 连接</div>
            <div className="text-sm text-gray-500">• MongoDB 文档采集</div>
            <div className="text-sm text-gray-500">• Redis 缓存数据</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Globe className="h-8 w-8 text-green-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">网页采集</h3>
          </div>
          <p className="text-gray-600 mb-4">智能爬取网页内容，支持动态加载和反爬机制</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• 静态页面抓取</div>
            <div className="text-sm text-gray-500">• 动态内容渲染</div>
            <div className="text-sm text-gray-500">• 图片/文件下载</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <BarChart3 className="h-8 w-8 text-purple-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">API接口</h3>
          </div>
          <p className="text-gray-600 mb-4">通过API接口获取数据，支持各种认证方式</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• RESTful API</div>
            <div className="text-sm text-gray-500">• GraphQL 查询</div>
            <div className="text-sm text-gray-500">• OAuth 认证</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center mb-4">
            <Download className="h-8 w-8 text-orange-600 mr-3" />
            <h3 className="text-xl font-semibold text-gray-900">文件处理</h3>
          </div>
          <p className="text-gray-600 mb-4">处理各种格式的文件和数据</p>
          <div className="space-y-2">
            <div className="text-sm text-gray-500">• Excel/CSV 解析</div>
            <div className="text-sm text-gray-500">• PDF 文本提取</div>
            <div className="text-sm text-gray-500">• JSON/XML 处理</div>
          </div>
        </div>
      </div>

      <div className="mt-12 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">采集策略</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">技术方案</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 分布式爬虫架构</li>
              <li>• 代理池轮换机制</li>
              <li>• 智能重试策略</li>
              <li>• 数据去重算法</li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-3">性能优化</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 并发控制优化</li>
              <li>• 内存使用管理</li>
              <li>• 网络请求优化</li>
              <li>• 存储效率提升</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
