import type { ExerciseMod, PrepareContext, SignInput, SignResult } from '../types'
import CryptoJS from 'crypto-js'
import React from 'react'

const mod: ExerciseMod = {
  version: '1.0.0',
  
  async prepare(ctx: PrepareContext) {
    // 可在此做前端准备计算，或直接返回空对象
    const timestamp = Math.floor(Date.now() / 1000)
    return {
      timestamp,
      hint: '这是题目模板，请根据实际需求修改'
    }
  },
  
  async signRequest(input: SignInput): Promise<SignResult> {
    const timestamp = Math.floor(Date.now() / 1000)
    
    // 示例：简单把答案和时间拼接，真实题目应实现自己的加密/签名
    const payload = { 
      answer: input.answer, 
      timeSpent: input.timeSpent,
      timestamp 
    }
    
    // 使用MD5签名（示例）
    const rawString = `${input.answer}:${input.timeSpent}:${timestamp}:template`
    const sign = CryptoJS.MD5(rawString).toString()
    
    return { 
      version: '1.0.0', 
      payload, 
      sign, 
      timestamp 
    }
  },
  
  renderHints() {
    return React.createElement('div', { className: 'bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4' }, [
      React.createElement('div', { key: 'content', className: 'flex items-start' }, [
        React.createElement('div', { key: 'icon', className: 'flex-shrink-0' }, 
          React.createElement('svg', { 
            className: 'h-5 w-5 text-gray-400', 
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
          React.createElement('h3', { key: 'title', className: 'text-sm font-medium text-gray-800' }, '题目模板'),
          React.createElement('div', { key: 'desc', className: 'mt-2 text-sm text-gray-700' }, [
            React.createElement('p', { key: 'p1' }, '这是题目模板，请根据实际需求修改：'),
            React.createElement('ul', { key: 'list', className: 'mt-1 list-disc list-inside space-y-1' }, [
              React.createElement('li', { key: 'li1' }, '修改 prepare 方法返回题目特定参数'),
              React.createElement('li', { key: 'li2' }, '修改 signRequest 方法实现签名逻辑'),
              React.createElement('li', { key: 'li3' }, '修改 renderHints 方法显示题目提示'),
              React.createElement('li', { key: 'li4' }, '创建对应的后端验证器')
            ])
          ])
        ])
      ])
    ])
  }
}

export default mod