import type { Definition, Prediction } from '../src/types'
import { useAuthStore } from '~/common/stores/authentication'

const AUTH_SERVICE_URL = "/api/auth"
const ANALYSE_SERVICE_URL = "/api/analyse"

export const generateChallenge: any = async (address: string) => {
  const challengeReq: any = await fetch(`${AUTH_SERVICE_URL}/api/v1/auth/challenge`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      address,
    }),
  })
  if (challengeReq.ok) {
    const res = await challengeReq.json()
    return res.challenge
  }
  return 'something went wrong'
}

export const getAuthorization: any = async (address: string, signature: string) => {
  const tokenReq: any = await fetch(`${AUTH_SERVICE_URL}/api/v1/auth/authorize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      address,
      signature,
    }),
  })
  if (tokenReq.ok) {
    const res = await tokenReq.json()
    return res.token
  }
  return 'something went wrong'
}

// Analyse servide
export const getAnalyse: any = async (image: any, kind: string): Promise<Error | Array<Prediction>> => {
  const auth = useAuthStore()
  const analyseReq: any = await fetch(`${ANALYSE_SERVICE_URL}/api/v1/analyse?kind=${kind}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
    body: image,
  })
  return new Promise((resolve, reject) => {
    if (analyseReq.ok) {
      const res = analyseReq.json()
      resolve(res)
    }
    else {
      const error = new Error('La requête a échoué.')
      reject(error)
    }
  })
}

// Details service
export const getDetails: any = async (name: string): Promise<Error | Definition> => {
  const auth = useAuthStore()
  const detailsReq: any = await fetch(`${ANALYSE_SERVICE_URL}/api/v1/details?name=${name}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
  })
  return new Promise((resolve, reject) => {
    if (detailsReq.ok) {
      const res = detailsReq.json()
      resolve(res)
    }
    else {
      const error = new Error('La requête a échoué.')
      reject(error)
    }
  })
}

// Details service
export const getHistory: any = async (): Promise<Error | any> => {
  const auth = useAuthStore()
  const detailsReq: any = await fetch(`${ANALYSE_SERVICE_URL}/api/v1/analyse`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${auth.token}`,
    },
  })
  return new Promise((resolve, reject) => {
    if (detailsReq.ok) {
      const res = detailsReq.json()
      resolve(res)
    }
    else {
      const error = new Error('La requête a échoué.')
      reject(error)
    }
  })
}
