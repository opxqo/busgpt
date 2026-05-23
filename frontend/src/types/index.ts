export interface User {
  id: number
  phone: string
  nickname: string
  avatar: string
  role: 'user' | 'admin'
  created_at: string
}

export type ContactType = 'email' | 'wechat' | 'telegram'

export type ProductType = 'chatgpt-plus' | 'chatgpt-team' | 'chatgpt-pro'

export interface Product {
  type: ProductType
  label: string
  official_price: number
  color: string
  max_seats: number
  description: string
}

export interface Ride {
  id: number
  title: string
  product: ProductType
  owner_id: number
  total_seats: number
  price_per_month: number
  duration: number
  warranty_days: number
  description: string
  contact_price: number
  contact_info?: string  // Only available after purchase or for owner
  is_purchased?: boolean
  purchase_count?: number
  remaining_seats?: number
  status: 'open' | 'closed' | 'expired'
  created_at: string
  expires_at: string
  owner: User
  product_details?: Product
}

export interface Order {
  id: number
  user_id: number
  ride_id: number
  amount: number
  status: 'paid' | 'refunded'
  created_at: string
  ride_title?: string
  ride_product?: string
  ride_price_per_month?: number
  ride_duration?: number
  ride_total_seats?: number
  ride_purchase_count?: number
  ride_remaining_seats?: number
  ride_status?: 'open' | 'closed' | 'expired' | 'deleted'
  ride_contact_info?: string
  ride_owner?: User
}
