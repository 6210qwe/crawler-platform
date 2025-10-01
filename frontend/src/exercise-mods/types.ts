export interface PrepareContext {
  userId?: number
  exerciseId: number
}

export interface SignInput {
  answer: number
  timeSpent: number
  prepareParams?: Record<string, any>
}

export interface SignResult {
  version?: string
  payload?: Record<string, any>
  sign?: string
  timestamp?: number
}

export interface ExerciseMod {
  version: string
  prepare?: (ctx: PrepareContext) => Promise<Record<string, any>> | Record<string, any>
  signRequest: (input: SignInput) => Promise<SignResult> | SignResult
  renderHints?: () => JSX.Element
}


