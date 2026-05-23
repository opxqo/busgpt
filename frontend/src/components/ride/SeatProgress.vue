<template>
  <div class="seat-progress">
    <div class="seats-visual">
      <div 
        v-for="index in total" 
        :key="index" 
        class="seat-dot"
        :class="{
          occupied: index <= occupied,
          [productType]: true
        }"
        :style="index <= occupied ? { backgroundColor: productColors[productType] } : {}"
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
}

.seat-dot.occupied {
  transform: scale(1.1);
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
