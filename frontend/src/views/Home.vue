<template>
  <div class="home-page">
    <section class="market-hero">
      <div class="container hero-grid">
        <div class="hero-copy">
          <span class="eyebrow">BusGPT 信息展示平台</span>
          <h1 class="page-title">发现可用 AI 订阅车位，付费解锁车主联系方式</h1>
          <p class="page-subtitle">
            平台只展示商品与联系方式信息。你可以先比较车位月费、服务费、车主信息与公开说明，再支付信息服务费获取联系方式，自行与车主沟通后续事项。
          </p>

          <div class="hero-actions">
            <router-link to="/market" class="btn btn-primary">
              <Search :size="17" />
              发现车位
            </router-link>
            <router-link to="/create" class="btn btn-secondary">
              <PlusCircle :size="17" />
              发布车位
            </router-link>
          </div>
        </div>

        <div class="service-panel surface-card">
          <div class="panel-title">
            <LockKeyhole :size="20" />
            <span>解锁流程</span>
          </div>
          <div class="steps">
            <div v-for="step in steps" :key="step.title" class="step">
              <strong>{{ step.title }}</strong>
              <p>{{ step.desc }}</p>
            </div>
          </div>
          <div class="risk-note">
            <ShieldCheck :size="16" />
            <span>信息服务费仅用于展示联系方式，不等同于订阅付款。</span>
          </div>
        </div>
      </div>
    </section>

    <section class="container marketplace-section">
      <div class="section-head">
        <div>
          <span class="eyebrow">最新商品</span>
          <h2>正在展示的订阅车位</h2>
        </div>
        <router-link to="/market" class="text-link">
          查看全部
          <ChevronRight :size="16" />
        </router-link>
      </div>

      <div class="filters surface-card">
        <div class="search-box">
          <Search :size="17" />
          <input v-model="query" type="search" placeholder="搜索 Plus、Team、Pro 或车主说明" @input="handleSearch" />
        </div>
        <div class="tabs" role="tablist" aria-label="产品筛选">
          <button
            v-for="tab in productTabs"
            :key="tab.value"
            type="button"
            class="tab"
            :class="{ active: activeProduct === tab.value }"
            @click="selectProduct(tab.value)"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>正在加载车位信息</p>
      </div>
      <div v-else-if="rides.length === 0" class="empty-state surface-card">
        <PackageOpen :size="34" />
        <h3>暂无可展示车位</h3>
        <p>可以稍后再来，或发布自己的订阅车位。</p>
        <router-link to="/create" class="btn btn-primary">发布车位</router-link>
      </div>
      <div v-else class="rides-grid">
        <RideCard v-for="ride in rides.slice(0, 6)" :key="ride.id" :ride="ride" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ChevronRight, LockKeyhole, PackageOpen, PlusCircle, Search, ShieldCheck } from '@lucide/vue'
import { ridesApi } from '../api/rides'
import RideCard from '../components/ride/RideCard.vue'
import type { ProductType, Ride } from '../types'

const rides = ref<Ride[]>([])
const loading = ref(true)
const query = ref('')
const activeProduct = ref<ProductType | ''>('')
let searchTimeout: ReturnType<typeof setTimeout> | null = null

const steps = [
  { title: '1. 浏览车位', desc: '比较月费、有效期、服务费和公开说明。' },
  { title: '2. 支付服务费', desc: '确认信息服务费后生成解锁订单。' },
  { title: '3. 获取联系方式', desc: '查看车主联系方式并自行沟通后续交易。' },
]

const productTabs: { label: string; value: ProductType | '' }[] = [
  { label: '全部', value: '' },
  { label: 'Plus', value: 'chatgpt-plus' },
  { label: 'Team', value: 'chatgpt-team' },
  { label: 'Pro', value: 'chatgpt-pro' },
]

const fetchRides = async () => {
  loading.value = true
  try {
    const res = await ridesApi.getRides({
      product: activeProduct.value,
      query: query.value,
    })
    rides.value = res.data
  } catch (err) {
    console.error('Failed to load rides', err)
    rides.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(fetchRides, 300)
}

const selectProduct = (product: ProductType | '') => {
  activeProduct.value = product
  fetchRides()
}

onMounted(fetchRides)
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.market-hero {
  padding: var(--spacing-xl) 0;
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(320px, 0.8fr);
  gap: var(--spacing-xl);
  align-items: stretch;
}

.hero-copy,
.service-panel {
  min-height: 310px;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: var(--spacing-md);
  padding: var(--spacing-xl);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  background: linear-gradient(180deg, #ffffff 0%, #faf8f3 100%);
  box-shadow: var(--card-shadow);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.service-panel {
  padding: var(--spacing-lg);
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 900;
}

.steps {
  display: grid;
  gap: var(--spacing-sm);
  margin: var(--spacing-lg) 0;
}

.step {
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.step strong {
  display: block;
  margin-bottom: 4px;
  color: var(--text-primary);
  font-size: 13px;
}

.step p,
.risk-note {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

.risk-note {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-radius: var(--border-radius-md);
  background: var(--color-warning-soft);
  color: #7c4a00;
}

.marketplace-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.section-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--spacing-md);
}

.section-head h2 {
  margin-top: 5px;
  color: var(--text-primary);
  font-size: 22px;
  font-weight: 900;
}

.text-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 900;
}

.filters {
  display: grid;
  grid-template-columns: minmax(280px, 1fr) auto;
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

.tabs {
  display: flex;
  gap: 4px;
  padding: 4px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.tab {
  min-height: 34px;
  padding: 0 13px;
  border-radius: var(--border-radius-sm);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 800;
}

.tab.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  box-shadow: 0 1px 2px rgba(25, 31, 36, 0.08);
}

.rides-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

@media (max-width: 1080px) {
  .hero-grid,
  .filters {
    grid-template-columns: 1fr;
  }

  .rides-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 680px) {
  .hero-copy,
  .service-panel {
    min-height: auto;
    padding: var(--spacing-lg);
  }

  .section-head {
    align-items: flex-start;
    flex-direction: column;
  }

  .tabs {
    overflow-x: auto;
  }

  .rides-grid {
    grid-template-columns: 1fr;
  }
}
</style>
