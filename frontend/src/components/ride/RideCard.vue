<template>
  <article class="ride-card">
    <div class="card-top">
      <span class="product-chip" :class="ride.product">{{ productLabel }}</span>
      <span class="status-chip" :class="ride.status">{{ statusLabel }}</span>
    </div>

    <router-link :to="`/ride/${ride.id}`" class="title-link">
      {{ ride.title }}
    </router-link>
    <p class="description">{{ ride.description || '车主暂未补充公开说明，支付信息服务费后可查看联系方式。' }}</p>

    <div class="price-row">
      <div>
        <span class="meta-label">车位月费</span>
        <strong class="seat-price">¥{{ formatMoney(ride.price_per_month) }}<small>/月</small></strong>
      </div>
      <div class="unlock-fee">
        <span>信息服务费</span>
        <strong>¥{{ formatMoney(ride.contact_price) }}</strong>
      </div>
    </div>

    <div class="facts">
      <span><Users :size="14" /> 已拼 {{ occupiedSeats }} 人</span>
      <span><Armchair :size="14" /> 还差 {{ remainingSeats }} 人</span>
      <span><CalendarClock :size="14" /> {{ ride.duration }} 个月</span>
      <span><Clock3 :size="14" /> {{ formattedDate }}</span>
    </div>

    <div class="seller-row">
      <div class="seller">
        <img :src="ride.owner?.avatar || defaultAvatar" alt="车主头像" class="avatar" />
        <span>
          <strong>{{ ride.owner?.nickname || '车主' }}</strong>
          <small>车主已验证</small>
        </span>
      </div>
      <router-link :to="`/ride/${ride.id}`" class="detail-btn">
        查看详情
        <ChevronRight :size="15" />
      </router-link>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Armchair, CalendarClock, ChevronRight, Clock3, Users } from '@lucide/vue'
import type { Ride } from '../../types'

const props = defineProps<{
  ride: Ride
}>()

const defaultAvatar = `https://api.dicebear.com/7.x/initials/svg?seed=${props.ride.owner_id}`

const productLabel = computed(() => {
  if (props.ride.product === 'chatgpt-team') return 'Team 协作位'
  if (props.ride.product === 'chatgpt-pro') return 'Pro 高阶位'
  return 'Plus 拼车位'
})

const statusLabel = computed(() => {
  if (props.ride.status === 'closed') return '已关闭'
  if (props.ride.status === 'expired') return '已过期'
  return '可解锁'
})

const occupiedSeats = computed(() => Number(props.ride.purchase_count || 0))
const remainingSeats = computed(() => Math.max(Number(props.ride.remaining_seats ?? props.ride.total_seats), 0))

const formattedDate = computed(() => {
  const date = new Date(props.ride.created_at)
  return `${date.getMonth() + 1}月${date.getDate()}日更新`
})

const formatMoney = (value: number | string) => Math.round(Number(value || 0))
</script>

<style scoped>
.ride-card {
  display: flex;
  min-height: 268px;
  flex-direction: column;
  gap: 14px;
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  background: var(--bg-secondary);
  box-shadow: var(--card-shadow);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast), transform var(--transition-fast);
}

.ride-card:hover {
  border-color: var(--border-color-hover);
  box-shadow: var(--card-shadow-hover);
  transform: translateY(-2px);
}

.card-top,
.price-row,
.seller-row,
.facts {
  display: flex;
  align-items: center;
}

.card-top,
.seller-row {
  justify-content: space-between;
  gap: var(--spacing-sm);
}

.title-link {
  color: var(--text-primary);
  font-size: 17px;
  font-weight: 900;
  line-height: 1.4;
}

.description {
  display: -webkit-box;
  min-height: 42px;
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.price-row {
  justify-content: space-between;
  gap: var(--spacing-md);
  padding: 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.meta-label,
.unlock-fee span {
  display: block;
  margin-bottom: 3px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
}

.seat-price {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 900;
  line-height: 1;
}

.seat-price small {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 700;
}

.unlock-fee {
  min-width: 92px;
  text-align: right;
}

.unlock-fee strong {
  color: var(--color-pro);
  font-size: 18px;
  font-weight: 900;
}

.facts {
  flex-wrap: wrap;
  gap: 8px;
}

.facts span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 700;
}

.seller {
  display: grid;
  min-width: 0;
  grid-template-columns: auto 1fr;
  gap: 9px;
  align-items: center;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
}

.seller span {
  display: flex;
  min-width: 0;
  flex-direction: column;
}

.seller strong {
  overflow: hidden;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.seller small {
  color: var(--color-info);
  font-size: 11px;
  font-weight: 800;
}

.detail-btn {
  display: inline-flex;
  min-height: 36px;
  align-items: center;
  gap: 4px;
  padding: 0 11px;
  border-radius: var(--border-radius-md);
  background: var(--color-primary);
  color: var(--text-inverse);
  font-size: 13px;
  font-weight: 900;
  white-space: nowrap;
}
</style>
