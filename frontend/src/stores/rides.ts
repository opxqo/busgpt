import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ridesApi } from '../api/rides'
import type { Ride, Product, ProductType } from '../types'

export const useRidesStore = defineStore('rides', () => {
  const products = ref<Product[]>([])
  const rides = ref<Ride[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchProducts() {
    try {
      const res = await ridesApi.getProducts()
      products.value = res.data
    } catch (err) {
      console.error('Failed to fetch products', err)
    }
  }

  async function fetchRides(filters: { product?: ProductType | ''; status_filter?: string; query?: string } = {}) {
    loading.value = true
    error.value = null
    try {
      const res = await ridesApi.getRides(filters)
      rides.value = res.data
    } catch (err) {
      const errorVal = err as { response?: { data?: { detail?: string } } }
      error.value = errorVal.response?.data?.detail || '获取车位列表失败'
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    rides,
    loading,
    error,
    fetchProducts,
    fetchRides,
  }
})
