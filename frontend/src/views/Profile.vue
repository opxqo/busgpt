<template>
  <div class="profile-page container">
    <header class="profile-header surface-card">
      <div class="profile-main">
        <img :src="userStore.user?.avatar || defaultAvatar" alt="用户头像" class="avatar-large" />
        <div>
          <span class="eyebrow">账户中心</span>
          <h1>{{ userStore.user?.nickname }}</h1>
          <p>{{ userStore.user?.phone }} · 注册于 {{ formattedRegisterDate }}</p>
        </div>
      </div>
      <router-link to="/create" class="btn btn-primary">
        <PlusCircle :size="16" />
        发布车位
      </router-link>
    </header>

    <section class="stat-grid">
      <div class="stat-card surface-card">
        <span>我的解锁</span>
        <strong>{{ orders.length }}</strong>
      </div>
      <div class="stat-card surface-card">
        <span>我的发布</span>
        <strong>{{ ownedRides.length }}</strong>
      </div>
      <div class="stat-card surface-card">
        <span>信息服务收入</span>
        <strong>¥{{ formatMoney(sales?.total_revenue || 0) }}</strong>
      </div>
    </section>

    <section class="workspace surface-card">
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          type="button"
          class="tab-btn"
          :class="{ active: activeTab === tab.value }"
          @click="activeTab = tab.value"
        >
          <component :is="tab.icon" :size="16" />
          {{ tab.label }}
        </button>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>加载账户信息中</p>
      </div>

      <div v-else class="tab-content">
        <div v-if="activeTab === 'orders'" class="table-wrap">
          <div v-if="orders.length === 0" class="empty-state">
            <ReceiptText :size="34" />
            <h3>暂无解锁记录</h3>
            <p>在详情页支付信息服务费后，联系方式会记录在这里。</p>
            <router-link to="/market" class="btn btn-primary">发现车位</router-link>
          </div>
          <table v-else class="records-table">
            <thead>
              <tr>
                <th>车位</th>
                <th>产品</th>
                <th>拼车进度</th>
                <th>服务费</th>
                <th>解锁时间</th>
                <th>联系方式</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td>
                  <router-link :to="`/ride/${order.ride_id}`" class="record-title">{{ order.ride_title || '已删除车位' }}</router-link>
                  <small>订单号 #{{ order.id }}</small>
                </td>
                <td>{{ productLabel(order.ride_product) }}</td>
                <td>
                  <div class="seat-metric">
                    <strong>{{ order.ride_purchase_count || 0 }}/{{ order.ride_total_seats || 0 }}</strong>
                    <span>还差 {{ order.ride_remaining_seats || 0 }} 人</span>
                  </div>
                </td>
                <td>¥{{ formatMoney(order.amount) }}</td>
                <td>{{ formatDate(order.created_at) }}</td>
                <td>
                  <button class="copy-btn" type="button" @click="copyText(order.ride_contact_info || '')">
                    <Copy :size="14" />
                    复制
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="activeTab === 'published'" class="published-section">
          <div v-if="ownedRides.length === 0" class="empty-state">
            <PackageOpen :size="34" />
            <h3>还没有发布车位</h3>
            <p>发布后可以在这里查看状态和解锁次数。</p>
            <router-link to="/create" class="btn btn-primary">发布车位</router-link>
          </div>
          <div v-else class="rides-grid">
            <RideCard v-for="ride in ownedRides" :key="ride.id" :ride="ride" />
          </div>
        </div>

        <div v-if="activeTab === 'sales'" class="sales-section">
          <div class="sales-summary">
            <div>
              <span>总订单</span>
              <strong>{{ sales?.total_orders || 0 }}</strong>
            </div>
            <div>
              <span>总收入</span>
              <strong>¥{{ formatMoney(sales?.total_revenue || 0) }}</strong>
            </div>
          </div>
          <table class="records-table">
            <thead>
              <tr>
                <th>发布车位</th>
                <th>解锁次数</th>
                <th>拼车人数</th>
                <th>服务费收入</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in sales?.rides || []" :key="item.ride_id">
                <td>
                  <router-link :to="`/ride/${item.ride_id}`" class="record-title">{{ item.ride_title }}</router-link>
                </td>
                <td>{{ item.order_count }}</td>
                <td>{{ item.order_count }}/{{ item.total_seats }} · 还差 {{ item.remaining_seats }} 人</td>
                <td>¥{{ formatMoney(item.revenue) }}</td>
              </tr>
              <tr v-if="!sales?.rides?.length">
                <td colspan="4" class="empty-cell">暂无销售记录</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="activeTab === 'settings'" class="settings-section">
          <form class="settings-form" @submit.prevent="handleSave">
            <div class="form-group">
              <label class="form-label" for="nickname">昵称</label>
              <input id="nickname" v-model.trim="editForm.nickname" class="form-control" type="text" required />
            </div>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <Save :size="16" />
              {{ saving ? '保存中...' : '保存资料' }}
            </button>
            <p v-if="saveMessage" class="save-message">{{ saveMessage }}</p>
          </form>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, markRaw, onMounted, reactive, ref } from 'vue'
import { Copy, FileChartColumn, PackageOpen, PlusCircle, ReceiptText, Save, Settings } from '@lucide/vue'
import { useUserStore } from '../stores/user'
import { ridesApi } from '../api/rides'
import { ordersApi } from '../api/orders'
import RideCard from '../components/ride/RideCard.vue'
import type { Order, Ride } from '../types'

interface SalesRide {
  ride_id: number
  ride_title: string
  order_count: number
  revenue: number
  total_seats: number
  remaining_seats: number
  status: string
}

interface SalesSummary {
  total_revenue: number
  total_orders: number
  rides: SalesRide[]
}

const userStore = useUserStore()
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt'
const loading = ref(true)
const saving = ref(false)
const saveMessage = ref('')
const activeTab = ref<'orders' | 'published' | 'sales' | 'settings'>('orders')
const orders = ref<Order[]>([])
const ownedRides = ref<Ride[]>([])
const sales = ref<SalesSummary | null>(null)

const tabs = [
  { value: 'orders' as const, label: '我的解锁', icon: markRaw(ReceiptText) },
  { value: 'published' as const, label: '我的发布', icon: markRaw(PackageOpen) },
  { value: 'sales' as const, label: '销售统计', icon: markRaw(FileChartColumn) },
  { value: 'settings' as const, label: '资料设置', icon: markRaw(Settings) },
]

const editForm = reactive({
  nickname: '',
})

const formattedRegisterDate = computed(() => {
  if (!userStore.user?.created_at) return ''
  return formatDate(userStore.user.created_at)
})

const loadProfileData = async () => {
  loading.value = true
  try {
    const [ordersRes, ownedRes, salesRes] = await Promise.all([
      ordersApi.getMyOrders(),
      ridesApi.getMyOwnedRides(),
      ordersApi.getMySales(),
    ])
    orders.value = ordersRes.data
    ownedRides.value = ownedRes.data
    sales.value = salesRes.data
    editForm.nickname = userStore.user?.nickname || ''
  } catch (err) {
    console.error('Failed to load profile data', err)
  } finally {
    loading.value = false
  }
}

onMounted(loadProfileData)

const handleSave = async () => {
  if (!editForm.nickname) return
  saving.value = true
  saveMessage.value = ''
  try {
    await userStore.updateProfile(editForm.nickname)
    saveMessage.value = '资料已保存'
  } catch (err) {
    saveMessage.value = '保存失败，请稍后重试'
  } finally {
    saving.value = false
  }
}

const copyText = async (text: string) => {
  if (!text) return
  await navigator.clipboard.writeText(text)
}

const productLabel = (product?: string) => {
  if (product === 'chatgpt-team') return 'Team'
  if (product === 'chatgpt-pro') return 'Pro'
  if (product === 'chatgpt-plus') return 'Plus'
  return '-'
}

const formatDate = (dateText: string) => {
  const date = new Date(dateText)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const formatMoney = (value: number | string) => Math.round(Number(value || 0))
</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
}

.profile-main {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.avatar-large {
  width: 64px;
  height: 64px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
}

.profile-main h1 {
  margin: 4px 0;
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 900;
}

.profile-main p {
  color: var(--text-secondary);
  font-size: 13px;
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.stat-card {
  padding: var(--spacing-md);
}

.stat-card span,
.sales-summary span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 800;
}

.stat-card strong,
.sales-summary strong {
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 900;
}

.workspace {
  overflow: hidden;
}

.tabs {
  display: flex;
  gap: 4px;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-inset);
}

.tab-btn {
  display: inline-flex;
  min-height: 38px;
  align-items: center;
  gap: 7px;
  padding: 0 13px;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 900;
}

.tab-btn.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  box-shadow: 0 1px 2px rgba(25, 31, 36, 0.08);
}

.tab-content {
  padding: var(--spacing-lg);
}

.table-wrap {
  overflow-x: auto;
}

.records-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 720px;
}

.records-table th,
.records-table td {
  padding: 14px 12px;
  border-bottom: 1px solid var(--border-color);
  text-align: left;
  vertical-align: middle;
}

.records-table th {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 900;
}

.records-table td {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 700;
}

.record-title {
  display: block;
  margin-bottom: 4px;
  color: var(--text-primary);
  font-weight: 900;
}

.records-table small {
  color: var(--text-muted);
  font-size: 12px;
}

.seat-metric {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.seat-metric strong {
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 900;
}

.seat-metric span {
  color: var(--text-muted);
  font-size: 12px;
}

.copy-btn {
  display: inline-flex;
  min-height: 32px;
  align-items: center;
  gap: 5px;
  padding: 0 10px;
  border-radius: var(--border-radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  font-size: 12px;
  font-weight: 900;
}

.rides-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.sales-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.sales-summary div {
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.empty-cell {
  color: var(--text-muted);
  text-align: center;
}

.settings-form {
  max-width: 420px;
}

.save-message {
  margin-top: var(--spacing-sm);
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 900;
}

@media (max-width: 960px) {
  .rides-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .profile-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .stat-grid,
  .sales-summary,
  .rides-grid {
    grid-template-columns: 1fr;
  }

  .tabs {
    overflow-x: auto;
  }
}
</style>
