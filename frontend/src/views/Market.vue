<template>
  <div class="market-page container">
    <!-- Header -->
    <header class="page-header anim-fade-up">
      <div class="header-accent" aria-hidden="true"></div>
      <div class="header-info">
        <span class="eyebrow">共享市场</span>
        <h1 class="page-title">发现可用订阅车位</h1>
        <p class="page-subtitle">筛选展示中的 ChatGPT 拼车车位，直接查看车主联系方式。</p>
      </div>
      <router-link to="/create" class="btn btn-primary publish-btn publish-shimmer">
        <PlusCircle :size="16" />
        <span>发布我的车位</span>
      </router-link>
    </header>

    <!-- Metrics Stats Section -->
    <section class="market-metrics anim-fade-up anim-d1">
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">展示车位</span>
          <strong class="metric-value">
            <span class="indicator-dot success"></span>
            {{ animatedRideCount }} 个
          </strong>
        </div>
      </div>
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">平均租金参考</span>
          <strong class="metric-value">
            <span class="indicator-dot primary"></span>
            ¥{{ animatedAvgPrice }}/月
          </strong>
        </div>
      </div>
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">平均拼车期限</span>
          <strong class="metric-value">
            <span class="indicator-dot warning"></span>
            {{ animatedAvgDuration }} 个月
          </strong>
        </div>
      </div>
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">总拼车座位</span>
          <strong class="metric-value">
            <span class="indicator-dot info"></span>
            {{ animatedTotalSeats }} 人
          </strong>
        </div>
      </div>
    </section>

    <!-- Filter Control Toolbar -->
    <section class="toolbar-panel surface-card anim-fade-up anim-d2">
      <div class="search-input-wrapper" :class="{ focused: searchFocused }">
        <Search :size="16" class="search-icon" />
        <input
          v-model="searchQuery"
          type="search"
          placeholder="搜索车位标题、描述..."
          @input="handleSearch"
          @focus="searchFocused = true"
          @blur="searchFocused = false"
        />
        <kbd v-if="!searchQuery && !searchFocused" class="search-kbd">/</kbd>
        <button v-else-if="searchQuery" class="search-clear" type="button" @click="clearSearch">
          <X :size="14" />
        </button>
      </div>

      <div class="filter-actions">
        <div class="product-tabs" role="tablist">
          <button
            v-for="tab in productTabs"
            :key="tab.value"
            type="button"
            class="tab-btn"
            :class="[{ active: activeProduct === tab.value }, tab.value]"
            @click="selectProduct(tab.value)"
          >
            <span v-if="tab.value" class="tab-dot" :class="tab.value"></span>
            {{ tab.label }}
          </button>
        </div>

        <div class="select-wrapper">
          <Filter :size="14" class="filter-icon" />
          <select v-model="selectedStatus" class="status-select" @change="fetchData">
            <option value="">全部状态</option>
            <option value="open">招募中</option>
            <option value="closed">已满员</option>
            <option value="expired">已过期</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Grid / Content -->
    <div v-if="ridesStore.loading" class="skeleton-grid">
      <div v-for="i in 8" :key="i" class="skeleton-card surface-card">
        <div class="skeleton-header">
          <div class="skel-chip"></div>
          <div class="skel-status"></div>
        </div>
        <div class="skel-title"></div>
        <div class="skel-desc"></div>
        <div class="skel-desc short"></div>
        <div class="skel-metrics">
          <div class="skel-metric"></div>
          <div class="skel-metric"></div>
        </div>
        <div class="skel-bar"></div>
        <div class="skel-footer">
          <div class="skel-price"></div>
          <div class="skel-btn"></div>
        </div>
      </div>
    </div>

    <div v-else-if="ridesStore.rides.length === 0" class="empty-state surface-card anim-fade-up">
      <PackageOpen :size="38" class="empty-icon" />
      <h3>暂无匹配的拼车车位</h3>
      <p>没有找到符合条件的车位。您可以调整筛选条件，或者直接发布一个车位。</p>
      <router-link to="/create" class="btn btn-primary">发布车位</router-link>
    </div>

    <div v-else class="rides-grid anim-fade-up anim-d3">
      <div v-for="(ride, index) in ridesStore.rides" :key="ride.id" class="grid-card-wrapper" :style="{ animationDelay: (index * 0.04) + 's' }">
        <RideCard :ride="ride" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type Ref, computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { Filter, PackageOpen, PlusCircle, Search, X } from '@lucide/vue'
import RideCard from '../components/ride/RideCard.vue'
import { useRidesStore } from '../stores/rides'
import type { ProductType } from '../types'

const ridesStore = useRidesStore()
const searchQuery = ref('')
const searchFocused = ref(false)
const activeProduct = ref<ProductType | ''>('')
const selectedStatus = ref('')
let searchTimeout: ReturnType<typeof setTimeout> | null = null

const productTabs: { label: string; value: ProductType | '' }[] = [
  { label: '全部', value: '' },
  { label: 'Plus', value: 'chatgpt-plus' },
  { label: 'Business', value: 'chatgpt-team' },
  { label: 'Pro', value: 'chatgpt-pro' },
]

const avgPrice = computed(() => {
  if (!ridesStore.rides.length) return 0
  const total = ridesStore.rides.reduce((sum, ride) => sum + Number(ride.price_per_month), 0)
  return Math.round(total / ridesStore.rides.length)
})

const avgDuration = computed(() => {
  if (!ridesStore.rides.length) return 0
  const total = ridesStore.rides.reduce((sum, ride) => sum + Number(ride.duration), 0)
  return Math.round(total / ridesStore.rides.length)
})

const totalSeats = computed(() =>
  ridesStore.rides.reduce((sum, ride) => sum + Number(ride.total_seats || 0), 0)
)

// Count-up animation for metric numbers
const animatedRideCount = ref(0)
const animatedAvgPrice = ref(0)
const animatedAvgDuration = ref(0)
const animatedTotalSeats = ref(0)

const animateValue = (target: Ref<number>, end: number, duration = 600) => {
  const start = target.value
  if (start === end) return
  const startTime = performance.now()
  const tick = (now: number) => {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3) // ease-out cubic
    target.value = Math.round(start + (end - start) * eased)
    if (progress < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

watch(
  () => ridesStore.rides.length,
  (val) => animateValue(animatedRideCount, val),
  { immediate: true }
)

watch(avgPrice, (val) => animateValue(animatedAvgPrice, val), { immediate: true })
watch(avgDuration, (val) => animateValue(animatedAvgDuration, val), { immediate: true })
watch(totalSeats, (val) => animateValue(animatedTotalSeats, val), { immediate: true })

const fetchData = () => {
  ridesStore.fetchRides({
    product: activeProduct.value,
    status_filter: selectedStatus.value,
    query: searchQuery.value,
  })
}

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(fetchData, 300)
}

const clearSearch = () => {
  searchQuery.value = ''
  fetchData()
}

const selectProduct = (product: ProductType | '') => {
  activeProduct.value = product
  fetchData()
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
    const target = e.target as HTMLElement
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.tagName === 'SELECT') return
    e.preventDefault()
    const input = document.querySelector('.search-input-wrapper input') as HTMLInputElement
    input?.focus()
  }
}

onMounted(() => {
  fetchData()
  ridesStore.fetchProducts()
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.anim-fade-up {
  opacity: 0;
  transform: translateY(12px);
  animation: fadeUp 0.45s ease-out forwards;
}

.anim-d1 { animation-delay: 0.05s; }
.anim-d2 { animation-delay: 0.12s; }
.anim-d3 { animation-delay: 0.2s; }

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.market-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  padding-bottom: var(--spacing-lg);
  position: relative;
}

.header-accent {
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--border-color-strong);
  opacity: 0.4;
}

.publish-shimmer {
  position: relative;
  overflow: hidden;
}

.publish-shimmer::after {
  content: '';
  position: absolute;
  inset: 0;
  background: transparent;
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.publish-shimmer:hover::after {
  transform: translateX(100%);
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.publish-btn {
  flex-shrink: 0;
}

/* Metrics Section */
.market-metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.metric-card {
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  align-items: center;
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.metric-card::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.metric-card:nth-child(1)::before { background: var(--color-success); }
.metric-card:nth-child(2)::before { background: var(--color-team); }
.metric-card:nth-child(3)::before { background: var(--color-pro); }
.metric-card:nth-child(4)::before { background: var(--color-info); }

.metric-card:hover {
  border-color: var(--border-color-strong);
  transform: translateY(-1px);
  box-shadow: var(--card-shadow);
}

.metric-card:hover::before {
  opacity: 1;
}

.metric-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-label {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
}

.metric-value {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.2;
}

/* Indicator dots */
.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--border-radius-full);
}

.indicator-dot.success {
  background: var(--color-success);
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.indicator-dot.primary {
  background: var(--color-team);
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.4);
}

.indicator-dot.warning {
  background: var(--color-pro);
  box-shadow: 0 0 8px rgba(139, 92, 246, 0.4);
}

.indicator-dot.info {
  background: var(--color-info);
  box-shadow: 0 0 8px rgba(6, 182, 212, 0.4);
}

/* Toolbar Panel */
.toolbar-panel {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--spacing-md);
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-color: var(--border-color-strong);
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  height: 40px;
  padding: 0 12px;
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-fast);
}

.search-input-wrapper.focused {
  border-color: var(--color-team);
  box-shadow: 0 0 0 3px var(--focus-ring), 0 2px 8px rgba(59, 130, 246, 0.08);
}

.search-icon {
  color: var(--text-muted);
  flex-shrink: 0;
}

.search-input-wrapper input {
  width: 100%;
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.search-input-wrapper input::placeholder {
  color: var(--text-muted);
  font-weight: 500;
}

.search-kbd {
  display: inline-flex;
  height: 20px;
  min-width: 20px;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-secondary);
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 700;
  font-family: inherit;
  flex-shrink: 0;
}

.search-clear {
  display: inline-flex;
  width: 20px;
  height: 20px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-full);
  border: none;
  background: var(--bg-tertiary);
  color: var(--text-muted);
  cursor: pointer;
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

.search-clear:hover {
  background: var(--text-primary);
  color: var(--text-inverse);
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.product-tabs {
  display: flex;
  min-width: 0;
  gap: 3px;
  padding: 3px;
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 32px;
  padding: 0 12px;
  border-radius: var(--border-radius-sm);
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tab-btn:hover {
  color: var(--text-secondary);
}

.tab-btn.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  position: relative;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 2px;
  border-radius: var(--border-radius-full);
  background: var(--text-primary);
  animation: tabPop 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes tabPop {
  from {
    width: 0;
    opacity: 0;
  }
  to {
    width: 16px;
    opacity: 1;
  }
}

.tab-btn.active.chatgpt-plus::after { background: var(--color-plus); }
.tab-btn.active.chatgpt-team::after { background: var(--color-team); }
.tab-btn.active.chatgpt-pro::after { background: var(--color-pro); }

.tab-dot {
  width: 6px;
  height: 6px;
  border-radius: var(--border-radius-full);
  background: var(--text-muted);
  flex-shrink: 0;
}

.tab-dot.chatgpt-plus {
  background: var(--color-plus);
}

.tab-dot.chatgpt-team {
  background: var(--color-team);
}

.tab-dot.chatgpt-pro {
  background: var(--color-pro);
}

.select-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.filter-icon {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  pointer-events: none;
  z-index: 1;
}

.select-wrapper select {
  height: 38px;
  padding: 0 32px 0 32px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 14px;
  transition: border-color var(--transition-fast);
}

.select-wrapper select:hover {
  border-color: var(--border-color-strong);
}

.rides-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.grid-card-wrapper {
  opacity: 0;
  transform: translateY(12px);
  animation: fadeUp 0.45s ease-out forwards;
}

.empty-icon {
  color: var(--text-muted);
  opacity: 0.6;
}

/* Skeleton Loading */
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.skeleton-card {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.skel-chip {
  width: 60px;
  height: 22px;
  border-radius: var(--border-radius-full);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite;
}

.skel-status {
  width: 48px;
  height: 20px;
  border-radius: var(--border-radius-full);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite 0.1s;
}

.skel-title {
  width: 80%;
  height: 18px;
  border-radius: var(--border-radius-sm);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite 0.15s;
}

.skel-desc {
  width: 100%;
  height: 12px;
  border-radius: var(--border-radius-sm);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite 0.2s;
}

.skel-desc.short {
  width: 60%;
  animation-delay: 0.25s;
}

.skel-metrics {
  display: flex;
  gap: 12px;
}

.skel-metric {
  flex: 1;
  height: 40px;
  border-radius: var(--border-radius-sm);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite 0.3s;
}

.skel-bar {
  width: 100%;
  height: 6px;
  border-radius: var(--border-radius-full);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite 0.35s;
}

.skel-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
}

.skel-price {
  width: 70px;
  height: 20px;
  border-radius: var(--border-radius-sm);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite 0.4s;
}

.skel-btn {
  width: 80px;
  height: 32px;
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  animation: shimmer 1.5s ease-in-out infinite 0.45s;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* Dark mode */
:global([data-theme="dark"] .skel-chip),
:global([data-theme="dark"] .skel-status),
:global([data-theme="dark"] .skel-title),
:global([data-theme="dark"] .skel-desc),
:global([data-theme="dark"] .skel-metric),
:global([data-theme="dark"] .skel-bar),
:global([data-theme="dark"] .skel-price),
:global([data-theme="dark"] .skel-btn ){
  background: var(--bg-tertiary);
}

:global([data-theme="dark"] .metric-card::before ){
  filter: brightness(1.2);
}

:global([data-theme="dark"] .search-input-wrapper.focused ){
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(0, 0, 0, 0.2);
}

@media (max-width: 1080px) {
  .toolbar-panel {
    grid-template-columns: 1fr;
  }
  .filter-actions {
    width: 100%;
    justify-content: space-between;
  }
  .rides-grid,
  .skeleton-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 680px) {
  .market-page {
    gap: var(--spacing-md);
  }
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
  .publish-btn {
    width: 100%;
  }
  .market-metrics {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: var(--spacing-sm);
  }
  .metric-card {
    padding: 10px;
  }
  .metric-label {
    font-size: 10px;
  }
  .metric-value {
    align-items: flex-start;
    gap: 5px;
    font-size: 15px;
    line-height: 1.25;
  }
  .indicator-dot {
    margin-top: 5px;
    width: 6px;
    height: 6px;
  }
  .toolbar-panel {
    padding: 10px;
  }
  .search-input-wrapper {
    height: 38px;
    padding: 0 10px;
  }
  .filter-actions {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }
  .product-tabs {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  .tab-btn {
    flex: 0 0 auto;
  }
  .select-wrapper {
    width: 100%;
  }
  .select-wrapper select {
    width: 100%;
  }
  .rides-grid,
  .skeleton-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }
}

@media (max-width: 360px) {
  .rides-grid,
  .skeleton-grid {
    grid-template-columns: 1fr;
  }
}
</style>
