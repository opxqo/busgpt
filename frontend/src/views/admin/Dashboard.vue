<template>
  <div class="admin-page container">
    <header class="page-header surface-card anim-fade-up">
      <div>
        <span class="eyebrow">管理后台</span>
        <h1 class="page-title">平台概览</h1>
        <p class="page-subtitle">查看平台核心运营数据，掌握整体业务状况。</p>
      </div>
      <button type="button" class="btn btn-secondary" :disabled="loading" @click="loadOverview">
        <RefreshCw :size="16" />
        刷新
      </button>
    </header>

    <div v-if="loading" class="loading-container surface-card anim-fade-up anim-d1">
      <div class="spinner"></div>
      <p>加载平台数据中</p>
    </div>

    <section v-else class="stat-grid anim-fade-up anim-d1">
      <router-link to="/admin/users" class="stat-card surface-card stat-link">
        <div class="stat-icon-wrap">
          <Users :size="20" class="stat-icon" />
        </div>
        <span class="stat-label">总用户数</span>
        <strong class="stat-value">{{ animUsers }}</strong>
      </router-link>

      <router-link to="/admin/rides" class="stat-card surface-card stat-link">
        <div class="stat-icon-wrap">
          <ParkingSquare :size="20" class="stat-icon" />
        </div>
        <span class="stat-label">总车位数</span>
        <strong class="stat-value">{{ animRides }}</strong>
      </router-link>

      <router-link to="/admin/rides" class="stat-card surface-card stat-link">
        <div class="stat-icon-wrap icon-active">
          <ParkingSquare :size="20" class="stat-icon" />
        </div>
        <span class="stat-label">活跃车位</span>
        <strong class="stat-value">{{ animActive }}</strong>
      </router-link>

      <router-link to="/admin/orders" class="stat-card surface-card stat-link">
        <div class="stat-icon-wrap">
          <ClipboardList :size="20" class="stat-icon" />
        </div>
        <span class="stat-label">总订单数</span>
        <strong class="stat-value">{{ animOrders }}</strong>
      </router-link>

      <router-link to="/admin/orders" class="stat-card surface-card stat-link">
        <div class="stat-icon-wrap icon-revenue">
          <DollarSign :size="20" class="stat-icon" />
        </div>
        <span class="stat-label">总收入</span>
        <strong class="stat-value">¥{{ formatMoney(animRevenue) }}</strong>
      </router-link>

      <router-link to="/admin/users" class="stat-card surface-card stat-link">
        <div class="stat-icon-wrap icon-new">
          <UserPlus :size="20" class="stat-icon" />
        </div>
        <span class="stat-label">今日新增用户</span>
        <strong class="stat-value">{{ animNewUsers }}</strong>
      </router-link>
    </section>

    <!-- Quick Navigation -->
    <section class="quick-nav-section anim-fade-up anim-d2">
      <h2 class="section-title">管理功能</h2>
      <div class="quick-nav-grid">
        <router-link v-for="item in quickNavItems" :key="item.to" :to="item.to" class="quick-nav-card surface-card">
          <div class="quick-nav-icon" :class="item.accent">
            <component :is="item.icon" :size="20" />
          </div>
          <div class="quick-nav-info">
            <strong>{{ item.label }}</strong>
            <p>{{ item.desc }}</p>
          </div>
          <ChevronRight :size="16" class="quick-nav-arrow" />
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { type Ref, onMounted, ref, watch } from 'vue'
import { RefreshCw, Users, ParkingSquare, ClipboardList, DollarSign, UserPlus, ChevronRight, BarChart3, Boxes } from '@lucide/vue'
import { adminApi } from '../../api/admin'
import type { AdminOverview } from '../../types'

const loading = ref(true)

const quickNavItems = [
  { to: '/admin/users', label: '用户管理', desc: '查看、搜索、启用或禁用平台用户', icon: Users, accent: 'accent-blue' },
  { to: '/admin/rides', label: '车位管理', desc: '管理车位状态、搜索和筛选车位信息', icon: ParkingSquare, accent: 'accent-green' },
  { to: '/admin/orders', label: '订单管理', desc: '查看全部订单记录，按状态筛选', icon: ClipboardList, accent: 'accent-amber' },
  { to: '/admin/analytics', label: '数据分析', desc: '销售指标、GMV 估算、产品排行和价格趋势', icon: BarChart3, accent: 'accent-purple' },
  { to: '/admin/products', label: '产品维护', desc: '维护产品档位、官方价格和展示说明', icon: Boxes, accent: 'accent-slate' },
]

const overview = ref<AdminOverview>({
  total_users: 0,
  total_rides: 0,
  total_orders: 0,
  total_revenue: 0,
  active_rides: 0,
  today_new_users: 0,
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

const animUsers = ref(0)
const animRides = ref(0)
const animActive = ref(0)
const animOrders = ref(0)
const animRevenue = ref(0)
const animNewUsers = ref(0)

watch(() => overview.value.total_users, (v) => animateValue(animUsers, v), { immediate: true })
watch(() => overview.value.total_rides, (v) => animateValue(animRides, v), { immediate: true })
watch(() => overview.value.active_rides, (v) => animateValue(animActive, v), { immediate: true })
watch(() => overview.value.total_orders, (v) => animateValue(animOrders, v), { immediate: true })
watch(() => overview.value.total_revenue, (v) => animateValue(animRevenue, Number(v)), { immediate: true })
watch(() => overview.value.today_new_users, (v) => animateValue(animNewUsers, v), { immediate: true })

const loadOverview = async () => {
  loading.value = true
  try {
    const res = await adminApi.getOverview()
    overview.value = res.data
  } catch {
    // ignore
  } finally {
    loading.value = false
  }
}

const formatMoney = (value: number | string) => {
  const num = Number(value || 0)
  if (num >= 10000) return `${(num / 10000).toFixed(1)}万`
  return Math.round(num)
}

onMounted(loadOverview)
</script>

<style scoped>
.admin-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* ===== Animations ===== */
.anim-fade-up {
  animation: fadeUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.anim-d1 { animation-delay: 0.08s; }
.anim-d2 { animation-delay: 0.16s; }

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  border-radius: 0 0 var(--border-radius-full) var(--border-radius-full);
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card:nth-child(1)::before { background: var(--color-info); }
.stat-card:nth-child(2)::before { background: var(--color-plus); }
.stat-card:nth-child(3)::before { background: var(--color-plus); }
.stat-card:nth-child(4)::before { background: var(--color-team); }
.stat-card:nth-child(5)::before { background: var(--color-warning); }
.stat-card:nth-child(6)::before { background: var(--color-info); }

.stat-link {
  text-decoration: none;
  cursor: pointer;
  transition: all var(--transition-normal);
  border: 1px solid var(--border-color);
}

.stat-link:hover {
  transform: translateY(-2px);
  box-shadow: var(--card-shadow-hover);
  border-color: var(--border-color-strong);
}

.stat-link:hover .stat-value {
  color: var(--color-primary);
}

.stat-icon-wrap {
  display: inline-flex;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  margin-bottom: var(--spacing-xs);
}

.stat-icon {
  color: var(--text-secondary);
}

.stat-icon-wrap.icon-active {
  background: var(--color-plus-soft);
  border-color: rgba(16, 185, 129, 0.2);
}

.stat-icon-wrap.icon-active .stat-icon {
  color: var(--color-plus);
}

.stat-icon-wrap.icon-revenue {
  background: var(--color-warning-soft);
  border-color: rgba(217, 119, 6, 0.2);
}

.stat-icon-wrap.icon-revenue .stat-icon {
  color: var(--color-warning);
}

.stat-icon-wrap.icon-new {
  background: var(--color-info-soft);
  border-color: rgba(15, 106, 191, 0.2);
}

.stat-icon-wrap.icon-new .stat-icon {
  color: var(--color-info);
}

.stat-label {
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 600;
}

.stat-value {
  color: var(--text-primary);
  font-size: 28px;
  font-weight: 900;
  line-height: 1;
}

/* Quick Navigation */
.quick-nav-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.section-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

.quick-nav-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.quick-nav-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  text-decoration: none;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  transition: all var(--transition-normal);
  cursor: pointer;
}

.quick-nav-card:hover {
  border-color: var(--border-color-strong);
  box-shadow: var(--card-shadow);
  transform: translateX(4px);
}

.quick-nav-card:hover .quick-nav-icon.accent-blue {
  box-shadow: 0 0 0 3px rgba(15, 106, 191, 0.1);
}

.quick-nav-card:hover .quick-nav-icon.accent-green {
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.quick-nav-card:hover .quick-nav-icon.accent-amber {
  box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.1);
}

.quick-nav-card:hover .quick-nav-icon.accent-purple {
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.quick-nav-card:hover .quick-nav-icon.accent-slate {
  box-shadow: 0 0 0 3px rgba(100, 116, 139, 0.1);
}

.quick-nav-card:hover .quick-nav-arrow {
  color: var(--text-primary);
  transform: translateX(2px);
}

.quick-nav-icon {
  display: inline-flex;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  flex-shrink: 0;
}

.quick-nav-icon.accent-blue {
  background: var(--color-info-soft);
  color: var(--color-info);
}

.quick-nav-icon.accent-green {
  background: var(--color-plus-soft);
  color: var(--color-plus);
}

.quick-nav-icon.accent-amber {
  background: var(--color-warning-soft);
  color: var(--color-warning);
}

.quick-nav-icon.accent-purple {
  background: var(--color-pro-soft);
  color: var(--color-pro);
}

.quick-nav-icon.accent-slate {
  background: var(--bg-inset);
  color: var(--text-secondary);
}

.quick-nav-info {
  flex: 1;
  min-width: 0;
}

.quick-nav-info strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.quick-nav-info p {
  margin: 0;
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.4;
}

.quick-nav-arrow {
  color: var(--text-muted);
  flex-shrink: 0;
  transition: all var(--transition-fast);
}

@media (max-width: 1080px) {
  .stat-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .stat-grid {
    grid-template-columns: 1fr;
  }
}

/* Dark mode */
:global([data-theme="dark"] .stat-card:hover ){
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

:global([data-theme="dark"] .quick-nav-card:hover ){
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>
