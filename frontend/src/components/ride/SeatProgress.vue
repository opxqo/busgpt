<template>
  <div class="seat-progress">
    <div class="seats-visual">
      <div
        v-for="index in total"
        :key="index"
        class="seat-dot"
        :class="{
          occupied: index <= occupied,
          frontier: index === occupied && occupied > 0,
          [productType]: true
        }"
        :style="{
          ...(index <= occupied ? { backgroundColor: productColors[productType] } : {}),
          animationDelay: (index * 0.06) + 's',
        }"
        :title="index <= occupied ? '已占用' : '空席位'"
      ></div>
    </div>
    <div class="seats-info">
      <span class="occupied-count">{{ occupied }}</span>
      <span class="divider">/</span>
      <span class="total-count">{{ total }}人</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProductType } from '../../types'

defineProps<{
  occupied: number
  total: number
  productType: ProductType
}>()

const productColors = {
  'chatgpt-plus': 'var(--color-plus)',
  'chatgpt-team': 'var(--color-team)',
  'chatgpt-pro': 'var(--color-pro)',
}
</script>

<style scoped>
.seat-progress {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.seats-visual {
  display: flex;
  gap: 6px;
}

.seat-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--border-radius-full);
  background-color: var(--border-color);
  transition: background-color var(--transition-fast), transform var(--transition-fast);
  animation: dotPop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.seat-dot.occupied {
  transform: scale(1.15);
  animation: none;
}

.seat-dot.frontier {
  animation: dotPop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) both, frontierPulse 2s ease-in-out infinite;
  box-shadow: 0 0 0 0 var(--color-plus);
}

.seat-dot.frontier.chatgpt-team {
  box-shadow: 0 0 0 0 var(--color-team);
}

.seat-dot.frontier.chatgpt-pro {
  box-shadow: 0 0 0 0 var(--color-pro);
}

@keyframes dotPop {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes frontierPulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--color-plus); }
  50% { box-shadow: 0 0 0 4px transparent; }
}

.seat-dot:hover {
  transform: scale(1.4);
  z-index: 1;
}

.seats-info {
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 1px;
}

.occupied-count {
  color: var(--text-primary);
  font-weight: 600;
}

.divider {
  color: var(--text-muted);
}

.total-count {
  color: var(--text-secondary);
}
</style>
