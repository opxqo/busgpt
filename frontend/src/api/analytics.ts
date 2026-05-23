import apiClient from './client'

export interface SalesOverview {
  total_revenue: number
  paid_orders: number
  active_rides: number
  new_rides: number
  average_order_amount: number
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

export const analyticsApi = {
  getSalesOverview(days = 30) {
    return apiClient.get<SalesOverview>('/analytics/sales/overview', { params: { days } })
  },

  getPriceTrends(days = 180) {
    return apiClient.get<PriceTrendPoint[]>('/analytics/prices/trends', { params: { days } })
  },

  getRideRankings(days = 30, limit = 5) {
    return apiClient.get<RideRankingItem[]>('/analytics/rankings/rides', { params: { days, limit } })
  },
}
