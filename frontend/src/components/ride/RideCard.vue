<template>
  <article class="ride-card hover-lift" :class="ride.product">
    <div class="card-top">
      <span class="product-chip" :class="ride.product">
        <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
          <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
        </svg>
        <span>{{ productLabel }}</span>
      </span>
      <span class="status-chip" :class="ride.status">{{ statusLabel }}</span>
    </div>

    <div class="card-body">
      <router-link :to="`/ride/${ride.id}`" class="title-link">
        {{ ride.title }}
      </router-link>
      <p class="description">{{ ride.description || '车主暂未补充公开说明。' }}</p>
    </div>

    <div class="price-row">
      <div class="price-item">
        <span class="meta-label">车位租金</span>
        <strong class="seat-price">¥{{ formatMoney(ride.price_per_month) }}<small>/月</small></strong>
      </div>
      <span class="price-divider" :class="ride.product" aria-hidden="true"></span>
      <div class="price-item warranty-item">
        <span class="meta-label">质保天数</span>
        <strong class="warranty-days" :class="ride.product">{{ warrantyDays }}<small>天</small></strong>
      </div>
    </div>

    <!-- Seat Progress -->
    <div class="seat-progress">
      <div class="progress-header">
        <div class="progress-label">
          <Users :size="13" class="progress-icon" />
          <span>拼车进度</span>
        </div>
        <span class="progress-count" :class="{ 'almost-full': fillPercent >= 80 }">{{ occupiedSeats }}/{{ totalSeats }}</span>
      </div>
      <div class="progress-track">
        <div
          class="progress-bar"
          :class="[ride.product, { full: fillPercent >= 100 }]"
          :style="{ width: fillPercent + '%' }"
        ></div>
      </div>
      <div class="progress-meta">
        <span class="remaining-tag" :class="{ urgent: remainingSeats <= 1 && ride.status === 'open' }">
          {{ remainingSeats <= 1 && ride.status === 'open' ? '仅剩 ' + remainingSeats + ' 位' : '还差 ' + remainingSeats + ' 人' }}
        </span>
        <span class="duration-tag">
          <CalendarClock :size="11" />
          {{ ride.duration }}个月
        </span>
      </div>
    </div>

    <div class="seller-row">
      <div class="seller">
        <img :src="ride.owner?.avatar || defaultAvatar" alt="车主头像" class="avatar" />
        <div class="seller-info">
          <strong>{{ ride.owner?.nickname || '车主' }}</strong>
          <span class="verified-tag"><BadgeCheck :size="12" /> 已认证车主</span>
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
import { BadgeCheck, CalendarClock, ChevronRight, Users } from '@lucide/vue'
import type { Ride } from '../../types'

const props = defineProps<{
  ride: Ride
}>()

const defaultAvatar = `https://api.dicebear.com/7.x/initials/svg?seed=${props.ride.owner_id}&backgroundColor=0f172a`

const productLabel = computed(() => {
  if (props.ride.product === 'chatgpt-team') return 'Business 团队'
  if (props.ride.product === 'chatgpt-pro') return 'Pro 极客'
  return 'Plus 拼车'
})

const statusLabel = computed(() => {
  if (props.ride.status === 'closed') return '已满员'
  if (props.ride.status === 'expired') return '已过期'
  return '招募中'
})

const totalSeats = computed(() => Number(props.ride.total_seats || 0))
const onboardSeats = computed(() => Number(props.ride.recruit_seats || Math.max((totalSeats.value || 1) - 1, 1)))
const occupiedSeats = computed(() => Math.min(onboardSeats.value + Number(props.ride.purchase_count || 0), totalSeats.value))
const remainingSeats = computed(() => Math.max(Number(props.ride.remaining_seats ?? (totalSeats.value - occupiedSeats.value)), 0))
const warrantyDays = computed(() => Number(props.ride.warranty_days || (props.ride.duration >= 12 ? 365 : props.ride.duration * 30)))
const fillPercent = computed(() => {
  if (totalSeats.value <= 0) return 0
  return Math.min(Math.round((occupiedSeats.value / totalSeats.value) * 100), 100)
})

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
  position: relative;
  overflow: hidden;
}

.ride-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--card-shadow-hover);
  border-color: var(--border-color-strong);
}

.ride-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-plus);
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.ride-card.chatgpt-team::before {
  background: var(--color-team);
}

.ride-card.chatgpt-pro::before {
  background: var(--color-pro);
}

.ride-card:hover::before {
  opacity: 1;
}

/* Product chip glow on card hover */
.ride-card:hover .product-chip.chatgpt-plus {
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.25);
  border-color: rgba(16, 185, 129, 0.3);
}

.ride-card:hover .product-chip.chatgpt-team {
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.25);
  border-color: rgba(59, 130, 246, 0.3);
}

.ride-card:hover .product-chip.chatgpt-pro {
  box-shadow: 0 0 8px rgba(139, 92, 246, 0.25);
  border-color: rgba(139, 92, 246, 0.3);
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
  letter-spacing: 0;
  transition: color var(--transition-fast);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.ride-card.chatgpt-plus .title-link:hover { color: var(--color-plus); }
.ride-card.chatgpt-team .title-link:hover { color: var(--color-team); }
.ride-card.chatgpt-pro .title-link:hover { color: var(--color-pro); }

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
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: center;
  gap: 12px;
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  margin-bottom: var(--spacing-md);
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.price-row:hover {
  border-color: var(--border-color-strong);
  background: var(--bg-tertiary);
}

.price-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.warranty-item {
  align-items: flex-end;
}

.price-divider {
  width: 3px;
  height: 26px;
  align-self: center;
  border-radius: var(--border-radius-full);
  background: var(--color-plus);
}

.price-divider.chatgpt-team {
  background: var(--color-team);
}

.price-divider.chatgpt-pro {
  background: var(--color-pro);
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

.warranty-days {
  color: var(--color-plus);
  font-size: 20px;
  font-weight: 800;
  line-height: 1;
}

.warranty-days.chatgpt-team {
  color: var(--color-team);
}

.warranty-days.chatgpt-pro {
  color: var(--color-pro);
}

.warranty-days small {
  color: currentColor;
  font-size: 11px;
  font-weight: 700;
  margin-left: 1px;
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

/* Seat Progress */
.seat-progress {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: var(--spacing-md);
  padding: 10px 12px;
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.progress-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.progress-label {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
}

.progress-icon {
  color: var(--text-muted);
}

.progress-count {
  font-size: 12px;
  font-weight: 800;
  color: var(--text-primary);
}

.progress-count.almost-full {
  color: var(--color-success);
}

.progress-track {
  height: 4px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: var(--border-radius-full);
  transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  background: var(--color-plus);
}

.progress-bar.chatgpt-team {
  background: var(--color-team);
}

.progress-bar.chatgpt-pro {
  background: var(--color-pro);
}

.progress-bar.full {
  position: relative;
  overflow: hidden;
}

.progress-bar.full::after {
  content: '';
  position: absolute;
  inset: 0;
  background: transparent;
  transform: translateX(-100%);
  animation: progressShimmer 2s ease-in-out infinite;
}

@keyframes progressShimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.progress-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.remaining-tag {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.remaining-tag.urgent {
  color: var(--color-warning);
  font-weight: 700;
  animation: urgentPulse 2s ease-in-out infinite;
}

@keyframes urgentPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.duration-tag {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 600;
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
  display: inline-flex;
  align-items: center;
  gap: 3px;
  color: var(--color-success);
  font-size: 10px;
  font-weight: 700;
}

.detail-btn {
  display: inline-flex;
  height: 34px;
  align-items: center;
  gap: 4px;
  padding: 0 14px;
  border-radius: var(--border-radius-sm);
  background: var(--color-team);
  color: var(--text-inverse);
  font-size: 12px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.detail-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: transparent;
  transform: translateX(-100%);
  transition: transform 0.5s ease;
}

.detail-btn:hover {
  background: var(--color-team-hover);
  box-shadow: 0 2px 10px color-mix(in srgb, var(--color-team) 30%, transparent);
  transform: translateY(-1px);
}

.detail-btn:hover::after {
  transform: translateX(100%);
}

.detail-btn:active {
  transform: scale(0.96) translateY(0);
}

.detail-btn:active {
  transform: scale(0.96);
}

.chip-logo {
  width: 14px;
  height: 14px;
  object-fit: contain;
  flex-shrink: 0;
}

/* Dark mode */
:global([data-theme="dark"] .ride-card ){
  background: var(--bg-tertiary);
}

:global([data-theme="dark"] .price-row ){
  background: var(--bg-inset);
}

:global([data-theme="dark"] .seat-progress ){
  background: var(--bg-inset);
}

:global([data-theme="dark"] .detail-btn ){
  background: var(--text-primary);
  color: var(--text-inverse);
  border: 1px solid var(--text-primary);
}

:global([data-theme="dark"] .detail-btn:hover ){
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  box-shadow: 0 2px 12px rgba(255, 255, 255, 0.12);
}

:global([data-theme="dark"] .ride-card:hover::before ){
  opacity: 0.7;
}

:global([data-theme="dark"] .progress-bar.full::after ){
  background: transparent;
}

:global([data-theme="dark"] .seller-row ){
  border-top-color: var(--border-color-strong);
}

:global([data-theme="dark"] .avatar ){
  border-color: var(--border-color-strong);
}

@media (max-width: 680px) {
  .ride-card {
    padding: 10px;
    border-radius: var(--border-radius-md);
  }

  .card-top {
    gap: 5px;
    margin-bottom: 8px;
  }

  .product-chip,
  .status-chip {
    height: 22px;
    padding: 0 6px;
    font-size: 9px;
  }

  .card-body {
    flex-grow: 0;
    gap: 4px;
    margin-bottom: 8px;
  }

  .title-link {
    min-height: 32px;
    font-size: 12px;
    line-height: 1.3;
    -webkit-line-clamp: 2;
  }

  .description {
    min-height: 15px;
    font-size: 10px;
    line-height: 1.45;
    -webkit-line-clamp: 1;
  }

  .price-row {
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    gap: 6px;
    padding: 8px 7px;
    margin-bottom: 8px;
  }

  .warranty-item {
    align-items: flex-end;
  }

  .price-divider {
    width: 2px;
    height: 20px;
    justify-self: center;
  }

  .meta-label {
    font-size: 8px;
    line-height: 1;
    letter-spacing: 0;
    white-space: nowrap;
  }

  .seat-price,
  .warranty-days {
    font-size: 14px;
    white-space: nowrap;
  }

  .seat-price small,
  .warranty-days small {
    font-size: 8px;
  }

  .seat-progress {
    gap: 4px;
    padding: 8px 10px;
    margin-bottom: 8px;
  }

  .progress-label span,
  .progress-count {
    font-size: 10px;
  }

  .remaining-tag,
  .duration-tag {
    font-size: 9px;
  }

  .seller-row {
    align-items: center;
    flex-direction: row;
    gap: 8px;
    padding-top: 8px;
  }

  .avatar {
    width: 24px;
    height: 24px;
  }

  .seller-info strong {
    font-size: 10px;
  }

  .verified-tag {
    font-size: 8px;
  }

  .detail-btn {
    width: auto;
    height: 30px;
    justify-content: center;
    padding: 0 9px;
    font-size: 10px;
  }
}
</style>
