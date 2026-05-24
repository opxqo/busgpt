<template>
  <div class="admin-page container">
    <header class="page-header surface-card">
      <div>
        <span class="eyebrow">管理后台</span>
        <h1 class="page-title">数据分析</h1>
        <p class="page-subtitle">查看销售指标、产品排行和价格趋势，洞察平台运营状况。</p>
      </div>
      <button type="button" class="btn btn-secondary" :disabled="loading" @click="loadAll">
        <RefreshCw :size="16" />
        刷新
      </button>
    </header>

    <div v-if="loading" class="loading-container surface-card">
      <div class="spinner"></div>
      <p>加载分析数据中</p>
    </div>

    <template v-else>
      <!-- Sales Overview Cards -->
      <section class="stat-grid anim-fade-up anim-d1">
        <div class="stat-card surface-card">
          <span class="stat-label">近30天总收入</span>
          <strong class="stat-value">¥{{ formatMoney(animRevenue) }}</strong>
        </div>
        <div class="stat-card surface-card">
          <span class="stat-label">近30天已付订单</span>
          <strong class="stat-value">{{ animPaidOrders }}</strong>
        </div>
        <div class="stat-card surface-card">
          <span class="stat-label">活跃车位</span>
          <strong class="stat-value">{{ animActiveRides }}</strong>
        </div>
        <div class="stat-card surface-card">
          <span class="stat-label">平均订单金额</span>
          <strong class="stat-value">¥{{ formatMoney(animAvgAmount) }}</strong>
        </div>
      </section>

      <!-- GMV Section -->
      <section class="gmv-section surface-card anim-fade-up anim-d2">
        <h2 class="section-title">平台 GMV 估算</h2>
        <p class="section-desc">基于联系方式解锁订单，估算平台促成的交易规模</p>

        <div class="gmv-cards">
          <div class="gmv-card gmv-primary">
            <span class="gmv-label">已成交 GMV</span>
            <strong class="gmv-value">¥{{ formatMoney(animGmvExercised) }}</strong>
            <span class="gmv-sub">{{ gmv.exercised_count }} 次联系方式解锁</span>
          </div>
          <div class="gmv-card">
            <span class="gmv-label">潜在 GMV</span>
            <strong class="gmv-value">¥{{ formatMoney(animGmvPotential) }}</strong>
            <span class="gmv-sub">{{ gmv.potential_count }} 个招募座位</span>
          </div>
          <div class="gmv-card">
            <span class="gmv-label">剩余 GMV</span>
            <strong class="gmv-value">¥{{ formatMoney(animGmvRemaining) }}</strong>
            <span class="gmv-sub">{{ gmv.potential_count - gmv.exercised_count }} 个潜在名额</span>
          </div>
          <div class="gmv-card">
            <span class="gmv-label">官方基准 GMV</span>
            <strong class="gmv-value">¥{{ formatMoney(animGmvBenchmark) }}</strong>
            <span class="gmv-sub">按官方价格估算</span>
          </div>
        </div>

        <!-- GMV by Product -->
        <div v-if="gmv.by_product.length > 0" class="gmv-product-table">
          <h3 class="sub-title">按产品拆分</h3>
          <table class="records-table">
            <thead>
              <tr>
                <th>产品</th>
                <th>车位数</th>
                <th>解锁/招募名额</th>
                <th class="text-right">已成交 GMV</th>
                <th class="text-right">潜在 GMV</th>
                <th class="text-right">剩余 GMV</th>
                <th>填充率</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in gmv.by_product" :key="item.product">
                <td>
                  <span class="product-chip sm" :class="item.product">{{ item.product_label }}</span>
                </td>
                <td>{{ item.ride_count }}</td>
                <td>{{ item.exercised_count }} / {{ item.potential_count }}</td>
                <td class="text-right gmv-cell">¥{{ formatMoney(item.exercised_gmv) }}</td>
                <td class="text-right">¥{{ formatMoney(item.potential_gmv) }}</td>
                <td class="text-right">¥{{ formatMoney(item.remaining_gmv) }}</td>
                <td>
                  <div class="fill-bar-wrap">
                    <div
                      class="fill-bar"
                      :class="item.product"
                      :style="{ width: fillRate(item.exercised_count, item.potential_count) + '%' }"
                    ></div>
                    <span class="fill-text">{{ fillRate(item.exercised_count, item.potential_count) }}%</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Rankings Section -->
      <section class="rankings-section anim-fade-up anim-d3">
        <!-- Product Rankings -->
        <div class="ranking-card surface-card">
          <h2 class="section-title">产品订单排行</h2>
          <p class="section-desc">近30天各产品类型按订单量排名</p>
          <div v-if="productRankings.length === 0" class="empty-inline">暂无数据</div>
          <div v-else class="ranking-list">
            <div v-for="(item, idx) in productRankings" :key="item.product" class="ranking-item">
              <div class="ranking-header">
                <span class="ranking-rank">#{{ idx + 1 }}</span>
                <span class="product-chip" :class="item.product">
                  <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                    <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
                  </svg>
                  <span>{{ item.product_label }}</span>
                </span>
                <span class="ranking-orders">{{ item.orders }} 单</span>
              </div>
              <div class="ranking-bar-wrap">
                <div
                  class="ranking-bar"
                  :class="item.product"
                  :style="{ width: barWidth(item.orders, maxProductOrders) + '%' }"
                ></div>
              </div>
              <div class="ranking-meta">
                <span>收入 ¥{{ formatMoney(item.revenue) }}</span>
                <span>均单 ¥{{ formatMoney(item.average_order_amount) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Ride Rankings -->
        <div class="ranking-card surface-card">
          <h2 class="section-title">热门车位排行</h2>
          <p class="section-desc">近30天按订单量排名的热门车位</p>
          <div v-if="rideRankings.length === 0" class="empty-inline">暂无数据</div>
          <div v-else class="ranking-list">
            <div v-for="(item, idx) in rideRankings" :key="item.ride_id" class="ranking-item">
              <div class="ranking-header">
                <span class="ranking-rank">#{{ idx + 1 }}</span>
                <router-link :to="`/ride/${item.ride_id}`" class="ranking-title">{{ item.ride_title }}</router-link>
                <span class="ranking-orders">{{ item.orders }} 单</span>
              </div>
              <div class="ranking-bar-wrap">
                <div
                  class="ranking-bar"
                  :class="item.product"
                  :style="{ width: barWidth(item.orders, maxRideOrders) + '%' }"
                ></div>
              </div>
              <div class="ranking-meta">
                <span class="product-chip sm" :class="item.product">{{ productLabel(item.product) }}</span>
                <span>收入 ¥{{ formatMoney(item.revenue) }}</span>
                <span>余座 {{ item.remaining_seats }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Price Trends -->
      <section class="trends-section surface-card anim-fade-up anim-d4">
        <h2 class="section-title">价格趋势</h2>
        <p class="section-desc">近期各产品平均月费和联系方式价格变化</p>

        <div v-if="priceTrends.length === 0" class="empty-inline">暂无数据</div>
        <div v-else class="table-container">
          <table class="records-table">
            <thead>
              <tr>
                <th>日期</th>
                <th>产品</th>
                <th>新增车位</th>
                <th class="text-right">平均月费</th>
                <th class="text-right">平均联系价格</th>
                <th class="text-right">最低月费</th>
                <th class="text-right">最高月费</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in priceTrends" :key="idx">
                <td class="date-col">{{ item.date }}</td>
                <td>
                  <span class="product-chip sm" :class="item.product">{{ productLabel(item.product) }}</span>
                </td>
                <td>{{ item.ride_count }}</td>
                <td class="text-right">¥{{ formatMoney(item.average_price_per_month) }}</td>
                <td class="text-right">¥{{ formatMoney(item.average_contact_price) }}</td>
                <td class="text-right">¥{{ formatMoney(item.minimum_price_per_month) }}</td>
                <td class="text-right">¥{{ formatMoney(item.maximum_price_per_month) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { type Ref, ref, computed, onMounted, watch } from 'vue'
import { RefreshCw } from '@lucide/vue'
import { analyticsApi, type SalesOverview, type PriceTrendPoint, type RideRankingItem } from '../../api/analytics'
import type { ProductRankingItem, GmvResponse } from '../../api/analytics'

const loading = ref(true)
const salesOverview = ref<SalesOverview>({
  total_revenue: 0,
  paid_orders: 0,
  active_rides: 0,
  new_rides: 0,
  average_order_amount: 0,
})
const productRankings = ref<ProductRankingItem[]>([])
const rideRankings = ref<RideRankingItem[]>([])
const priceTrends = ref<PriceTrendPoint[]>([])
const gmv = ref<GmvResponse>({
  exercised_gmv: 0,
  potential_gmv: 0,
  remaining_gmv: 0,
  benchmark_gmv: 0,
  exercised_count: 0,
  potential_count: 0,
  active_rides: 0,
  by_product: [],
})

// Count-up animation
const animateValue = (target: Ref<number>, end: number, duration = 600) => {
  const start = target.value
  if (start === end) return
  const startTime = performance.now()
  const tick = (now: number) => {
    const elapsed = now - startTime
    const progress = Math.min(elapsed / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    target.value = Math.round(start + (end - start) * eased)
    if (progress < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

const animRevenue = ref(0)
const animPaidOrders = ref(0)
const animActiveRides = ref(0)
const animAvgAmount = ref(0)
const animGmvExercised = ref(0)
const animGmvPotential = ref(0)
const animGmvRemaining = ref(0)
const animGmvBenchmark = ref(0)

watch(() => salesOverview.value.total_revenue, (v) => animateValue(animRevenue, Number(v)), { immediate: true })
watch(() => salesOverview.value.paid_orders, (v) => animateValue(animPaidOrders, v), { immediate: true })
watch(() => salesOverview.value.active_rides, (v) => animateValue(animActiveRides, v), { immediate: true })
watch(() => salesOverview.value.average_order_amount, (v) => animateValue(animAvgAmount, Number(v)), { immediate: true })
watch(() => gmv.value.exercised_gmv, (v) => animateValue(animGmvExercised, Number(v)), { immediate: true })
watch(() => gmv.value.potential_gmv, (v) => animateValue(animGmvPotential, Number(v)), { immediate: true })
watch(() => gmv.value.remaining_gmv, (v) => animateValue(animGmvRemaining, Number(v)), { immediate: true })
watch(() => gmv.value.benchmark_gmv, (v) => animateValue(animGmvBenchmark, Number(v)), { immediate: true })

const maxProductOrders = computed(() => {
  if (productRankings.value.length === 0) return 1
  return Math.max(...productRankings.value.map((i) => i.orders), 1)
})

const maxRideOrders = computed(() => {
  if (rideRankings.value.length === 0) return 1
  return Math.max(...rideRankings.value.map((i) => i.orders), 1)
})

const productLabels: Record<string, string> = {
  'chatgpt-plus': 'Plus',
  'chatgpt-team': 'Business',
  'chatgpt-pro': 'Pro',
}

const productLabel = (product: string) => productLabels[product] || product

const formatMoney = (value: number | string) => {
  const num = Number(value || 0)
  if (num >= 10000) return `${(num / 10000).toFixed(1)}万`
  return Math.round(num * 100) / 100
}

const fillRate = (exercised: number, potential: number) => {
  if (potential <= 0) return 0
  return Math.round((exercised / potential) * 100)
}

const barWidth = (value: number, max: number) => {
  if (max <= 0) return 0
  return Math.round((value / max) * 100)
}

const loadAll = async () => {
  loading.value = true
  try {
    const [salesRes, prodRes, rideRes, priceRes, gmvRes] = await Promise.all([
      analyticsApi.getSalesOverview(30),
      analyticsApi.getProductRankings(30, 10),
      analyticsApi.getRideRankings(30, 10),
      analyticsApi.getPriceTrends(30),
      analyticsApi.getGmv(),
    ])
    salesOverview.value = salesRes.data
    productRankings.value = prodRes.data
    rideRankings.value = rideRes.data
    priceTrends.value = priceRes.data
    gmv.value = gmvRes.data
  } catch {
    // ignore
  } finally {
    loading.value = false
  }
}

onMounted(loadAll)
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
.anim-d4 { animation-delay: 0.28s; }

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.admin-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--border-color-strong);
  opacity: 0.6;
}

.page-title {
  margin: 4px 0 6px;
}

/* Stat Cards */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-plus);
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.stat-card:nth-child(2)::before { background: var(--color-team); }
.stat-card:nth-child(3)::before { background: var(--color-plus); }
.stat-card:nth-child(4)::before { background: var(--color-pro); }

.stat-card:hover {
  border-color: var(--border-color-strong);
  box-shadow: var(--card-shadow);
  transform: translateY(-1px);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-label {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 600;
}

.stat-value {
  color: var(--text-primary);
  font-size: 26px;
  font-weight: 900;
  line-height: 1;
  transition: color var(--transition-fast);
}

.stat-card:nth-child(1):hover .stat-value { color: var(--color-plus); }
.stat-card:nth-child(2):hover .stat-value { color: var(--color-team); }
.stat-card:nth-child(3):hover .stat-value { color: var(--color-plus); }
.stat-card:nth-child(4):hover .stat-value { color: var(--color-pro); }

/* GMV Section */
.gmv-section {
  padding: var(--spacing-lg);
}

.gmv-cards {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.gmv-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  transition: all var(--transition-normal);
}

.gmv-card:hover {
  border-color: var(--border-color-strong);
  box-shadow: var(--card-shadow);
  transform: translateY(-1px);
}

.gmv-card.gmv-primary {
  background: color-mix(in srgb, var(--color-plus-soft) 40%, var(--bg-card));
  border-color: rgba(16, 185, 129, 0.25);
}

.gmv-card {
  position: relative;
  overflow: hidden;
}

.gmv-card::before {
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

.gmv-card:nth-child(1)::before { background: var(--color-plus); }
.gmv-card:nth-child(2)::before { background: var(--color-team); }
.gmv-card:nth-child(3)::before { background: var(--color-pro); }
.gmv-card:nth-child(4)::before { background: var(--color-info); }

.gmv-card:hover::before {
  opacity: 1;
}

.gmv-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.gmv-value {
  font-size: 22px;
  font-weight: 900;
  color: var(--text-primary);
  line-height: 1.2;
}

.gmv-primary .gmv-value {
  color: var(--color-plus);
}

.gmv-sub {
  font-size: 12px;
  color: var(--text-muted);
}

.gmv-product-table {
  margin-top: var(--spacing-md);
}

.sub-title {
  margin: 0 0 var(--spacing-sm);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
}

.gmv-cell {
  font-weight: 700;
  color: var(--text-primary);
}

.fill-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 100px;
}

.fill-bar-wrap {
  position: relative;
  height: 8px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
  overflow: hidden;
  min-width: 80px;
}

.fill-bar {
  height: 100%;
  border-radius: var(--border-radius-full);
  animation: bar-fill-in 0.6s ease-out both;
}

.fill-bar.chatgpt-plus { background: var(--color-plus); }
.fill-bar.chatgpt-team { background: var(--color-team); }
.fill-bar.chatgpt-pro { background: var(--color-pro); }

.fill-text {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  white-space: nowrap;
  min-width: 32px;
  text-align: right;
}

/* Rankings */
.rankings-section {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.ranking-card {
  padding: var(--spacing-lg);
}

.section-title {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 24px;
  height: 2px;
  border-radius: var(--border-radius-full);
  background: var(--color-team);
  opacity: 0.6;
}

.section-desc {
  margin: 0 0 var(--spacing-md);
  color: var(--text-muted);
  font-size: 13px;
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.ranking-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px;
  border-radius: var(--border-radius-md);
  transition: background-color var(--transition-fast), border-color var(--transition-fast);
  border-left: 3px solid transparent;
}

.ranking-item:hover {
  background: var(--bg-tertiary);
  border-left-color: var(--color-plus);
}

.ranking-item:nth-child(1):hover { border-left-color: var(--color-pro); }
.ranking-item:nth-child(2):hover { border-left-color: var(--color-team); }
.ranking-item:nth-child(3):hover { border-left-color: var(--color-plus); }

/* Staggered ranking entrance */
.ranking-item {
  opacity: 0;
  transform: translateY(6px);
  animation: rankFadeIn 0.35s ease-out forwards;
}

.ranking-item:nth-child(1) { animation-delay: 0.05s; }
.ranking-item:nth-child(2) { animation-delay: 0.1s; }
.ranking-item:nth-child(3) { animation-delay: 0.15s; }
.ranking-item:nth-child(4) { animation-delay: 0.2s; }
.ranking-item:nth-child(5) { animation-delay: 0.25s; }

@keyframes rankFadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.ranking-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ranking-rank {
  font-size: 12px;
  font-weight: 800;
  color: var(--text-muted);
  min-width: 24px;
}

.ranking-title {
  flex: 1;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  text-decoration: none;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ranking-title:hover {
  text-decoration: underline;
}

.ranking-orders {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}

.ranking-bar-wrap {
  height: 8px;
  border-radius: var(--border-radius-full);
  background: var(--bg-inset);
  overflow: hidden;
}

.ranking-bar {
  height: 100%;
  border-radius: var(--border-radius-full);
  animation: bar-fill-in 0.6s ease-out both;
}

@keyframes bar-fill-in {
  from {
    width: 0 !important;
  }
}

.ranking-bar.chatgpt-plus {
  background: var(--color-plus);
}

.ranking-bar.chatgpt-team {
  background: var(--color-team);
}

.ranking-bar.chatgpt-pro {
  background: var(--color-pro);
}

.ranking-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: var(--text-muted);
}

/* Product Chip */
.product-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 12px;
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: 700;
}

.product-chip.sm {
  padding: 2px 8px;
  font-size: 11px;
}

.chip-logo {
  width: 14px;
  height: 14px;
}

.product-chip.chatgpt-plus {
  background: var(--color-plus-soft);
  color: var(--color-plus);
}

.product-chip.chatgpt-team {
  background: var(--color-team-soft);
  color: var(--color-team);
}

.product-chip.chatgpt-pro {
  background: var(--color-pro-soft);
  color: var(--color-pro);
}

/* Trends Table */
.trends-section {
  padding: var(--spacing-lg);
}

.table-container {
  margin-top: var(--spacing-md);
}

.records-table th,
.records-table td {
  padding: 10px 14px;
}

.records-table tbody tr {
  transition: background-color var(--transition-fast);
}

.records-table tbody tr:hover {
  background: var(--bg-tertiary);
}

.text-right {
  text-align: right;
}

.date-col {
  color: var(--text-muted);
  white-space: nowrap;
}

.empty-inline {
  padding: var(--spacing-lg);
  text-align: center;
  color: var(--text-muted);
  font-size: 14px;
}

@media (max-width: 1080px) {
  .rankings-section {
    grid-template-columns: 1fr;
  }

  .stat-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .gmv-cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .stat-grid,
  .gmv-cards {
    grid-template-columns: 1fr;
  }
}

/* Dark mode */
:global([data-theme="dark"] .stat-card:hover ){
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

:global([data-theme="dark"] .gmv-card:hover ){
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

:global([data-theme="dark"] .gmv-card.gmv-primary ){
  background: color-mix(in srgb, var(--color-success-soft) 12%, var(--bg-tertiary));
  border-color: rgba(52, 211, 153, 0.2);
}

:global([data-theme="dark"] .ranking-item:hover ){
  background: var(--bg-inset);
}

:global([data-theme="dark"] .records-table tbody tr:hover ){
  background: var(--bg-inset);
}

:global([data-theme="dark"] .section-title::after ){
  opacity: 0.4;
}
</style>
