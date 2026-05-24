<template>
  <div class="admin-page console-page container">
    <header class="console-header anim-fade-up">
      <div class="console-title-block">
        <span class="eyebrow">Admin Console</span>
        <h1 class="page-title">用户管理</h1>
        <span class="console-meta">table-users</span>
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
          placeholder="搜索邮箱或昵称..."
          @keyup.enter="resetAndLoad"
        />
        <select v-model="roleFilter" class="form-control" @change="resetAndLoad">
          <option value="">全部角色</option>
          <option value="user">普通用户</option>
          <option value="admin">管理员</option>
        </select>
      </div>
      <button type="button" class="btn btn-secondary" :disabled="loading" @click="resetAndLoad">
        <Search :size="16" />
        搜索
      </button>
    </div>

    <div v-if="loading && users.length === 0" class="loading-container surface-card anim-fade-up anim-d1">
      <div class="spinner"></div>
      <p>加载用户数据中</p>
    </div>

    <div v-else-if="users.length === 0" class="empty-state surface-card anim-fade-up anim-d1">
      <Users :size="38" class="empty-icon" />
      <h3>暂无用户数据</h3>
      <p>没有找到匹配的用户，请调整搜索条件。</p>
    </div>

    <template v-else>
      <div class="summary-bar anim-fade-up anim-d2">
        <div class="summary-item">
          <span class="summary-label">总用户</span>
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
          <strong class="summary-value">{{ users.length }} 条</strong>
        </div>
      </div>

      <div class="table-container surface-card anim-fade-up anim-d3">
      <table class="records-table">
        <thead>
          <tr>
            <th>用户</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>状态</th>
            <th>注册时间</th>
            <th>车位数</th>
            <th>订单数</th>
            <th class="text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, idx) in users" :key="user.id" class="table-row-animate" :class="{ 'admin-row': user.role === 'admin' }" :style="{ animationDelay: (idx * 0.03) + 's' }">
            <td>
              <div class="user-cell">
                <img :src="user.avatar || defaultAvatar" alt="" class="user-avatar" />
                <span class="user-name">{{ user.nickname }}</span>
              </div>
            </td>
            <td class="mono-text">{{ user.email }}</td>
            <td>
              <span class="role-chip" :class="user.role">{{ user.role === 'admin' ? '管理员' : '用户' }}</span>
            </td>
            <td>
              <span class="status-tag" :class="{ active: user.is_active, disabled: !user.is_active }">
                {{ user.is_active ? '正常' : '已禁用' }}
              </span>
            </td>
            <td class="date-col">{{ formatDate(user.created_at) }}</td>
            <td>{{ user.ride_count }}</td>
            <td>{{ user.order_count }}</td>
            <td class="text-right">
              <button
                v-if="user.role !== 'admin'"
                type="button"
                class="btn btn-sm"
                :class="user.is_active ? 'btn-danger' : 'btn-secondary'"
                @click="toggleUserStatus(user)"
              >
                {{ user.is_active ? '禁用' : '启用' }}
              </button>
              <span v-else class="text-muted">—</span>
            </td>
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
import { Search, Users } from '@lucide/vue'
import { adminApi } from '../../api/admin'
import type { AdminUserListItem } from '../../types'

const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt&backgroundColor=0f172a'
const PAGE_SIZE = 20

const loading = ref(false)
const users = ref<AdminUserListItem[]>([])
const total = ref(0)
const currentPage = ref(1)
const search = ref('')
const roleFilter = ref('')
const message = ref('')

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / PAGE_SIZE)))

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const loadUsers = async () => {
  loading.value = true
  message.value = ''
  try {
    const params: Record<string, string | number> = {
      skip: (currentPage.value - 1) * PAGE_SIZE,
      limit: PAGE_SIZE,
    }
    if (search.value) params.search = search.value
    if (roleFilter.value) params.role = roleFilter.value
    const res = await adminApi.getUsers(params)
    users.value = res.data.items
    total.value = res.data.total
  } catch {
    message.value = '加载用户数据失败'
  } finally {
    loading.value = false
  }
}

const resetAndLoad = () => {
  currentPage.value = 1
  loadUsers()
}

const goToPage = (page: number) => {
  currentPage.value = page
  loadUsers()
}

const toggleUserStatus = async (user: AdminUserListItem) => {
  const action = user.is_active ? '禁用' : '启用'
  if (!confirm(`确定要${action}用户「${user.nickname}」吗？`)) return

  try {
    await adminApi.updateUserStatus(user.id, !user.is_active)
    user.is_active = !user.is_active
    message.value = `已${action}用户「${user.nickname}」`
  } catch {
    message.value = `${action}失败，请重试`
  }
}

onMounted(loadUsers)
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
  max-width: 260px;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.toolbar-fields .form-control:focus {
  border-color: var(--color-pro);
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-full);
  border: 1px solid var(--border-color);
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

.role-chip {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: 700;
}

.role-chip.user {
  background: var(--bg-inset);
  color: var(--text-secondary);
}

.role-chip.admin {
  background: var(--color-pro-soft);
  color: var(--color-pro);
}

.status-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--border-radius-full);
  font-size: 12px;
  font-weight: 700;
}

.status-tag.active {
  background: var(--color-plus-soft);
  color: var(--color-plus);
}

.status-tag.disabled {
  background: var(--color-danger-soft);
  color: var(--color-danger);
}

.date-col {
  color: var(--text-muted);
  white-space: nowrap;
}

.text-right {
  text-align: right;
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
  border-color: var(--color-pro);
  color: var(--color-pro);
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

/* Admin row accent */
.admin-row {
  border-left: 3px solid var(--color-pro);
}

.admin-row td:first-child {
  padding-left: 13px;
}

.btn-danger {
  color: var(--color-danger);
  background: var(--color-danger-soft);
  border: 1px solid transparent;
  cursor: pointer;
  border-radius: var(--border-radius-md);
  font-weight: 600;
  transition: all var(--transition-fast);
}

.btn-danger:hover {
  background: var(--color-danger-hover);
  border-color: var(--color-danger-border-hover);
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

.table-container {
  transition: all var(--transition-fast);
}

.table-container:hover {
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

.btn-danger,
.btn-secondary {
  box-shadow: none;
}

/* Dark mode */
:global([data-theme="dark"] .toolbar-fields .form-control:focus ){
  box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
}

:global([data-theme="dark"] .table-container:hover ){
  border-color: var(--border-color-strong);
}

:global([data-theme="dark"] .feedback ){
  background: rgba(52, 211, 153, 0.08);
  border-color: rgba(52, 211, 153, 0.15);
}

:global([data-theme="dark"] .user-avatar ){
  border-color: var(--border-color-strong);
}

:global([data-theme="dark"] .pagination-btns .btn-secondary:hover:not(:disabled) ){
  border-color: rgba(167, 139, 250, 0.4);
  color: var(--color-pro);
}

:global([data-theme="dark"] .summary-bar ){
  background: var(--bg-tertiary);
  border-color: var(--border-color-strong);
}

:global([data-theme="dark"] .admin-row ){
  border-left-color: rgba(167, 139, 250, 0.5);
}
</style>
