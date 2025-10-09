// 第二题：动态字体之变幻
import type { ExerciseMod, PrepareContext, SignInput, SignResult } from '../types'
import CryptoJS from 'crypto-js'
import React from 'react'

const mod: ExerciseMod = {
  version: '2.1.3',
  
  async prepare(ctx: PrepareContext) {
    // 返回动态字体参数
    const timestamp = Math.floor(Date.now() / 1000)
    const encodingKey = `dynamic_${timestamp}`
    
    return {
      timestamp,
      encodingKey,
      hint: '字体文件会动态变化，需要实时解析',
      algorithm: 'dynamic_font_encoding'
    }
  },
  
  async signRequest(input: SignInput): Promise<SignResult> {
    const timestamp = Math.floor(Date.now() / 1000)
    const encodingKey = `dynamic_${timestamp}`
    const rawString = `${input.answer}:${input.timeSpent}:${timestamp}:${encodingKey}:dynamic_font`
    const sign = CryptoJS.SHA256(rawString).toString()
    
    return {
      version: '2.1.3',
      payload: {
        answer: input.answer,
        timeSpent: input.timeSpent,
        timestamp,
        encodingKey
      },
      sign,
      timestamp
    }
  },
  
  renderHints() {
    return React.createElement('div', { className: 'bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4' }, [
      React.createElement('div', { key: 'content', className: 'flex items-start' }, [
        React.createElement('div', { key: 'icon', className: 'flex-shrink-0' }, 
          React.createElement('svg', { 
            className: 'h-5 w-5 text-blue-400', 
            viewBox: '0 0 20 20', 
            fill: 'currentColor' 
          }, 
            React.createElement('path', { 
              fillRule: 'evenodd', 
              d: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z', 
              clipRule: 'evenodd' 
            })
          )
        ),
        React.createElement('div', { key: 'text', className: 'ml-3' }, [
          React.createElement('h3', { key: 'title', className: 'text-sm font-medium text-blue-800' }, '动态字体提示'),
          React.createElement('div', { key: 'desc', className: 'mt-2 text-sm text-blue-700' }, [
            React.createElement('p', { key: 'p1' }, '动态字体需要实时解析：'),
            React.createElement('ul', { key: 'list', className: 'mt-1 list-disc list-inside space-y-1' }, [
              React.createElement('li', { key: 'li1' }, '字体文件会随时间变化'),
              React.createElement('li', { key: 'li2' }, '需要根据时间戳计算正确的数字'),
              React.createElement('li', { key: 'li3' }, '使用动态编码密钥进行验证')
            ])
          ])
        ])
      ])
    ])
  }
}

export default mod