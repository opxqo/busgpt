import apiClient from './client'
import type {
  AdminOverview,
  AdminUserListItem,
  AdminRideListItem,
  AdminOrderListItem,
} from '../types'

export interface PaginatedResponse<T> {
  items: T[]
  total: number
}

export const adminApi = {
  getOverview() {
    return apiClient.get<AdminOverview>('/admin/overview')
  },

  getUsers(params: { skip?: number; limit?: number; search?: string; role?: string }) {
    return apiClient.get<PaginatedResponse<AdminUserListItem>>('/admin/users', { params })
  },

  getUserDetail(userId: number) {
    return apiClient.get<AdminUserListItem>(`/admin/users/${userId}`)
  },

  updateUserStatus(userId: number, isActive: boolean) {
    return apiClient.put(`/admin/users/${userId}/status`, { is_active: isActive })
  },

  getRides(params: {
    skip?: number
    limit?: number
    search?: string
    product?: string
    status?: string
  }) {
    return apiClient.get<PaginatedResponse<AdminRideListItem>>('/admin/rides', { params })
  },

  updateRideStatus(rideId: number, newStatus: string) {
    return apiClient.put(`/admin/rides/${rideId}/status`, { status: newStatus })
  },

  deleteRide(rideId: number) {
    return apiClient.delete(`/admin/rides/${rideId}`)
  },

  getOrders(params: { skip?: number; limit?: number; status?: string; search?: string }) {
    return apiClient.get<PaginatedResponse<AdminOrderListItem>>('/admin/orders', { params })
  },
}
