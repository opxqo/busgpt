<template>
  <div class="admin-page console-page container">
    <header class="console-header anim-fade-up">
      <div class="console-title-block">
        <span class="eyebrow">Admin Console</span>
        <h1 class="page-title">订单管理</h1>
        <span class="console-meta">table-orders</span>
      </div>
    </header>

    <nav class="segmented-tabs anim-fade-up anim-d1" aria-label="后台导航">
      <router-link to="/admin">概览</router-link>
      <router-link to="/admin/users">用户</router-link>
      <router-link to="/admin/rides">车位</router-link>
      <router-link to="/admin/orders">订单</router-link>
      <router-link to="/admin/analytics">分析</router-link>
      <router-link to="/admin/products">产品</router-link>
    </nav>

    <div class="toolbar surface-card anim-fade-up anim-d1">
      <div class="toolbar-fields">
        <input
          v-model.trim="search"
          class="form-control"
          type="text"
          placeholder="搜索订单号..."
          @keyup.enter="resetAndLoad"
        />
        <select v-model="statusFilter" class="form-control" @change="resetAndLoad">
          <option value="">全部状态</option>
          <option value="paid">已支付</option>
          <option value="pending">待支付</option>
          <option value="expired">已过期</option>
          <option value="cancelled">已取消</option>
          <option value="refunded">已退款</option>
        </select>
      </div>
      <button type="button" class="btn btn-secondary" :disabled="loading" @click="resetAndLoad">
        <Search :size="16" />
        搜索
      </button>
    </div>

    <div v-if="loading && orders.length === 0" class="loading-container surface-card anim-fade-up anim-d1">
      <div class="spinner"></div>
      <p>加载订单数据中</p>
    </div>

    <div v-else-if="orders.length === 0" class="empty-state surface-card anim-fade-up anim-d1">
      <ClipboardList :size="38" class="empty-icon" />
      <h3>暂无订单数据</h3>
      <p>没有找到匹配的订单，请调整搜索条件。</p>
    </div>

    <template v-else>
      <div class="summary-bar anim-fade-up anim-d2">
        <div class="summary-item">
          <span class="summary-label">总订单</span>
          <strong class="summary-value">{{ total }}</strong>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
          <span class="summary-label">当前页</span>
          <strong class="summary-value">{{ currentPage }}/{{ totalPages }}</strong>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
          <span class="summary-label">本页显示</span>
          <strong class="summary-value">{{ orders.length }} 条</strong>
        </div>
      </div>

      <div class="table-container surface-card anim-fade-up anim-d3">
        <table class="records-table">
          <thead>
            <tr>
              <th>订单号</th>
              <th>用户</th>
              <th>邮箱</th>
              <th>车位</th>
              <th>产品</th>
              <th class="text-right">金额</th>
              <th>状态</th>
              <th>支付时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(order, idx) in orders" :key="order.id" class="table-row-animate" :class="order.ride_product" :style="{ animationDelay: (idx * 0.03) + 's' }">
            <td class="mono-text">#{{ order.id }}</td>
            <td class="user-name">{{ order.user_nickname || '-' }}</td>
            <td class="mono-text">{{ order.user_email || '-' }}</td>
            <td>
              <router-link v-if="order.ride_id" :to="`/ride/${order.ride_id}`" class="record-title">
                {{ order.ride_title || '已失效车位' }}
              </router-link>
              <span v-else class="text-muted">已失效</span>
            </td>
            <td>
              <span class="product-chip" :class="order.ride_product">
                <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                  <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
                </svg>
                <span>{{ productLabel(order.ride_product) }}</span>
              </span>
            </td>
            <td class="text-right price-text">¥{{ Number(order.amount).toFixed(2) }}</td>
            <td>
              <span class="status-chip" :class="order.status">{{ statusLabel(order.status) }}</span>
            </td>
            <td class="date-col">{{ order.paid_at ? formatDate(order.paid_at) : '-' }}</td>
          </tr>
        </tbody>
      </table>

        <div class="pagination">
          <span class="pagination-info">共 {{ total }} 条，第 {{ currentPage }}/{{ totalPages }} 页</span>
          <div class="pagination-btns">
            <button type="button" class="btn btn-sm btn-secondary" :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">上一页</button>
            <button type="button" class="btn btn-sm btn-secondary" :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">下一页</button>
          </div>
        </div>
      </div>
    </template>

    <p v-if="message" class="feedback" role="status">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Search, ClipboardList } from '@lucide/vue'
import { adminApi } from '../../api/admin'
import type { AdminOrderListItem } from '../../types'

const PAGE_SIZE = 20

const loading = ref(false)
const orders = ref<AdminOrderListItem[]>([])
const total = ref(0)
const currentPage = ref(1)
const search = ref('')
const statusFilter = ref('')
const message = ref('')

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))

const productLabels: Record<string, string> = {
  'chatgpt-plus': 'Plus',
  'chatgpt-team': 'Business',
  'chatgpt-pro': 'Pro',
}

const productLabel = (product: string) => productLabels[product] || product || '-'

const statusLabels: Record<string, string> = {
  paid: '已支付',
  pending: '待支付',
  expired: '已过期',
  cancelled: '已取消',
  refunded: '已退款',
}

const statusLabel = (status: string) => statusLabels[status] || status

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

const loadOrders = async () => {
  loading.value = true
  message.value = ''
  try {
    const params: Record<string, string | number> = {
      skip: (currentPage.value - 1) * PAGE_SIZE,
      limit: PAGE_SIZE,
    }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    const res = await adminApi.getOrders(params)
    orders.value = res.data.items
    total.value = res.data.total
  } catch {
    message.value = '加载订单数据失败'
  } finally {
    loading.value = false
  }
}

const resetAndLoad = () => {
  currentPage.value = 1
  loadOrders()
}

const goToPage = (page: number) => {
  currentPage.value = page
  loadOrders()
}

onMounted(loadOrders)
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

.toolbar {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
}

.toolbar-fields {
  display: flex;
  flex: 1;
  gap: var(--spacing-sm);
}

.toolbar-fields .form-control {
  max-width: 220px;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.toolbar-fields .form-control:focus {
  border-color: var(--color-team);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.record-title {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: 600;
}

.record-title:hover {
  text-decoration: underline;
}

.user-name {
  font-weight: 600;
  color: var(--text-primary);
}

.mono-text {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 13px;
  letter-spacing: 0.02em;
}

.product-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 12px;
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: 700;
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

.status-chip {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: 700;
}

.status-chip.paid {
  background: var(--color-plus-soft);
  color: var(--color-plus);
}

.status-chip.pending {
  background: var(--color-warning-soft);
  color: var(--color-warning);
}

.status-chip.expired {
  background: var(--bg-inset);
  color: var(--text-muted);
}

.status-chip.cancelled {
  background: var(--bg-inset);
  color: var(--text-muted);
}

.status-chip.refunded {
  background: var(--color-info-soft);
  color: var(--color-info);
}

.price-text {
  font-weight: 700;
  color: var(--text-primary);
}

.date-col {
  color: var(--text-muted);
  white-space: nowrap;
}

.text-right {
  text-align: right;
}

.table-container :deep(.records-table tbody tr) {
  transition: background-color var(--transition-fast);
}

.table-container :deep(.records-table tbody tr:hover) {
  background: var(--bg-tertiary);
}

.table-container {
  transition: all var(--transition-fast);
}

.table-container:hover {
  border-color: var(--border-color-strong);
}

.text-muted {
  color: var(--text-muted);
  font-size: 13px;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-top: 1px solid var(--border-color);
  background: var(--bg-inset);
  border-radius: 0 0 var(--border-radius-lg) var(--border-radius-lg);
}

.pagination-info {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 600;
}

.pagination-btns {
  display: flex;
  gap: var(--spacing-sm);
}

.pagination-btns .btn-secondary:hover:not(:disabled) {
  border-color: var(--color-team);
  color: var(--color-team);
}

.btn-sm {
  min-height: 34px;
  padding: 0 14px;
  font-size: 13px;
}

/* Summary Bar */
.summary-bar {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: 10px var(--spacing-lg);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.summary-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
}

.summary-value {
  font-size: 13px;
  font-weight: 800;
  color: var(--text-primary);
}

.summary-divider {
  width: 1px;
  height: 16px;
  background: var(--border-color);
}

/* Staggered table row entrance */
.table-row-animate {
  opacity: 0;
  animation: rowFadeIn 0.3s ease-out forwards;
}

@keyframes rowFadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Product-colored row hover */
.table-container :deep(.records-table tbody tr.chatgpt-plus:hover) {
  border-left: 3px solid var(--color-plus);
}

.table-container :deep(.records-table tbody tr.chatgpt-team:hover) {
  border-left: 3px solid var(--color-team);
}

.table-container :deep(.records-table tbody tr.chatgpt-pro:hover) {
  border-left: 3px solid var(--color-pro);
}

.feedback {
  color: var(--color-success);
  font-size: 13px;
  font-weight: 700;
  padding: 10px 14px;
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: var(--border-radius-md);
  background: var(--color-success-soft);
  animation: fadeUp 0.3s ease-out;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xxl);
  text-align: center;
}

.empty-icon {
  color: var(--text-muted);
}

.empty-state h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 16px;
}

.empty-state p {
  color: var(--text-secondary);
  font-size: 14px;
}

@media (max-width: 768px) {
  .console-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .segmented-tabs {
    width: 100%;
    overflow-x: auto;
  }

  .segmented-tabs a {
    flex: 0 0 auto;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar-fields {
    flex-direction: column;
  }

  .toolbar-fields .form-control {
    max-width: 100%;
  }
}

/* Dark mode */
:global([data-theme="dark"] .toolbar-fields .form-control:focus ){
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.15);
}

:global([data-theme="dark"] .table-container:hover ){
  border-color: var(--border-color-strong);
}

:global([data-theme="dark"] .feedback ){
  background: rgba(52, 211, 153, 0.08);
  border-color: rgba(52, 211, 153, 0.15);
}

:global([data-theme="dark"] .pagination-btns .btn-secondary:hover:not(:disabled) ){
  border-color: rgba(96, 165, 250, 0.4);
  color: var(--color-team);
}

:global([data-theme="dark"] .summary-bar ){
  background: var(--bg-tertiary);
  border-color: var(--border-color-strong);
}

.admin-page {
  gap: var(--spacing-md);
}

.toolbar {
  padding: 10px 12px;
  border-radius: var(--border-radius-md);
}

.toolbar-fields .form-control {
  max-width: 220px;
}

.summary-bar {
  padding: 8px 12px;
  border-radius: var(--border-radius-md);
  background: var(--bg-secondary);
}

.table-container {
  border-radius: var(--border-radius-md);
}

.table-row-animate {
  opacity: 1;
  animation: none;
}

.pagination {
  padding: 10px 12px;
  border-radius: 0 0 var(--border-radius-md) var(--border-radius-md);
}

.table-container :deep(.records-table tbody tr.chatgpt-plus:hover),
.table-container :deep(.records-table tbody tr.chatgpt-team:hover),
.table-container :deep(.records-table tbody tr.chatgpt-pro:hover) {
  border-left: 0;
}

:global([data-theme="dark"] .table-container .records-table tbody tr.chatgpt-plus:hover){
  border-left-color: rgba(52, 211, 153, 0.5);
}

:global([data-theme="dark"] .table-container .records-table tbody tr.chatgpt-team:hover){
  border-left-color: rgba(96, 165, 250, 0.5);
}

:global([data-theme="dark"] .table-container .records-table tbody tr.chatgpt-pro:hover){
  border-left-color: rgba(167, 139, 250, 0.5);
}
</style>
