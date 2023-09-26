import type { ViteSSGContext } from 'vite-ssg'

export type UserModule = (ctx: ViteSSGContext) => void

export interface Prediction {
  label: string
  probability: number
}

export interface Definition {
  name: string
  description: string
  key_factors: KeyFactor[]
  category: string
  tags: Tag[]
  created_at: null
  updated_at: null
}
export interface History {
  ID: string
  Owner: string
  FileName: string
  Image: string
  Kind: string
  Prediction: Prediction[]
}

interface KeyFactor {
  name: string
}
interface Tag {
  name: string
  color: string
}
