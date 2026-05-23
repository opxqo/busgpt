<template>
  <div class="profile-page container">
    <!-- Profile Header Banner -->
    <header class="profile-header surface-card">
      <div class="profile-main">
        <div class="avatar-wrap">
          <img :src="userStore.user?.avatar || defaultAvatar" alt="用户头像" class="avatar-large" />
          <span class="online-dot"></span>
        </div>
        <div class="user-meta">
          <span class="eyebrow">账户控制中心</span>
          <h1 class="user-name">{{ userStore.user?.nickname }}</h1>
          <p class="user-sub">{{ userStore.user?.phone }} · 加入于 {{ formattedRegisterDate }}</p>
        </div>
      </div>
      <router-link to="/create" class="btn btn-primary publish-shortcut-btn">
        <PlusCircle :size="16" />
        <span>发布新车位</span>
      </router-link>
    </header>

    <!-- Stats grid -->
    <section class="stat-grid">
      <div class="stat-card surface-card">
        <span class="stat-label">我解锁的联系方式</span>
        <strong class="stat-value">{{ orders.length }} <small>个</small></strong>
      </div>
      <div class="stat-card surface-card">
        <span class="stat-label">我发布的拼车车位</span>
        <strong class="stat-value">{{ ownedRides.length }} <small>个</small></strong>
      </div>
      <div class="stat-card surface-card">
        <span class="stat-label">信息解锁累计收益</span>
        <strong class="stat-value text-purple">¥{{ formatMoney(sales?.total_revenue || 0) }}</strong>
      </div>
    </section>

    <!-- Workspace -->
    <section class="workspace surface-card">
      <div class="workspace-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          type="button"
          class="tab-btn"
          :class="{ active: activeTab === tab.value }"
          @click="activeTab = tab.value"
        >
          <component :is="tab.icon" :size="15" />
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>正在获取您的账户数据...</p>
      </div>

      <div v-else class="tab-content">
        <!-- Tab 1: Unlocked Contacts (My Orders) -->
        <div v-if="activeTab === 'orders'" class="table-wrap">
          <div v-if="orders.length === 0" class="empty-state">
            <ReceiptText :size="38" class="empty-icon" />
            <h3>暂无解锁记录</h3>
            <p>在车位详情页成功支付服务费后，解锁的车主联络方式会记录在这里。</p>
            <router-link to="/market" class="btn btn-primary">去市场挑选车位</router-link>
          </div>
          <table v-else class="records-table">
            <thead>
              <tr>
                <th>共享车位</th>
                <th>产品类型</th>
                <th>拼车进度</th>
                <th>解锁服务费</th>
                <th>解锁时间</th>
                <th class="text-right">车主联系方式</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td>
                  <router-link :to="`/ride/${order.ride_id}`" class="record-title">{{ order.ride_title || '已失效车位' }}</router-link>
                  <small class="order-id">订单号 #{{ order.id }}</small>
                </td>
                <td>
                  <span class="product-chip" :class="order.ride_product">{{ productLabel(order.ride_product) }}</span>
                </td>
                <td>
                  <div class="seat-metric">
                    <strong>已拼 {{ order.ride_purchase_count || 0 }}/{{ order.ride_total_seats || 0 }} 人</strong>
                    <span>空余 {{ order.ride_remaining_seats || 0 }} 个名额</span>
                  </div>
                </td>
                <td>¥{{ formatMoney(order.amount) }}</td>
                <td class="date-col">{{ formatDate(order.created_at) }}</td>
                <td class="text-right">
                  <button class="btn-copy" type="button" @click="copyText(order.ride_contact_info || '', order.id)">
                    <Copy :size="13" />
                    <span>{{ copyStates[order.id] ? '已复制' : '复制资料' }}</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tab 2: Hosted Rides -->
        <div v-if="activeTab === 'published'" class="published-section">
          <div v-if="ownedRides.length === 0" class="empty-state">
            <PackageOpen :size="38" class="empty-icon" />
            <h3>还没有发布过车位</h3>
            <p>您可以将您多余的 ChatGPT 订阅位发布在此，让他人分摊月费。</p>
            <router-link to="/create" class="btn btn-primary">发布共享车位</router-link>
          </div>
          <div v-else class="rides-grid">
            <RideCard v-for="ride in ownedRides" :key="ride.id" :ride="ride" />
          </div>
        </div>

        <!-- Tab 3: Sales Stats -->
        <div v-if="activeTab === 'sales'" class="sales-section">
          <div class="sales-summary-cards">
            <div class="summary-card">
              <span>车主服务订单总数</span>
              <strong>{{ sales?.total_orders || 0 }} 笔</strong>
            </div>
            <div class="summary-card">
              <span>解锁总收益</span>
              <strong class="text-purple">¥{{ formatMoney(sales?.total_revenue || 0) }}</strong>
            </div>
          </div>
          <div class="table-wrap">
            <table class="records-table">
              <thead>
                <tr>
                  <th>发布的车位标题</th>
                  <th>车友解锁次数</th>
                  <th>车位当前载员</th>
                  <th>信息费累计收益</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in sales?.rides || []" :key="item.ride_id">
                  <td>
                    <router-link :to="`/ride/${item.ride_id}`" class="record-title">{{ item.ride_title }}</router-link>
                  </td>
                  <td>{{ item.order_count }} 次被解锁</td>
                  <td>
                    <div class="seat-metric">
                      <strong>{{ item.order_count }}/{{ item.total_seats }} 人</strong>
                      <span>空位 {{ item.remaining_seats }} 个</span>
                    </div>
                  </td>
                  <td>¥{{ formatMoney(item.revenue) }}</td>
                </tr>
                <tr v-if="!sales?.rides?.length">
                  <td colspan="4" class="empty-cell">暂无车友解锁您的车位</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Tab 4: Settings -->
        <div v-if="activeTab === 'settings'" class="settings-section">
          <form class="settings-form" @submit.prevent="handleSave">
            <div class="form-group">
              <label class="form-label" for="nickname">设置新的昵称</label>
              <input id="nickname" v-model.trim="editForm.nickname" class="form-control" type="text" required />
            </div>
            <button type="submit" class="btn btn-primary submit-btn-save" :disabled="saving">
              <Save :size="16" />
              <span>{{ saving ? '正在保存修改...' : '更新账户信息' }}</span>
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
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt&backgroundColor=0f172a'
const loading = ref(true)
const saving = ref(false)
const saveMessage = ref('')
const activeTab = ref<'orders' | 'published' | 'sales' | 'settings'>('orders')
const orders = ref<Order[]>([])
const ownedRides = ref<Ride[]>([])
const sales = ref<SalesSummary | null>(null)
const copyStates = ref<Record<string, boolean>>({})

const tabs = [
  { value: 'orders' as const, label: '我的解锁', icon: markRaw(ReceiptText) },
  { value: 'published' as const, label: '我的发布', icon: markRaw(PackageOpen) },
  { value: 'sales' as const, label: '销售统计', icon: markRaw(FileChartColumn) },
  { value: 'settings' as const, label: '账户设置', icon: markRaw(Settings) },
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
    saveMessage.value = '基本信息已成功更新'
  } catch {
    saveMessage.value = '更新失败，请稍后重试'
  } finally {
    saving.value = false
  }
}

const copyText = async (text: string, id: number) => {
  if (!text) return
  await navigator.clipboard.writeText(text)
  copyStates.value[id] = true
  setTimeout(() => {
    copyStates.value[id] = false
  }, 1800)
}

const productLabel = (product?: string) => {
  if (product === 'chatgpt-team') return 'Team 协作'
  if (product === 'chatgpt-pro') return 'Pro 极客'
  if (product === 'chatgpt-plus') return 'Plus 拼车'
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
  gap: var(--spacing-md);
  padding: var(--spacing-lg) var(--spacing-xl);
  background: linear-gradient(135deg, #ffffff 0%, var(--bg-tertiary) 100%);
  border-color: var(--border-color-strong);
}

.profile-main {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.avatar-wrap {
  position: relative;
}

.avatar-large {
  width: 60px;
  height: 60px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
  border: 2px solid #ffffff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.online-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  background: var(--color-success);
  border: 2px solid #ffffff;
  border-radius: var(--border-radius-full);
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  margin: var(--spacing-xs) 0;
  letter-spacing: -0.02em;
}

.user-sub {
  color: var(--text-secondary);
  font-size: 13px;
  margin: 0;
}

/* Stats dashboard */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.stat-card {
  padding: var(--spacing-md) var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
}

.stat-value {
  color: var(--text-primary);
  font-size: 26px;
  font-weight: 800;
  line-height: 1.2;
}

.stat-value small {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.text-purple {
  color: var(--color-pro);
}

/* Workspace tab content */
.workspace {
  border-color: var(--border-color-strong);
  overflow: hidden;
}

.workspace-tabs {
  display: flex;
  gap: 4px;
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-inset);
}

.tab-btn {
  display: inline-flex;
  min-height: 38px;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  border-radius: var(--border-radius-md);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tab-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.tab-btn.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.tab-content {
  padding: var(--spacing-xl);
}

.table-wrap {
  overflow-x: auto;
}

.records-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.records-table th {
  padding: 12px;
  border-bottom: 2px solid var(--border-color);
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-align: left;
}

.records-table td {
  padding: 14px 12px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  vertical-align: middle;
}

.record-title {
  display: block;
  font-size: 14px;
  font-weight: 800;
  color: var(--text-primary);
  text-decoration: none;
  margin-bottom: 2px;
}

.record-title:hover {
  text-decoration: underline;
}

.order-id {
  color: var(--text-muted);
  font-size: 11px;
}

.seat-metric {
  display: flex;
  flex-direction: column;
}

.seat-metric strong {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.seat-metric span {
  font-size: 11px;
  color: var(--text-muted);
}

.date-col {
  color: var(--text-muted);
  font-size: 12px;
}

.btn-copy {
  display: inline-flex;
  height: 30px;
  align-items: center;
  gap: 4px;
  padding: 0 10px;
  border-radius: var(--border-radius-sm);
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-copy:hover {
  background: var(--text-primary);
  color: var(--text-inverse);
  border-color: var(--text-primary);
}

/* Sales breakdown */
.sales-summary-cards {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.summary-card span {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 600;
}

.summary-card strong {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
}

.empty-cell {
  text-align: center;
  color: var(--text-muted);
  padding: var(--spacing-lg) 0;
}

/* Settings Form */
.settings-form {
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.submit-btn-save {
  align-self: flex-start;
  min-width: 140px;
}

.save-message {
  font-size: 13px;
  color: var(--color-success);
  font-weight: 700;
  margin: 0;
}

.rides-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.empty-icon {
  color: var(--text-muted);
}

@media (max-width: 1080px) {
  .rides-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
  .publish-shortcut-btn {
    width: 100%;
  }
  .stat-grid,
  .sales-summary-cards {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }
  .workspace-tabs {
    overflow-x: auto;
  }
  .rides-grid {
    grid-template-columns: 1fr;
  }
}
</style>
