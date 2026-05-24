import apiClient from './client'

export const authApi = {
  register(email: string, nickname: string, password: string) {
    return apiClient.post('/auth/register', { email, nickname, password })
  },

  login(email: string, password: string) {
    return apiClient.post('/auth/login', { email, password })
  },

  getMe() {
    return apiClient.get('/auth/me')
  },

  activate(token: string) {
    return apiClient.get(`/auth/activate?token=${encodeURIComponent(token)}`)
  },

  resendActivation(email: string) {
    return apiClient.post('/auth/resend-activation', { email })
  },

  updateProfile(nickname?: string, avatar?: string) {
    return apiClient.put('/users/me', { nickname, avatar })
  },

  changePassword(currentPassword: string, newPassword: string) {
    return apiClient.put('/users/me/password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  },
}
