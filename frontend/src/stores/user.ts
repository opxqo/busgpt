import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/auth'
import type { User } from '../types'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function init() {
    if (token.value && !user.value) {
      loading.value = true
      try {
        const response = await authApi.getMe()
        user.value = response.data
      } catch (err) {
        console.error('Failed to load user profile on init', err)
        logout()
      } finally {
        loading.value = false
      }
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.login(email, password)
      const accessToken = response.data.access_token
      token.value = accessToken
      localStorage.setItem('token', accessToken)

      const userProfile = await authApi.getMe()
      user.value = userProfile.data
      localStorage.setItem('user', JSON.stringify(userProfile.data))

      return true
    } catch (err) {
      const errorVal = err as { response?: { data?: { detail?: string } } }
      error.value = errorVal.response?.data?.detail || '登录失败，请检查账号密码'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(email: string, nickname: string, password: string) {
    loading.value = true
    error.value = null
    try {
      await authApi.register(email, nickname, password)
      // Registration succeeds — user must activate email before login
      return true
    } catch (err) {
      const errorVal = err as { response?: { data?: { detail?: string } } }
      error.value = errorVal.response?.data?.detail || '注册失败，请检查输入'
      return false
    } finally {
      loading.value = false
    }
  }

  async function activate(token: string) {
    loading.value = true
    error.value = null
    try {
      await authApi.activate(token)
      return true
    } catch (err) {
      const errorVal = err as { response?: { data?: { detail?: string } } }
      error.value = errorVal.response?.data?.detail || '激活失败'
      return false
    } finally {
      loading.value = false
    }
  }

  async function resendActivation(email: string) {
    loading.value = true
    error.value = null
    try {
      await authApi.resendActivation(email)
      return true
    } catch (err) {
      const errorVal = err as { response?: { data?: { detail?: string } } }
      error.value = errorVal.response?.data?.detail || '重发失败'
      return false
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function updateProfile(nickname?: string, avatar?: string) {
    loading.value = true
    try {
      const response = await authApi.updateProfile(nickname, avatar)
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
      return true
    } catch (err) {
      const errorVal = err as { response?: { data?: { detail?: string } } }
      error.value = errorVal.response?.data?.detail || '修改资料失败'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isLoggedIn,
    isAdmin,
    init,
    login,
    register,
    activate,
    resendActivation,
    logout,
    updateProfile,
  }
})
