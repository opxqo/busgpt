<template>
  <article class="ride-card hover-lift">
    <div class="card-top">
      <span class="product-chip" :class="ride.product">{{ productLabel }}</span>
      <span class="status-chip" :class="ride.status">{{ statusLabel }}</span>
    </div>

    <div class="card-body">
      <router-link :to="`/ride/${ride.id}`" class="title-link">
        {{ ride.title }}
      </router-link>
      <p class="description">{{ ride.description || '车主暂未补充公开说明，支付信息服务费后可查看联系方式。' }}</p>
    </div>

    <div class="price-row">
      <div class="price-item">
        <span class="meta-label">车位租金</span>
        <strong class="seat-price">¥{{ formatMoney(ride.price_per_month) }}<small>/月</small></strong>
      </div>
      <div class="divider"></div>
      <div class="price-item unlock-fee">
        <span class="meta-label">信息解锁费</span>
        <strong>¥{{ formatMoney(ride.contact_price) }}</strong>
      </div>
    </div>

    <div class="facts">
      <div class="fact-item">
        <Users :size="14" class="fact-icon" />
        <span>已拼 {{ occupiedSeats }}/{{ ride.total_seats }} 人</span>
      </div>
      <div class="fact-item">
        <Armchair :size="14" class="fact-icon" />
        <span>还差 {{ remainingSeats }} 人</span>
      </div>
      <div class="fact-item">
        <CalendarClock :size="14" class="fact-icon" />
        <span>{{ ride.duration }}个月</span>
      </div>
    </div>

    <div class="seller-row">
      <div class="seller">
        <img :src="ride.owner?.avatar || defaultAvatar" alt="车主头像" class="avatar" />
        <div class="seller-info">
          <strong>{{ ride.owner?.nickname || '车主' }}</strong>
          <span class="verified-tag">已认证车主</span>
        </div>
      </div>
      <router-link :to="`/ride/${ride.id}`" class="detail-btn">
        <span>立即搭车</span>
        <ChevronRight :size="15" />
      </router-link>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Armchair, CalendarClock, ChevronRight, Users } from '@lucide/vue'
import type { Ride } from '../../types'

const props = defineProps<{
  ride: Ride
}>()

const defaultAvatar = `https://api.dicebear.com/7.x/initials/svg?seed=${props.ride.owner_id}&backgroundColor=0f172a`

const productLabel = computed(() => {
  if (props.ride.product === 'chatgpt-team') return 'Team 协作'
  if (props.ride.product === 'chatgpt-pro') return 'Pro 极客'
  return 'Plus 拼车'
})

const statusLabel = computed(() => {
  if (props.ride.status === 'closed') return '已关闭'
  if (props.ride.status === 'expired') return '已过期'
  return '可解锁'
})

const occupiedSeats = computed(() => Number(props.ride.purchase_count || 0))
const remainingSeats = computed(() => Math.max(Number(props.ride.remaining_seats ?? props.ride.total_seats), 0))

const formatMoney = (value: number | string) => Math.round(Number(value || 0))
</script>

<style scoped>
.ride-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  background: var(--bg-secondary);
  box-shadow: var(--card-shadow);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal), border-color var(--transition-normal);
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.title-link {
  color: var(--text-primary);
  font-size: 17px;
  font-weight: 800;
  line-height: 1.4;
  text-decoration: none;
  letter-spacing: -0.01em;
  transition: color var(--transition-fast);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.title-link:hover {
  color: #3b82f6; /* Blue highlight on hover */
}

.description {
  display: -webkit-box;
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  margin: 0;
}

.price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  margin-bottom: var(--spacing-md);
}

.price-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.divider {
  width: 1px;
  height: 28px;
  background: var(--border-color);
}

.meta-label {
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.seat-price {
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 800;
  line-height: 1;
}

.seat-price small {
  color: var(--text-secondary);
  font-size: 11px;
  font-weight: 600;
}

.unlock-fee {
  text-align: right;
}

.unlock-fee strong {
  color: var(--color-pro); /* Purple/Violet color */
  font-size: 20px;
  font-weight: 800;
  line-height: 1;
}

.facts {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-lg);
  padding: 0 var(--spacing-xs);
}

.fact-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
}

.fact-icon {
  color: var(--text-muted);
}

.seller-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.seller {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  min-width: 0;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-full);
  border: 1px solid var(--border-color);
}

.seller-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.seller-info strong {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.verified-tag {
  color: #10b981; /* Green verified tag */
  font-size: 10px;
  font-weight: 700;
}

.detail-btn {
  display: inline-flex;
  height: 34px;
  align-items: center;
  gap: 4px;
  padding: 0 12px;
  border-radius: var(--border-radius-sm);
  background: var(--color-primary);
  color: var(--text-inverse);
  font-size: 12px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
  transition: all var(--transition-fast);
}

.detail-btn:hover {
  background: var(--color-primary-hover);
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.12);
}

.detail-btn:active {
  transform: scale(0.96);
}
</style>
