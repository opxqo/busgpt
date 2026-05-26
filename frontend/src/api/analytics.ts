import apiClient from './client'

export interface SalesOverview {
  total_revenue: number
  paid_orders: number
  active_rides: number
  new_rides: number
  average_order_amount: number
}

export interface PlatformStats {
  total_users: number
  active_rides: number
  total_rides: number
}

export interface PriceTrendPoint {
  date: string
  product: string
  ride_count: number
  average_price_per_month: number
  average_contact_price: number
  minimum_price_per_month: number
  maximum_price_per_month: number
}

export interface RideRankingItem {
  ride_id: number
  ride_title: string
  product: string
  orders: number
  revenue: number
  total_seats: number
  recruit_seats: number
  remaining_seats: number
  status: string
  owner_id: number
  owner_nickname?: string
}

export interface ProductRankingItem {
  product: string
  product_label: string
  orders: number
  revenue: number
  average_order_amount: number
}

export interface GmvByProduct {
  product: string
  product_label: string
  exercised_gmv: number
  potential_gmv: number
  remaining_gmv: number
  exercised_count: number
  potential_count: number
  ride_count: number
}

export interface GmvResponse {
  exercised_gmv: number
  potential_gmv: number
  remaining_gmv: number
  benchmark_gmv: number
  exercised_count: number
  potential_count: number
  active_rides: number
  by_product: GmvByProduct[]
}

export const analyticsApi = {
  getPlatformStats() {
    return apiClient.get<PlatformStats>('/analytics/platform/stats')
  },

  getSalesOverview(days = 30) {
    return apiClient.get<SalesOverview>('/analytics/sales/overview', { params: { days } })
  },

  getPriceTrends(days = 180) {
    return apiClient.get<PriceTrendPoint[]>('/analytics/prices/trends', { params: { days } })
  },

  getRideRankings(days = 30, limit = 5) {
    return apiClient.get<RideRankingItem[]>('/analytics/rankings/rides', { params: { days, limit } })
  },

  getProductRankings(days = 30, limit = 10) {
    return apiClient.get<ProductRankingItem[]>('/analytics/rankings/products', { params: { days, limit } })
  },

  getGmv() {
    return apiClient.get<GmvResponse>('/analytics/gmv')
  },
}
