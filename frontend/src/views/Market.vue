<template>
  <div class="market-page container">
    <header class="page-header">
      <div>
        <span class="eyebrow">商品市场</span>
        <h1 class="page-title">发现车位</h1>
        <p class="page-subtitle">筛选公开展示的 AI 订阅车位。联系方式需支付信息服务费后查看。</p>
      </div>
      <router-link to="/create" class="btn btn-primary">
        <PlusCircle :size="17" />
        发布车位
      </router-link>
    </header>

    <section class="toolbar surface-card">
      <div class="search-box">
        <Search :size="17" />
        <input v-model="searchQuery" type="search" placeholder="搜索车位标题或公开说明" @input="handleSearch" />
      </div>

      <div class="product-tabs">
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

      <select v-model="selectedStatus" class="status-select" @change="fetchData">
        <option value="">仅可解锁</option>
        <option value="open">可解锁</option>
        <option value="closed">已关闭</option>
        <option value="expired">已过期</option>
      </select>
    </section>

    <section class="market-metrics">
      <div class="metric surface-card">
        <span>展示车位</span>
        <strong>{{ ridesStore.rides.length }}</strong>
      </div>
      <div class="metric surface-card">
        <span>平均月费</span>
        <strong>¥{{ avgPrice }}</strong>
      </div>
      <div class="metric surface-card">
        <span>信息服务费</span>
        <strong>¥{{ avgUnlockFee }}</strong>
      </div>
    </section>

    <div v-if="ridesStore.loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载车位中</p>
    </div>

    <div v-else-if="ridesStore.rides.length === 0" class="empty-state surface-card">
      <PackageOpen :size="34" />
      <h3>暂无匹配车位</h3>
      <p>可以调整筛选条件，或发布一个新的展示车位。</p>
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
  { label: 'Team', value: 'chatgpt-team' },
  { label: 'Pro', value: 'chatgpt-pro' },
]

const avgPrice = computed(() => {
  if (!ridesStore.rides.length) return 0
  const total = ridesStore.rides.reduce((sum, ride) => sum + Number(ride.price_per_month), 0)
  return Math.round(total / ridesStore.rides.length)
})

const avgUnlockFee = computed(() => {
  if (!ridesStore.rides.length) return 0
  const total = ridesStore.rides.reduce((sum, ride) => sum + Number(ride.contact_price), 0)
  return Math.round(total / ridesStore.rides.length)
})

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
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-lg);
}

.toolbar {
  display: grid;
  grid-template-columns: minmax(260px, 1fr) auto auto;
  gap: var(--spacing-md);
  align-items: center;
  padding: var(--spacing-md);
}

.search-box {
  display: flex;
  min-height: 42px;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  color: var(--text-muted);
}

.search-box input {
  width: 100%;
  color: var(--text-primary);
  font-size: 14px;
}

.product-tabs {
  display: flex;
  gap: 4px;
  padding: 4px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.tab-btn {
  min-height: 34px;
  padding: 0 13px;
  border-radius: var(--border-radius-sm);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 800;
}

.tab-btn.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  box-shadow: 0 1px 2px rgba(25, 31, 36, 0.08);
}

.status-select {
  min-height: 42px;
  padding: 0 34px 0 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 800;
}

.market-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.metric {
  padding: var(--spacing-md);
}

.metric span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 800;
}

.metric strong {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 900;
}

.rides-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

@media (max-width: 1080px) {
  .toolbar {
    grid-template-columns: 1fr;
  }

  .rides-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 680px) {
  .page-header {
    flex-direction: column;
  }

  .product-tabs {
    overflow-x: auto;
  }

  .market-metrics,
  .rides-grid {
    grid-template-columns: 1fr;
  }
}
</style>
