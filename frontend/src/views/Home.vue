<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section ref="heroSection" class="hero-section">
      <div class="hero-bg-pattern" aria-hidden="true">
        <div
          class="hero-bg-track"
          :style="{
            gridTemplateColumns: `repeat(${heroPatternCols}, var(--hero-pattern-cell-size))`,
            width: `${heroPatternCols * HERO_PATTERN_CELL_SIZE}px`,
            height: `${heroPatternRows * HERO_PATTERN_CELL_SIZE}px`,
          }"
        >
          <span v-for="tile in heroPatternTiles" :key="tile" class="hero-bg-tile">
            <span class="hero-bg-dot"></span>
            <span class="hero-bg-plus"></span>
          </span>
        </div>
      </div>
      <div class="hero-container container">
        <div class="hero-content">
          <div class="badge-container">
            <span class="pill-badge">BusGPT 车位信息聚合台</span>
          </div>
          <h1 class="hero-title">
            发现可用 AI 订阅车位<br />
            <span class="gradient-text">直接获取车主联系方式</span>
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
              <Search :size="20" />
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
            <span>平台仅作信息聚合，请线下自行核实订阅细节与支付方式。</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Recommended Marketplace Section (Carousel) -->
    <section class="container marketplace-section">
      <div class="section-header">
        <div class="section-title-wrap">
          <span class="eyebrow">实时推荐</span>
          <h2>最新拼车车位</h2>
        </div>
        <div class="nav-and-view-all">
          <router-link to="/market" class="view-all-link">
            <span>查看全部车位</span>
            <ChevronRight :size="16" />
          </router-link>
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
      <div
        v-else
        class="carousel-outer"
        @touchstart="pauseCarousel"
        @touchend="resumeCarousel"
      >
        <button type="button" class="carousel-arrow left" @click="showPreviousRide" aria-label="向左滑动">
          <ChevronLeft :size="20" />
        </button>
        
        <div
          class="carousel-track"
          :style="{ transform: `translateX(calc(-${activeCarouselIndex} * var(--carousel-step)))` }"
          ref="carouselTrack"
        >
          <div v-for="ride in rides" :key="ride.id" class="carousel-slide">
            <RideCard :ride="ride" />
          </div>
        </div>

        <button type="button" class="carousel-arrow right" @click="showNextRide" aria-label="向右滑动">
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
                <div class="rank-progress-bar" :style="{ width: `${(item.seats / 50) * 100}%`, background: item.color }"></div>
                <span class="rank-val">{{ item.seats }} 人拼车</span>
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
              <span>本月新增拼车</span>
              <strong>326 <small>单</small></strong>
            </div>
            <div class="mini-stat-box">
              <span>累计成功对接</span>
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
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import {
  BarChart3,
  ChevronLeft,
  ChevronRight,
  PackageOpen,
  PieChart,
  PlusCircle,
  Search,
  ShieldCheck,
  TrendingUp,
} from '@lucide/vue'
import { ridesApi } from '../api/rides'
import RideCard from '../components/ride/RideCard.vue'
import type { Ride } from '../types'

const rides = ref<Ride[]>([])
const loading = ref(true)
const heroSection = ref<HTMLElement | null>(null)
const heroPatternCols = ref(0)
const heroPatternRows = ref(0)
const carouselTrack = ref<HTMLElement | null>(null)
const carouselPaused = ref(false)
const activeCarouselIndex = ref(0)
const visibleRideCount = ref(3)
let carouselTimer: ReturnType<typeof setInterval> | null = null
let carouselFirstMoveTimer: ReturnType<typeof setTimeout> | null = null
let resizeTimer: ReturnType<typeof setTimeout> | null = null
const HERO_PATTERN_CELL_SIZE = 36

const heroPatternTiles = computed(() => heroPatternCols.value * heroPatternRows.value)

const steps = [
  { title: '挑选心仪车位', desc: '对比月费租金、拼车人数、使用期限及车主公开的详细拼车说明。' },
  { title: '查看联系方式', desc: '直接查看车主的微信、Telegram 等联系账号，无需额外付费。' },
  { title: '自行对接拼车', desc: '添加车主微信或 Telegram，私下沟通订阅细节，完成搭车。' },
]

// Simulated Data for charts
const rankingData = [
  { title: '稳定老车 - GPT-4o 4人拼车位', label: 'Plus 拼车', product: 'chatgpt-plus', seats: 45, color: 'var(--color-plus)' },
  { title: 'Pro 极客无限 o1/o1-pro 终极车位', label: 'Pro 极客', product: 'chatgpt-pro', seats: 38, color: 'var(--color-pro)' },
  { title: 'Team 大号协作车位，季付稳定招募', label: 'Team 协作', product: 'chatgpt-team', seats: 31, color: 'var(--color-team)' },
  { title: 'Plus 体验车，支持月付测试', label: 'Plus 拼车', product: 'chatgpt-plus', seats: 22, color: 'var(--color-plus)' },
  { title: 'Team 高性价比 10人车，随时加入', label: 'Team 协作', product: 'chatgpt-team', seats: 15, color: 'var(--color-team)' },
]

const maxCarouselIndex = computed(() => Math.max(rides.value.length - visibleRideCount.value, 0))

const syncVisibleRideCount = () => {
  if (window.innerWidth <= 680) visibleRideCount.value = 1
  else if (window.innerWidth <= 1080) visibleRideCount.value = 2
  else visibleRideCount.value = 3

  activeCarouselIndex.value = Math.min(activeCarouselIndex.value, maxCarouselIndex.value)
}

const renderHeroPattern = () => {
  const rect = heroSection.value?.getBoundingClientRect()
  const padding = HERO_PATTERN_CELL_SIZE * 8
  const width = rect?.width || window.innerWidth
  const height = rect?.height || window.innerHeight

  heroPatternCols.value = Math.ceil((width + padding * 2) / HERO_PATTERN_CELL_SIZE)
  heroPatternRows.value = Math.ceil((height + padding * 2) / HERO_PATTERN_CELL_SIZE)
}

const handleResize = () => {
  syncVisibleRideCount()
  if (resizeTimer) clearTimeout(resizeTimer)
  resizeTimer = setTimeout(renderHeroPattern, 120)
}

const showPreviousRide = () => {
  activeCarouselIndex.value =
    activeCarouselIndex.value <= 0 ? maxCarouselIndex.value : activeCarouselIndex.value - 1
}

const showNextRide = () => {
  activeCarouselIndex.value =
    activeCarouselIndex.value >= maxCarouselIndex.value ? 0 : activeCarouselIndex.value + 1
}

const pauseCarousel = () => {
  carouselPaused.value = true
}

const resumeCarousel = () => {
  carouselPaused.value = false
}

const stopCarousel = () => {
  if (carouselFirstMoveTimer) {
    clearTimeout(carouselFirstMoveTimer)
    carouselFirstMoveTimer = null
  }

  if (carouselTimer) {
    clearInterval(carouselTimer)
    carouselTimer = null
  }
}

const startCarousel = () => {
  if (carouselTimer) clearInterval(carouselTimer)

  carouselTimer = setInterval(() => {
    if (!carouselPaused.value) {
      showNextRide()
    }
  }, 3200)
}

const fetchRides = async () => {
  loading.value = true
  try {
    const res = await ridesApi.getRides()
    rides.value = res.data
  } catch (err) {
    console.error('Failed to load rides', err)
    rides.value = []
  } finally {
    loading.value = false
    activeCarouselIndex.value = 0
    stopCarousel()
    carouselFirstMoveTimer = setTimeout(() => {
      carouselFirstMoveTimer = null
      if (!carouselPaused.value) showNextRide()
      startCarousel()
    }, 900)
  }
}

onMounted(() => {
  syncVisibleRideCount()
  renderHeroPattern()
  window.addEventListener('resize', handleResize)
  fetchRides()
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (resizeTimer) clearTimeout(resizeTimer)
  stopCarousel()
})
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
  overflow: hidden;
  border-bottom: 1px solid var(--border-color);
  --hero-pattern-bg: #fbfaf8;
  --hero-pattern-cell-size: 36px;
  --hero-pattern-half-move-size: -36px;
  --hero-pattern-move-size: -72px;
  --hero-pattern-color: 174, 140, 98;
  --hero-pattern-dot-opacity: 0.4;
  --hero-pattern-icon-opacity: 0.46;
  --hero-pattern-duration: 7.6s;
  --hero-pattern-ease: cubic-bezier(0.45, 0, 0.12, 1);
  background-color: var(--hero-pattern-bg);
}

[data-theme="dark"] .hero-section {
  --hero-pattern-bg: #181816;
  --hero-pattern-color: 243, 240, 233;
  --hero-pattern-dot-opacity: 0.22;
  --hero-pattern-icon-opacity: 0.3;
}

.hero-bg-pattern {
  position: absolute;
  inset: -90px;
  overflow: hidden;
  pointer-events: none;
}

.hero-bg-track {
  position: absolute;
  left: 0;
  top: 0;
  display: grid;
  grid-auto-rows: var(--hero-pattern-cell-size);
  will-change: transform;
  animation: hero-bg-drift var(--hero-pattern-duration) var(--hero-pattern-ease) infinite;
}

.hero-bg-tile {
  position: relative;
  width: var(--hero-pattern-cell-size);
  height: var(--hero-pattern-cell-size);
}

.hero-bg-dot,
.hero-bg-plus {
  position: absolute;
  left: 50%;
  top: 50%;
  display: block;
  will-change: opacity, transform;
  animation-duration: var(--hero-pattern-duration);
  animation-timing-function: var(--hero-pattern-ease);
  animation-iteration-count: infinite;
}

.hero-bg-dot {
  width: 4.8px;
  height: 4.8px;
  border-radius: var(--border-radius-full);
  background: rgba(var(--hero-pattern-color), var(--hero-pattern-dot-opacity));
  animation-name: hero-dot-morph;
}

.hero-bg-plus {
  width: 18px;
  height: 18px;
  opacity: 0;
  background: rgba(var(--hero-pattern-color), var(--hero-pattern-icon-opacity));
  mask: url('/icons/openai.svg') center / contain no-repeat;
  -webkit-mask: url('/icons/openai.svg') center / contain no-repeat;
  animation-name: hero-plus-morph;
}

@keyframes hero-bg-drift {
  0% {
    transform: translate3d(0, 0, 0);
  }

  50% {
    transform: translate3d(var(--hero-pattern-half-move-size), var(--hero-pattern-half-move-size), 0);
  }

  100% {
    transform: translate3d(var(--hero-pattern-move-size), var(--hero-pattern-move-size), 0);
  }
}

@keyframes hero-dot-morph {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) rotate(0deg);
  }

  50% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.58) rotate(-90deg);
  }

  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) rotate(0deg);
  }
}

@keyframes hero-plus-morph {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.58) rotate(90deg);
  }

  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) rotate(0deg);
  }

  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.58) rotate(90deg);
  }
}

.hero-container {
  position: relative;
  z-index: 1;
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
  letter-spacing: 0;
  color: var(--text-primary);
}

.gradient-text {
  background: linear-gradient(135deg, var(--color-plus) 0%, var(--color-team) 100%);
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
  color: var(--color-warning);
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
  letter-spacing: 0;
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

/* Carousel Styles */
.carousel-outer {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  overflow: hidden;
}

.carousel-track {
  display: flex;
  flex: 0 0 100%;
  gap: var(--spacing-md);
  padding: 8px 0;
  width: 100%;
  --carousel-step: calc((100% - var(--spacing-md) * 2) / 3 + var(--spacing-md));
  transition: transform 420ms cubic-bezier(0.22, 1, 0.36, 1);
  will-change: transform;
}

.carousel-slide {
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
  border-color: color-mix(in srgb, var(--color-info) 24%, var(--border-color));
  background:
    linear-gradient(135deg, color-mix(in srgb, var(--color-info-soft) 72%, transparent) 0%, transparent 62%),
    var(--bg-card);
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
  border: 1px solid color-mix(in srgb, var(--color-info) 18%, var(--border-color));
  border-radius: var(--border-radius-md);
  background: color-mix(in srgb, var(--bg-secondary) 88%, var(--color-info-soft));
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
  .carousel-slide {
    flex: 0 0 calc(50% - 8px); /* Two cards per view on tablet */
  }
  .carousel-track {
    --carousel-step: calc((100% - var(--spacing-md)) / 2 + var(--spacing-md));
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
  .carousel-slide {
    flex: 0 0 calc(100% - 20px); /* One card per view on mobile */
  }
  .carousel-track {
    --carousel-step: calc(100% - 4px);
  }
  .carousel-arrow {
    display: none; /* Hide arrows on mobile and rely on swipe snap */
  }
}

@media (prefers-reduced-motion: reduce) {
  .carousel-track {
    transition: none;
  }

  .hero-bg-track,
  .hero-bg-dot,
  .hero-bg-plus {
    animation: none;
  }

  .hero-bg-dot {
    opacity: 1;
    transform: translate(-50%, -50%);
  }

  .hero-bg-plus {
    opacity: 0;
  }
}
</style>
