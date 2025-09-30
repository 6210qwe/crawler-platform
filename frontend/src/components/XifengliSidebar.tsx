import { Link } from 'react-router-dom'
import { Star, TrendingUp, Calendar, Tag, Heart } from 'lucide-react'

const CrawlerSidebar: React.FC = () => {
  const recommendedArticles = [
    { title: 'Python爬虫入门教程：从零开始学爬虫', date: '01-03', views: 15154 },
    { title: '反爬虫技术详解：如何绕过网站防护', date: '01-07', views: 9841 },
    { title: 'Selenium自动化爬虫实战案例', date: '11-25', views: 8993 },
  ]

  const hotArticles = [
    'Scrapy框架深度解析与实战应用',
    'JavaScript逆向工程入门指南',
    '爬虫数据存储与数据库设计',
    '代理IP池的构建与管理策略',
    '爬虫性能优化技巧总结',
  ]

  const tags = [
    'Python', '爬虫', 'Scrapy', 'Selenium', '反爬虫', '数据采集', 'JavaScript', '逆向工程', '代理IP', '数据库',
    'API', '自动化', '网页解析', '数据清洗', '分布式爬虫', '爬虫框架', '网络请求', '数据存储', '性能优化', '安全防护',
    '机器学习', '数据分析', '正则表达式', 'XPath', 'BeautifulSoup', 'requests', 'aiohttp', '多线程', '异步编程', '监控告警',
    '日志分析', '数据可视化', '爬虫调度', '任务队列', 'Redis', 'MongoDB', 'MySQL', 'Elasticsearch', 'Kafka', 'Docker',
    'Linux', 'Nginx', '负载均衡', '高可用', '容错处理', '重试机制', '限流策略', '反反爬虫', '验证码识别', '模拟登录'
  ]

  return (
    <div className="w-80 space-y-6">
      {/* 站长推荐 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Star className="h-5 w-5 text-yellow-500 mr-2" />
          热门推荐
        </h3>
        <div className="space-y-3">
          {recommendedArticles.map((article, index) => (
            <div key={index} className="border-b border-gray-100 pb-3 last:border-b-0">
              <Link 
                to="/notes" 
                className="text-sm text-gray-700 hover:text-blue-600 line-clamp-2 block mb-1"
              >
                {article.title}
              </Link>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{article.date}</span>
                <span>{article.views}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 热门文章 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <TrendingUp className="h-5 w-5 text-red-500 mr-2" />
          技术文章
        </h3>
        <div className="space-y-2">
          {hotArticles.map((article, index) => (
            <Link 
              key={index}
              to="/notes" 
              className="block text-sm text-gray-700 hover:text-blue-600 py-1"
            >
              {article}
            </Link>
          ))}
        </div>
      </div>

      {/* 文章归档 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Calendar className="h-5 w-5 text-blue-500 mr-2" />
          文章归档
        </h3>
        <div className="space-y-2">
          {['2025 年 09 月 (0)', '2025 年 08 月 (0)', '2025 年 07 月 (0)', '2025 年 06 月 (0)', '2025 年 05 月 (0)', '2025 年 04 月 (0)'].map((archive, index) => (
            <Link 
              key={index}
              to="/notes" 
              className="block text-sm text-gray-700 hover:text-blue-600 py-1"
            >
              {archive}
            </Link>
          ))}
        </div>
      </div>

      {/* 标签云 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Tag className="h-5 w-5 text-green-500 mr-2" />
          技术标签
        </h3>
        <div className="flex flex-wrap gap-2">
          {tags.map((tag, index) => (
            <Link 
              key={index}
              to="/notes" 
              className="text-xs bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 px-2 py-1 rounded transition-colors"
            >
              {tag}
            </Link>
          ))}
        </div>
      </div>

      {/* 与我联系 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Heart className="h-5 w-5 text-pink-500 mr-2" />
          与我联系
        </h3>
        <div className="space-y-2 text-sm text-gray-600">
          <div>QQ</div>
          <div>微信</div>
          <div>关于本站</div>
          <div>关于站长</div>
          <div>使用声明</div>
          <div>留言友链</div>
          <div>网站地图</div>
          <div>更新日志</div>
          <div>致敬开源</div>
        </div>
      </div>

      {/* 友链 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">友链</h3>
        <div className="space-y-2 text-sm">
          {['笛声', '龙笑天下', '一人夕', '沈唁志', '龙砚庭', '雅兮网', '雨落泪尽', '青山小站', '银色乐航', '闲鱼博客', '爱达导航', '博客志'].map((link, index) => (
            <Link 
              key={index}
              to="/notes" 
              className="block text-gray-700 hover:text-blue-600 py-1"
            >
              {link}
            </Link>
          ))}
        </div>
      </div>
    </div>
  )
}

export default CrawlerSidebar

