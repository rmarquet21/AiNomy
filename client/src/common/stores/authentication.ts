import { defineStore } from 'pinia'

interface AuthState {
  token: string | null
  address: string | null
}

export const useAuthStore = defineStore({
  id: 'auth',
  state: (): AuthState => ({
    token: localStorage.getItem('token') || null,
    address: localStorage.getItem('address') || null
  }),
  actions: {
    setUser(token: string, address: string) {
      this.token = token
      this.address = address
      localStorage.setItem('token', token)
      localStorage.setItem('address', address)
    },
    clearToken() {
      this.token = null
      this.address = null
      localStorage.removeItem('token')
      localStorage.removeItem('address')
    },
  },
})