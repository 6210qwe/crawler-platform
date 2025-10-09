// 题目加载器
import { ExerciseMod, ExerciseData } from './types'

class ExerciseLoader {
  private static instance: ExerciseLoader
  private exerciseModules: Map<number, ExerciseMod> = new Map()
  private loadedModules: Set<number> = new Set()

  private constructor() {}

  static getInstance(): ExerciseLoader {
    if (!ExerciseLoader.instance) {
      ExerciseLoader.instance = new ExerciseLoader()
    }
    return ExerciseLoader.instance
  }

  // 加载单个题目模块
  async loadExercise(exerciseId: number): Promise<ExerciseMod | null> {
    if (this.exerciseModules.has(exerciseId)) {
      return this.exerciseModules.get(exerciseId)!
    }

    if (this.loadedModules.has(exerciseId)) {
      return null // 已经尝试加载过但失败了
    }

    try {
      // 动态导入题目模块
      const module = await import(`./${exerciseId}/mod.ts`)
      const exerciseMod: ExerciseMod = module.default
      
      // 验证模块结构
      if (!this.validateModule(exerciseMod)) {
        console.warn(`Exercise ${exerciseId} module validation failed`)
        this.loadedModules.add(exerciseId)
        return null
      }

      this.exerciseModules.set(exerciseId, exerciseMod)
      return exerciseMod
    } catch (error) {
      console.warn(`Failed to load exercise ${exerciseId}:`, error)
      this.loadedModules.add(exerciseId)
      return null
    }
  }

  // 获取已加载的题目模块
  getExercise(exerciseId: number): ExerciseMod | null {
    return this.exerciseModules.get(exerciseId) || null
  }

  // 获取所有已加载的题目
  getAllExercises(): ExerciseMod[] {
    return Array.from(this.exerciseModules.values())
  }

  // 预加载多个题目
  async preloadExercises(exerciseIds: number[]): Promise<void> {
    const loadPromises = exerciseIds.map(id => this.loadExercise(id))
    await Promise.allSettled(loadPromises)
  }

  // 验证模块结构
  private validateModule(module: any): module is ExerciseMod {
    return (
      module &&
      typeof module.id === 'number' &&
      typeof module.title === 'string' &&
      typeof module.description === 'string' &&
      typeof module.difficulty === 'string'
    )
  }

  // 清除缓存
  clearCache(): void {
    this.exerciseModules.clear()
    this.loadedModules.clear()
  }
}

export default ExerciseLoader

