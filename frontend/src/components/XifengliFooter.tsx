import { Heart, ArrowUp } from 'lucide-react'

const CrawlerFooter: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <footer className="bg-white border-t border-gray-200 mt-12">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* 网站信息 */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">关于本站</h3>
            <div className="space-y-2 text-sm text-gray-600">
              <p>爬虫工具平台 - 专业爬虫技术学习</p>
              <p>专注于爬虫技术与逆向工程</p>
              <p>分享实用的爬虫工具和技巧</p>
            </div>
          </div>

          {/* 快速链接 */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">快速链接</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <a href="/" className="text-gray-600 hover:text-blue-600">首页</a>
              <a href="/exercises" className="text-gray-600 hover:text-blue-600">爬虫工具</a>
              <a href="/notes" className="text-gray-600 hover:text-blue-600">技术笔记</a>
              <a href="/dashboard" className="text-gray-600 hover:text-blue-600">数据采集</a>
              <a href="/profile" className="text-gray-600 hover:text-blue-600">个人中心</a>
              <a href="/leaderboard" className="text-gray-600 hover:text-blue-600">技术分享</a>
            </div>
          </div>

          {/* 联系信息 */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">与我联系</h3>
            <div className="space-y-2 text-sm text-gray-600">
              <p>QQ: 123456789</p>
              <p>微信: crawler2024</p>
              <p>邮箱: contact@crawler-tools.com</p>
            </div>
          </div>
        </div>

        {/* 版权信息 */}
        <div className="border-t border-gray-200 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-sm text-gray-600 mb-4 md:mb-0">
              <p>Copyright © 2024-2025 爬虫工具平台 All Rights Reserved</p>
              <p>专注于爬虫技术学习与工具分享</p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1 text-sm text-gray-600">
                <Heart className="h-4 w-4 text-red-500" />
                <span>浏览：3,763,271 次</span>
              </div>
              
              <button
                onClick={scrollToTop}
                className="flex items-center space-x-1 text-sm text-gray-600 hover:text-blue-600 transition-colors"
              >
                <ArrowUp className="h-4 w-4" />
                <span>返回顶部</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default CrawlerFooter

