import apiClient from './client'

export const ordersApi = {
  /** Purchase contact info for a ride */
  purchaseContact(rideId: number) {
    return apiClient.post('/orders', { ride_id: rideId })
  },

  /** Get my purchase history */
  getMyOrders() {
    return apiClient.get('/orders/mine')
  },

  /** Check if I've purchased a specific ride */
  checkPurchased(rideId: number) {
    return apiClient.get(`/orders/check/${rideId}`)
  },

  /** Get sales records for my rides (as owner) */
  getMySales() {
    return apiClient.get('/my/rides/sales')
  },
}
