import type { ExerciseMod, PrepareContext, SignInput, SignResult } from '../types'
import CryptoJS from 'crypto-js'

const mod: ExerciseMod = {
  version: '1.0.0',
  
  async prepare(ctx: PrepareContext) {
    // 返回当前时间戳，供前端生成 MD5 参数
    const timestamp = Math.floor(Date.now() / 1000)
    return { 
      timestamp,
      hint: '翻页时需要携带 MD5(timestamp + "spider") 参数'
    }
  },
  
  async signRequest(input: SignInput): Promise<SignResult> {
    const timestamp = Math.floor(Date.now() / 1000)
    const rawString = timestamp + 'spider'
    const md5Hash = CryptoJS.MD5(rawString).toString()
    
    return {
      version: '1.0.0',
      payload: {
        answer: input.answer,
        timeSpent: input.timeSpent,
        timestamp,
        md5Param: md5Hash
      },
      sign: md5Hash,
      timestamp
    }
  },
  
  renderHints() {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.726-1.36 3.491 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-yellow-800">题目提示</h3>
            <div className="mt-2 text-sm text-yellow-700">
              <p>翻页时需要携带 MD5 加密参数：</p>
              <code className="mt-1 block bg-yellow-100 px-2 py-1 rounded text-xs">
                MD5(当前时间戳 + "spider")
              </code>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default mod


