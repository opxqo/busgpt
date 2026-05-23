import apiClient from './client'

export const authApi = {
  register(phone: string, nickname: string, password: string) {
    return apiClient.post('/auth/register', { phone, nickname, password })
  },
  
  login(phone: string, password: string) {
    return apiClient.post('/auth/login', { phone, password })
  },
  
  getMe() {
    return apiClient.get('/auth/me')
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
