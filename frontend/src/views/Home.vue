<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-container container">
        <div class="hero-content">
          <div class="badge-container">
            <span class="pill-badge">BusGPT 车位信息聚合台</span>
          </div>
          <h1 class="hero-title">
            发现可用 AI 订阅车位<br />
            <span class="gradient-text">付费解锁车主联系方式</span>
          </h1>
          <p class="hero-subtitle">
            轻松找到志同道合的伙伴分摊 AI 订阅费。平台仅作商品与联系方式的信息共享，协助您与车主建立连接，不涉及中间差价与资金代收。
          </p>

          <div class="hero-actions">
            <router-link to="/market" class="btn btn-primary hero-btn">
              <Search :size="16" />
              <span>发现订阅车位</span>
            </router-link>
            <router-link to="/create" class="btn btn-secondary hero-btn">
              <PlusCircle :size="16" />
              <span>发布共享车位</span>
            </router-link>
          </div>
        </div>

        <div class="process-panel surface-card">
          <div class="panel-header">
            <div class="icon-circle">
              <LockKeyhole :size="20" />
            </div>
            <strong>极简拼车三步走</strong>
          </div>
          <div class="steps-flow">
            <div v-for="(step, idx) in steps" :key="step.title" class="step-item">
              <div class="step-num">0{{ idx + 1 }}</div>
              <div class="step-info">
                <strong>{{ step.title }}</strong>
                <p>{{ step.desc }}</p>
              </div>
            </div>
          </div>
          <div class="panel-footer">
            <ShieldCheck :size="14" class="safety-icon" />
            <span>信息服务费仅用于解锁车主联系方式，请线下确认订阅细节。</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Recommended Marketplace Section (Carousel) -->
    <section class="container marketplace-section">
      <div class="section-header">
        <div class="section-title-wrap">
          <span class="eyebrow">实时推荐</span>
          <h2>最新可解锁车位</h2>
        </div>
        <div class="nav-and-view-all">
          <router-link to="/market" class="view-all-link">
            <span>查看全部车位</span>
            <ChevronRight :size="16" />
          </router-link>
        </div>
      </div>

      <div class="filter-toolbar surface-card">
        <div class="search-input-wrapper">
          <Search :size="18" class="search-icon" />
          <input v-model="query" type="search" placeholder="搜索 Plus, Team, Pro 或车主关键词" @input="handleSearch" />
        </div>
        <div class="tabs-list" role="tablist">
          <button
            v-for="tab in productTabs"
            :key="tab.value"
            type="button"
            class="tab-item"
            :class="{ active: activeProduct === tab.value }"
            @click="selectProduct(tab.value)"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <!-- Carousel -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>正在拉取最新可共享车位...</p>
      </div>
      <div v-else-if="rides.length === 0" class="empty-state surface-card">
        <PackageOpen :size="38" class="empty-icon" />
        <h3>暂无展示中的订阅车位</h3>
        <p>稍后再来看看，或者自己发布一个订阅车位，吸引车友拼车。</p>
        <router-link to="/create" class="btn btn-primary">发布车位</router-link>
      </div>
      <div v-else class="carousel-outer">
        <button type="button" class="carousel-arrow left" @click="scrollLeft" aria-label="向左滑动">
          <ChevronLeft :size="20" />
        </button>
        
        <div class="carousel-track" ref="carouselTrack">
          <div v-for="ride in rides" :key="ride.id" class="carousel-slide">
            <RideCard :ride="ride" />
          </div>
        </div>

        <button type="button" class="carousel-arrow right" @click="scrollRight" aria-label="向右滑动">
          <ChevronRight :size="20" />
        </button>
      </div>
    </section>

    <!-- Platform Data Dashboard Section -->
    <section class="container stats-dashboard-section">
      <div class="section-header">
        <div class="section-title-wrap">
          <span class="eyebrow">数据洞察</span>
          <h2>本平台拼车数据看板</h2>
        </div>
      </div>

      <div class="dashboard-grid">
        <!-- Chart 1: Price Trends Line Chart -->
        <div class="dashboard-card surface-card">
          <div class="card-header-wrap">
            <TrendingUp :size="16" class="chart-icon-trend" />
            <strong>ChatGPT 拼车月费价格走势 (近6个月)</strong>
          </div>
          <div class="chart-container">
            <!-- SVG Price Line Chart -->
            <svg viewBox="0 0 500 220" class="line-chart-svg" aria-label="价格趋势图">
              <!-- Y-Axis Grid Lines & Labels -->
              <g class="grid-lines">
                <line x1="45" y1="20" x2="480" y2="20" stroke="var(--border-color)" stroke-dasharray="3" />
                <text x="15" y="24" class="y-label">¥200</text>

                <line x1="45" y1="70" x2="480" y2="70" stroke="var(--border-color)" stroke-dasharray="3" />
                <text x="15" y="74" class="y-label">¥150</text>

                <line x1="45" y1="120" x2="480" y2="120" stroke="var(--border-color)" stroke-dasharray="3" />
                <text x="15" y="124" class="y-label">¥100</text>

                <line x1="45" y1="170" x2="480" y2="170" stroke="var(--border-color)" stroke-dasharray="3" />
                <text x="15" y="174" class="y-label">¥50</text>

                <line x1="45" y1="200" x2="480" y2="200" stroke="var(--border-color-strong)" />
                <text x="15" y="204" class="y-label">¥0</text>
              </g>

              <!-- Lines for Product Prices (Calculated using coordinates based on simulated data) -->
              <!-- Plus: Green (#10b981) -->
              <path
                d="M 60,185 L 140,182 L 220,180 L 300,185 L 380,183 L 460,180"
                fill="none"
                stroke="var(--color-plus)"
                stroke-width="3"
                stroke-linecap="round"
              />
              <!-- Team: Blue (#2563eb) -->
              <path
                d="M 60,192 L 140,190 L 220,191 L 300,193 L 380,192 L 460,190"
                fill="none"
                stroke="var(--color-team)"
                stroke-width="3"
                stroke-linecap="round"
              />
              <!-- Pro: Purple (#8b5cf6) -->
              <path
                d="M 60,140 L 140,130 L 220,120 L 300,110 L 380,100 L 460,90"
                fill="none"
                stroke="var(--color-pro)"
                stroke-width="3"
                stroke-linecap="round"
              />

              <!-- Vertex circles (Pro) -->
              <g class="chart-points">
                <circle cx="60" cy="140" r="4" fill="var(--bg-secondary)" stroke="var(--color-pro)" stroke-width="2" />
                <circle cx="140" cy="130" r="4" fill="var(--bg-secondary)" stroke="var(--color-pro)" stroke-width="2" />
                <circle cx="220" cy="120" r="4" fill="var(--bg-secondary)" stroke="var(--color-pro)" stroke-width="2" />
                <circle cx="300" cy="110" r="4" fill="var(--bg-secondary)" stroke="var(--color-pro)" stroke-width="2" />
                <circle cx="380" cy="100" r="4" fill="var(--bg-secondary)" stroke="var(--color-pro)" stroke-width="2" />
                <circle cx="460" cy="90" r="4" fill="var(--bg-secondary)" stroke="var(--color-pro)" stroke-width="2" />
              </g>

              <!-- X-Axis Labels -->
              <g class="x-axis-labels" fill="var(--text-secondary)">
                <text x="60" y="218" text-anchor="middle">12月</text>
                <text x="140" y="218" text-anchor="middle">1月</text>
                <text x="220" y="218" text-anchor="middle">2月</text>
                <text x="300" y="218" text-anchor="middle">3月</text>
                <text x="380" y="218" text-anchor="middle">4月</text>
                <text x="460" y="218" text-anchor="middle">5月</text>
              </g>
            </svg>
            <!-- Legend -->
            <div class="chart-legend">
              <span class="legend-item"><span class="legend-color plus"></span>Plus (约¥35/月)</span>
              <span class="legend-item"><span class="legend-color team"></span>Team (约¥28/月)</span>
              <span class="legend-item"><span class="legend-color pro"></span>Pro (下降至约¥110/月)</span>
            </div>
          </div>
        </div>

        <!-- Chart 2: Top Selling/Unlocked Rides Bar Chart -->
        <div class="dashboard-card surface-card">
          <div class="card-header-wrap">
            <BarChart3 :size="16" class="chart-icon-rank" />
            <strong>ChatGPT 拼车销量热度排行 (前 5 名)</strong>
          </div>
          <div class="ranking-list">
            <div v-for="(item, idx) in rankingData" :key="item.title" class="rank-item">
              <div class="rank-meta">
                <span class="rank-badge" :class="`top-${idx + 1}`">{{ idx + 1 }}</span>
                <span class="rank-title">{{ item.title }}</span>
                <span class="product-chip mini" :class="item.product">{{ item.label }}</span>
              </div>
              <div class="rank-progress-bar-wrap">
                <div class="rank-progress-bar" :style="{ width: `${(item.unlocks / 50) * 100}%`, background: item.color }"></div>
                <span class="rank-val">{{ item.unlocks }} 次解锁</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Chart 3: Mini summaries -->
        <div class="dashboard-card surface-card summary-card-dashboard">
          <div class="card-header-wrap">
            <PieChart :size="16" class="chart-icon-pie" />
            <strong>今日运营快报 (实时数据模拟)</strong>
          </div>
          <div class="mini-stats-flow">
            <div class="mini-stat-box">
              <span>本月累计拼车对接</span>
              <strong>¥5,480 <small>服务费</small></strong>
            </div>
            <div class="mini-stat-box">
              <span>累计对接解锁量</span>
              <strong>2,842 <small>次</small></strong>
            </div>
            <div class="mini-stat-box">
              <span>平台已托管活跃车位</span>
              <strong>149 <small>个车位</small></strong>
            </div>
            <div class="mini-stat-box">
              <span>车友满意度评价</span>
              <strong>98.6% <small>好评率</small></strong>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {
  BarChart3,
  ChevronLeft,
  ChevronRight,
  LockKeyhole,
  PackageOpen,
  PieChart,
  PlusCircle,
  Search,
  ShieldCheck,
  TrendingUp,
} from '@lucide/vue'
import { ridesApi } from '../api/rides'
import RideCard from '../components/ride/RideCard.vue'
import type { ProductType, Ride } from '../types'

const rides = ref<Ride[]>([])
const loading = ref(true)
const query = ref('')
const activeProduct = ref<ProductType | ''>('')
const carouselTrack = ref<HTMLElement | null>(null)
let searchTimeout: ReturnType<typeof setTimeout> | null = null

const steps = [
  { title: '挑选心仪车位', desc: '对比月费租金、拼车人数、使用期限及车主公开的详细拼车说明。' },
  { title: '解锁联系方式', desc: '模拟完成服务费支付，即可实时揭晓车主的联系账号。' },
  { title: '自行对接拼车', desc: '添加车主微信或 Telegram，私下沟通订阅细节，完成搭车。' },
]

const productTabs: { label: string; value: ProductType | '' }[] = [
  { label: '全部推荐', value: '' },
  { label: 'ChatGPT Plus', value: 'chatgpt-plus' },
  { label: 'ChatGPT Team', value: 'chatgpt-team' },
  { label: 'ChatGPT Pro', value: 'chatgpt-pro' },
]

// Simulated Data for charts
const rankingData = [
  { title: '稳定老车 - GPT-4o 4人拼车位', label: 'Plus 拼车', product: 'chatgpt-plus', unlocks: 45, color: 'var(--color-plus)' },
  { title: 'Pro 极客无限 o1/o1-pro 终极车位', label: 'Pro 极客', product: 'chatgpt-pro', unlocks: 38, color: 'var(--color-pro)' },
  { title: 'Team 大号协作车位，季付稳定招募', label: 'Team 协作', product: 'chatgpt-team', unlocks: 31, color: 'var(--color-team)' },
  { title: 'Plus 体验车，支持月付测试', label: 'Plus 拼车', product: 'chatgpt-plus', unlocks: 22, color: 'var(--color-plus)' },
  { title: 'Team 高性价比 10人车，随时加入', label: 'Team 协作', product: 'chatgpt-team', unlocks: 15, color: 'var(--color-team)' },
]

const scrollLeft = () => {
  if (carouselTrack.value) {
    carouselTrack.value.scrollBy({ left: -340, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (carouselTrack.value) {
    carouselTrack.value.scrollBy({ left: 340, behavior: 'smooth' })
  }
}

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
  gap: var(--spacing-xxl);
}

/* Hero Section */
.hero-section {
  position: relative;
  padding: var(--spacing-xxl) 0;
  background-color: var(--bg-secondary);
  background-image: radial-gradient(var(--border-color-strong) 0.8px, transparent 0.8px);
  background-size: 24px 24px;
  border-bottom: 1px solid var(--border-color);
}

.hero-container {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: var(--spacing-xxl);
  align-items: center;
}

.hero-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.badge-container {
  display: inline-block;
}

.pill-badge {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 700;
  border: 1px solid var(--border-color);
}

.hero-title {
  font-size: 44px;
  font-weight: 800;
  line-height: 1.15;
  letter-spacing: -0.03em;
  color: var(--text-primary);
}

.gradient-text {
  background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
  max-width: 580px;
}

.hero-actions {
  display: flex;
  gap: var(--spacing-md);
  margin-top: var(--spacing-sm);
}

.hero-btn {
  min-width: 140px;
}

/* Process Panel */
.process-panel {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--card-shadow-hover);
  background: var(--bg-secondary);
  border-color: var(--border-color-strong);
}

.panel-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.panel-header strong {
  font-size: 15px;
  font-weight: 800;
  color: var(--text-primary);
}

.icon-circle {
  display: inline-flex;
  width: 38px;
  height: 38px;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
  color: var(--text-primary);
}

.steps-flow {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.step-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.step-item:hover {
  border-color: var(--border-color-strong);
  transform: translateX(4px);
}

.step-num {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-muted);
  font-style: italic;
  line-height: 1;
}

.step-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.step-info strong {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.step-info p {
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin: 0;
}

.panel-footer {
  display: flex;
  gap: 6px;
  padding: 10px 12px;
  border-radius: var(--border-radius-sm);
  background: var(--color-warning-soft);
  color: #854d0e;
  font-size: 11px;
  line-height: 1.5;
}

.safety-icon {
  flex-shrink: 0;
  margin-top: 1px;
}

/* Marketplace Section (Carousel) */
.marketplace-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.section-title-wrap h2 {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: var(--spacing-xs) 0 0;
  color: var(--text-primary);
}

.view-all-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.view-all-link:hover {
  color: var(--text-primary);
}

.filter-toolbar {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--spacing-md);
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  height: 44px;
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

.tabs-list {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.tab-item {
  height: 36px;
  padding: 0 16px;
  border-radius: var(--border-radius-sm);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tab-item.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* Carousel Styles */
.carousel-outer {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.carousel-track {
  display: flex;
  gap: var(--spacing-md);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  padding: 8px 0;
  width: 100%;
}

.carousel-track::-webkit-scrollbar {
  display: none; /* Hide scrollbars for a clean tech look */
}

.carousel-track {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.carousel-slide {
  scroll-snap-align: start;
  flex: 0 0 calc(33.333% - 11px); /* Three cards per view on desktop */
  display: flex;
  flex-direction: column;
  align-items: stretch;
  transition: transform var(--transition-normal);
}

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: var(--border-radius-full);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  box-shadow: var(--card-shadow);
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all var(--transition-fast);
}

.carousel-arrow:hover {
  background: var(--bg-inset);
  color: var(--text-primary);
  border-color: var(--border-color-strong);
}

.carousel-arrow.left {
  left: -20px;
}

.carousel-arrow.right {
  right: -20px;
}

/* Stats Dashboard Section */
.stats-dashboard-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  padding-bottom: var(--spacing-xl);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.9fr 0.7fr;
  gap: var(--spacing-lg);
  align-items: stretch;
}

.dashboard-card {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.card-header-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
}

.card-header-wrap strong {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-primary);
}

.chart-icon-trend {
  color: var(--color-pro);
}

.chart-icon-rank {
  color: var(--color-team);
}

.chart-icon-pie {
  color: var(--color-plus);
}

.chart-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  flex-grow: 1;
  justify-content: center;
}

.line-chart-svg {
  width: 100%;
  height: auto;
  max-height: 180px;
  overflow: visible;
}

.y-label {
  font-size: 9px;
  font-weight: 700;
}

.chart-legend {
  display: flex;
  justify-content: space-between;
  padding-top: var(--spacing-xs);
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 700;
  color: var(--text-secondary);
}

.legend-color {
  width: 10px;
  height: 4px;
  border-radius: var(--border-radius-full);
}

.legend-color.plus {
  background: var(--color-plus);
}

.legend-color.team {
  background: var(--color-team);
}

.legend-color.pro {
  background: var(--color-pro);
}

/* Rank lists */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  justify-content: center;
  flex-grow: 1;
}

.rank-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rank-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.rank-badge {
  display: inline-flex;
  width: 18px;
  height: 18px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-full);
  font-size: 10px;
  font-weight: 800;
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

.rank-badge.top-1 {
  background: var(--color-pro-soft);
  color: var(--color-pro);
}

.rank-badge.top-2 {
  background: var(--color-team-soft);
  color: var(--color-team);
}

.rank-badge.top-3 {
  background: var(--color-plus-soft);
  color: var(--color-plus);
}

.rank-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-grow: 1;
}

.product-chip.mini {
  font-size: 9px;
  padding: 1px 6px;
  min-height: 18px;
}

.rank-progress-bar-wrap {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.rank-progress-bar {
  height: 6px;
  border-radius: var(--border-radius-full);
  transition: width 0.8s ease-in-out;
  min-width: 4px;
}

.rank-val {
  font-size: 10px;
  color: var(--text-muted);
  font-weight: 700;
  white-space: nowrap;
}

/* Operational highlights */
.summary-card-dashboard {
  background: linear-gradient(135deg, #ffffff 0%, var(--bg-inset) 100%);
}

.mini-stats-flow {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  justify-content: center;
  flex-grow: 1;
}

.mini-stat-box {
  padding: 10px 12px;
  border: 1px dashed var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-secondary);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mini-stat-box span {
  font-size: 10px;
  color: var(--text-muted);
  font-weight: 700;
}

.mini-stat-box strong {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
}

.mini-stat-box strong small {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-secondary);
}

@media (max-width: 1120px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 1080px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
  }
  .filter-toolbar {
    grid-template-columns: 1fr;
  }
  .carousel-slide {
    flex: 0 0 calc(50% - 8px); /* Two cards per view on tablet */
  }
}

@media (max-width: 680px) {
  .hero-title {
    font-size: 32px;
  }
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
  .tabs-list {
    width: 100%;
    overflow-x: auto;
  }
  .carousel-slide {
    flex: 0 0 calc(100% - 20px); /* One card per view on mobile */
  }
  .carousel-arrow {
    display: none; /* Hide arrows on mobile and rely on swipe snap */
  }
}
</style>
