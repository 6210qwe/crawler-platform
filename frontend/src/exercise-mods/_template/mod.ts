import type { ExerciseMod, PrepareContext, SignInput, SignResult } from '../types'

const mod: ExerciseMod = {
  version: '1.0.0',
  async prepare(ctx: PrepareContext) {
    // 可在此做前端准备计算，或直接返回空对象
    return {}
  },
  async signRequest(input: SignInput): Promise<SignResult> {
    const timestamp = Math.floor(Date.now() / 1000)
    // 示例：简单把答案和时间拼接，真实题目应实现自己的加密/签名
    const payload = { a: input.answer, t: input.timeSpent }
    const sign = btoa(`${input.answer}:${input.timeSpent}:${timestamp}`)
    return { version: '1.0.0', payload, sign, timestamp }
  },
  renderHints() {
    return null
  },
}

export default mod


