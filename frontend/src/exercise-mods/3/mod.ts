// 第三题：字体加密之迷雾
import type { ExerciseMod, PrepareContext, SignInput, SignResult } from '../types'
import CryptoJS from 'crypto-js'
import React from 'react'

const mod: ExerciseMod = {
  version: '3.0.0',
  
  async prepare(ctx: PrepareContext) {
    // 返回加密字体参数
    const timestamp = Math.floor(Date.now() / 1000)
    
    return {
      timestamp,
      hint: '使用Caesar算法，偏移量为13',
      algorithm: 'Caesar',
      shift: 13,
      cipherKey: 'ROT13'
    }
  },
  
  async signRequest(input: SignInput): Promise<SignResult> {
    const timestamp = Math.floor(Date.now() / 1000)
    const shift = 13
    const rawString = `${input.answer}:${input.timeSpent}:${timestamp}:${shift}:encrypted_font`
    const sign = CryptoJS.SHA256(rawString).toString()
    
    return {
      version: '3.0.0',
      payload: {
        answer: input.answer,
        timeSpent: input.timeSpent,
        timestamp,
        algorithm: 'Caesar',
        shift
      },
      sign,
      timestamp
    }
  },
  
  renderHints() {
    return React.createElement('div', { className: 'bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4' }, [
      React.createElement('div', { key: 'content', className: 'flex items-start' }, [
        React.createElement('div', { key: 'icon', className: 'flex-shrink-0' }, 
          React.createElement('svg', { 
            className: 'h-5 w-5 text-purple-400', 
            viewBox: '0 0 20 20', 
            fill: 'currentColor' 
          }, 
            React.createElement('path', { 
              fillRule: 'evenodd', 
              d: 'M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z', 
              clipRule: 'evenodd' 
            })
          )
        ),
        React.createElement('div', { key: 'text', className: 'ml-3' }, [
          React.createElement('h3', { key: 'title', className: 'text-sm font-medium text-purple-800' }, '加密字体提示'),
          React.createElement('div', { key: 'desc', className: 'mt-2 text-sm text-purple-700' }, [
            React.createElement('p', { key: 'p1' }, '字体数据已加密，需要解密：'),
            React.createElement('ul', { key: 'list', className: 'mt-1 list-disc list-inside space-y-1' }, [
              React.createElement('li', { key: 'li1' }, '算法：Caesar密码'),
              React.createElement('li', { key: 'li2' }, '偏移量：13'),
              React.createElement('li', { key: 'li3' }, '密钥：ROT13'),
              React.createElement('li', { key: 'li4' }, '需要先解密再计算数字总和')
            ])
          ])
        ])
      ])
    ])
  }
}

export default mod