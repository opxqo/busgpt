import apiClient from './client'
import type { Product, ProductType } from '../types'

export const ridesApi = {
  getProducts() {
    return apiClient.get('/products')
  },

  updateProduct(productType: ProductType, product: Omit<Product, 'type'>) {
    return apiClient.put(`/products/${productType}`, product)
  },

  getRides(filters: { product?: ProductType | ''; status_filter?: string; query?: string } = {}) {
    const params = new URLSearchParams()
    if (filters.product) params.append('product', filters.product)
    if (filters.status_filter) params.append('status_filter', filters.status_filter)
    if (filters.query) params.append('query', filters.query)
    
    return apiClient.get(`/rides?${params.toString()}`)
  },

  getRide(id: number) {
    return apiClient.get(`/rides/${id}`)
  },

  createRide(ride: {
    title: string
    product: ProductType
    total_seats: number
    price_per_month: number
    duration: number
    warranty_days: number
    description?: string
    contact_info: string
    contact_website?: string
    contact_price: number
  }) {
    return apiClient.post('/rides', ride)
  },

  updateRide(id: number, ride: {
    title?: string
    product?: ProductType
    total_seats?: number
    price_per_month?: number
    duration?: number
    warranty_days?: number
    description?: string
    contact_info?: string
    contact_website?: string
    contact_price?: number
    status?: string
  }) {
    return apiClient.put(`/rides/${id}`, ride)
  },

  deleteRide(id: number) {
    return apiClient.delete(`/rides/${id}`)
  },

  getMyOwnedRides() {
    return apiClient.get('/my/rides/owned')
  },
}
