<template>
  <div class="market-page container">
    <!-- Header -->
    <header class="page-header">
      <div class="header-info">
        <span class="eyebrow">共享市场</span>
        <h1 class="page-title">发现可用订阅车位</h1>
        <p class="page-subtitle">筛选展示中的 ChatGPT 拼车车位，直接查看车主联系方式。</p>
      </div>
      <router-link to="/create" class="btn btn-primary publish-btn">
        <PlusCircle :size="16" />
        <span>发布我的车位</span>
      </router-link>
    </header>

    <!-- Metrics Stats Section -->
    <section class="market-metrics">
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">展示车位</span>
          <strong class="metric-value">
            <span class="indicator-dot success"></span>
            {{ ridesStore.rides.length }} 个
          </strong>
        </div>
      </div>
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">平均租金参考</span>
          <strong class="metric-value">
            <span class="indicator-dot primary"></span>
            ¥{{ avgPrice }}/月
          </strong>
        </div>
      </div>
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">平均拼车期限</span>
          <strong class="metric-value">
            <span class="indicator-dot warning"></span>
            {{ avgDuration }} 个月
          </strong>
        </div>
      </div>
      <div class="metric-card surface-card">
        <div class="metric-info">
          <span class="metric-label">总拼车座位</span>
          <strong class="metric-value">
            <span class="indicator-dot info"></span>
            {{ totalSeats }} 人
          </strong>
        </div>
      </div>
    </section>

    <!-- Filter Control Toolbar -->
    <section class="toolbar-panel surface-card">
      <div class="search-input-wrapper">
        <Search :size="18" class="search-icon" />
        <input v-model="searchQuery" type="search" placeholder="搜索车位标题、公开描述或说明" @input="handleSearch" />
      </div>

      <div class="filter-actions">
        <div class="product-tabs" role="tablist">
          <button
            v-for="tab in productTabs"
            :key="tab.value"
            type="button"
            class="tab-btn"
            :class="{ active: activeProduct === tab.value }"
            @click="selectProduct(tab.value)"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="select-wrapper">
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
    <div v-if="ridesStore.loading" class="loading-container">
      <div class="spinner"></div>
      <p>正在搜索匹配的车位...</p>
    </div>

    <div v-else-if="ridesStore.rides.length === 0" class="empty-state surface-card">
      <PackageOpen :size="38" class="empty-icon" />
      <h3>暂无匹配的拼车车位</h3>
      <p>没有找到符合条件的车位。您可以调整筛选条件，或者直接发布一个车位。</p>
      <router-link to="/create" class="btn btn-primary">发布车位</router-link>
    </div>

    <div v-else class="rides-grid">
      <RideCard v-for="ride in ridesStore.rides" :key="ride.id" :ride="ride" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { PackageOpen, PlusCircle, Search } from '@lucide/vue'
import RideCard from '../components/ride/RideCard.vue'
import { useRidesStore } from '../stores/rides'
import type { ProductType } from '../types'

const ridesStore = useRidesStore()
const searchQuery = ref('')
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

const selectProduct = (product: ProductType | '') => {
  activeProduct.value = product
  fetchData()
}

onMounted(() => {
  fetchData()
  ridesStore.fetchProducts()
})
</script>

<style scoped>
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
  height: 42px;
  padding: 0 var(--spacing-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  transition: border-color var(--transition-fast);
}

.search-input-wrapper:focus-within {
  border-color: var(--text-primary);
}

.search-icon {
  color: var(--text-muted);
}

.search-input-wrapper input {
  width: 100%;
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  color: var(--text-primary);
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.product-tabs {
  display: flex;
  min-width: 0;
  gap: 4px;
  padding: 4px;
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.tab-btn {
  height: 34px;
  padding: 0 14px;
  border-radius: var(--border-radius-sm);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tab-btn.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.select-wrapper select {
  height: 42px;
  padding: 0 32px 0 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
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

.empty-icon {
  color: var(--text-muted);
}

@media (max-width: 1080px) {
  .toolbar-panel {
    grid-template-columns: 1fr;
  }
  .filter-actions {
    width: 100%;
    justify-content: space-between;
  }
  .rides-grid {
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
    height: 40px;
    padding: 0 12px;
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
  .select-wrapper select {
    width: 100%;
  }
  .rides-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
  }
}

@media (max-width: 360px) {
  .rides-grid {
    grid-template-columns: 1fr;
  }
}
</style>
