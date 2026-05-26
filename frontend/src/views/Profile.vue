<template>
  <div class="profile-page container">
    <!-- Profile Header Banner -->
    <header class="profile-header surface-card anim-fade-up">
      <div class="profile-main">
        <div class="avatar-wrap">
          <img :src="userStore.user?.avatar || defaultAvatar" alt="用户头像" class="avatar-large" />
          <span class="online-dot"></span>
        </div>
        <div class="user-meta">
          <span class="eyebrow">账户控制中心</span>
          <h1 class="user-name">{{ userStore.user?.nickname }}</h1>
          <p class="user-sub">{{ userStore.user?.email }} · 加入于 {{ formattedRegisterDate }}</p>
        </div>
      </div>
      <router-link to="/create" class="btn btn-primary publish-shortcut-btn submit-shimmer">
        <PlusCircle :size="16" />
        <span>发布新车位</span>
      </router-link>
    </header>

    <!-- Stats grid -->
    <section class="stat-grid anim-fade-up anim-d1">
      <div class="stat-card surface-card">
        <span class="stat-label">我解锁查看的联系方式</span>
        <strong class="stat-value">{{ unlockedOrders.length }} <small>次</small></strong>
      </div>
      <div class="stat-card surface-card">
        <span class="stat-label">我发布的拼车车位</span>
        <strong class="stat-value">{{ ownedRides.length }} <small>个</small></strong>
      </div>
      <div class="stat-card surface-card">
        <span class="stat-label">招募被解锁查看</span>
        <strong class="stat-value">{{ sales?.total_unlocks || 0 }} <small>次</small></strong>
      </div>
    </section>

    <!-- Workspace -->
    <section class="workspace surface-card anim-fade-up anim-d2">
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

      <div v-if="loading" class="skeleton-workspace">
        <div class="skel-row" v-for="i in 4" :key="i">
          <div class="skel skel-cell skel-w20"></div>
          <div class="skel skel-cell skel-w15"></div>
          <div class="skel skel-cell skel-w25"></div>
          <div class="skel skel-cell skel-w15"></div>
          <div class="skel skel-cell skel-w10"></div>
        </div>
      </div>

      <div v-else class="tab-content">
        <!-- Tab 1: Unlocked Contacts (My Orders) -->
        <div v-if="activeTab === 'orders'" class="table-wrap">
          <div v-if="orders.length === 0" class="empty-state">
            <ReceiptText :size="38" class="empty-icon" />
            <h3>暂无拼车记录</h3>
            <p>在市场中挑选心仪的车位，查看车主联系方式后即可开始拼车。</p>
            <router-link to="/market" class="btn btn-primary">去市场挑选车位</router-link>
          </div>
          <table v-else class="records-table">
            <thead>
              <tr>
                <th>共享车位</th>
                <th>产品类型</th>
                <th>拼车进度</th>
                <th>加入时间</th>
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
                  <span class="product-chip" :class="order.ride_product">
                    <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                      <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
                    </svg>
                    <span>{{ productLabel(order.ride_product) }}</span>
                  </span>
                </td>
                <td>
                  <div class="seat-metric">
                    <strong>进度 {{ orderOccupiedSeats(order) }}/{{ order.ride_total_seats || 0 }} 人</strong>
                    <span>空余 {{ order.ride_remaining_seats || 0 }} 个名额</span>
                  </div>
                </td>
                <td class="date-col">{{ formatDate(order.created_at) }}</td>
                <td class="text-right">
                  <button class="btn-copy" type="button" @click="copyText(orderContactText(order), order.id)">
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
          <div v-else class="published-manager">
            <div class="published-toolbar">
              <div>
                <h2>已发布招募</h2>
                <p>管理展示信息、车位状态和隐藏联系方式。</p>
              </div>
              <router-link to="/create" class="btn btn-primary publish-toolbar-btn">
                <PlusCircle :size="15" />
                <span>新增招募</span>
              </router-link>
            </div>

            <div class="published-list">
              <article v-for="ride in ownedRides" :key="ride.id" class="manage-card" :class="ride.product">
                <div class="manage-card-main">
                  <div class="manage-title-row">
                    <span class="product-chip" :class="ride.product">
                      <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                        <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
                      </svg>
                      <span>{{ productLabel(ride.product) }}</span>
                    </span>
                    <span class="status-chip" :class="ride.status">{{ statusLabel(ride.status) }}</span>
                  </div>
                  <router-link :to="`/ride/${ride.id}`" class="manage-title">{{ ride.title }}</router-link>
                  <p class="manage-desc">{{ ride.description || '暂未填写公开说明。' }}</p>
                  <div class="manage-metrics">
                    <div>
                      <span>车位租金</span>
                      <strong>¥{{ formatMoney(ride.price_per_month) }}/月</strong>
                    </div>
                    <div>
                      <span>质保</span>
                      <strong>{{ ride.warranty_days }}天</strong>
                    </div>
                    <div>
                      <span>拼车进度</span>
                      <strong>{{ rideOccupiedSeats(ride) }}/{{ ride.total_seats }} 人</strong>
                    </div>
                    <div>
                      <span>到期日</span>
                      <strong>{{ formatDate(ride.expires_at) }}</strong>
                    </div>
                  </div>
                </div>
                <div class="manage-actions">
                  <router-link :to="`/ride/${ride.id}`" class="icon-action" aria-label="查看招募">
                    <Eye :size="15" />
                    <span>查看</span>
                  </router-link>
                  <button class="icon-action" type="button" @click="openEditRide(ride)">
                    <Pencil :size="15" />
                    <span>编辑</span>
                  </button>
                  <button class="icon-action" type="button" :disabled="actionLoadingId === ride.id" @click="toggleRideStatus(ride)">
                    <Power :size="15" />
                    <span>{{ ride.status === 'open' ? '暂停' : '恢复' }}</span>
                  </button>
                  <button class="icon-action danger" type="button" :disabled="actionLoadingId === ride.id || (ride.purchase_count || 0) > 0" @click="deleteRide(ride)">
                    <Trash2 :size="15" />
                    <span>删除</span>
                  </button>
                </div>
              </article>
            </div>
            <p class="manager-note">已有联系方式解锁记录的招募不可直接删除，可以先暂停招募，保留订单与联系方式记录。</p>
          </div>
        </div>

        <!-- Tab 3: Sales Stats -->
        <div v-if="activeTab === 'sales'" class="sales-section">
          <div class="sales-summary-cards">
            <div class="summary-card">
              <span>联系方式解锁总数</span>
              <strong>{{ sales?.total_unlocks || 0 }} 次</strong>
            </div>
            <div class="summary-card">
              <span>当前上车总人数</span>
              <strong>{{ sales?.rides?.reduce((sum, r) => sum + r.recruit_seats, 0) || 0 }} 人</strong>
            </div>
          </div>
          <div class="table-wrap">
            <table class="records-table">
              <thead>
                <tr>
                  <th>发布的车位标题</th>
                  <th>解锁查看人数</th>
                  <th>车位当前载员</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in sales?.rides || []" :key="item.ride_id">
                  <td>
                    <router-link :to="`/ride/${item.ride_id}`" class="record-title">{{ item.ride_title }}</router-link>
                  </td>
                  <td>{{ item.unlock_count || item.order_count }} 人已解锁</td>
                  <td>
                    <div class="seat-metric">
                      <strong>{{ item.recruit_seats }}/{{ item.total_seats }} 人</strong>
                      <span>空位 {{ item.remaining_seats }} 个</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="!sales?.rides?.length">
                  <td colspan="3" class="empty-cell">暂无联系方式解锁记录</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Tab 4: Settings -->
        <div v-if="activeTab === 'settings'" class="settings-section">
          <div class="settings-grid">
            <form class="settings-form settings-panel" @submit.prevent="handleSave">
              <div class="settings-panel-heading">
                <h3>基本信息</h3>
                <p>更新账户公开展示昵称和头像。</p>
              </div>
              <div class="avatar-setting">
                <img :src="avatarPreviewUrl" alt="头像预览" class="avatar-preview" @error="handleAvatarError" />
                <div>
                  <strong>头像预览</strong>
                  <span>支持 HTTPS 图片链接，留空则使用默认头像。</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label" for="nickname">设置新的昵称</label>
                <input id="nickname" v-model.trim="editForm.nickname" class="form-control" type="text" required />
              </div>
              <div class="form-group">
                <label class="form-label" for="avatar">头像图片链接</label>
                <input id="avatar" v-model.trim="editForm.avatar" class="form-control" type="url" placeholder="https://example.com/avatar.png" />
              </div>
              <button type="submit" class="btn btn-primary submit-btn-save" :disabled="saving">
                <Save :size="16" />
                <span>{{ saving ? '正在保存修改...' : '更新账户信息' }}</span>
              </button>
              <p v-if="saveMessage" class="save-message">{{ saveMessage }}</p>
            </form>

            <form class="settings-form settings-panel" @submit.prevent="handlePasswordChange">
              <div class="settings-panel-heading">
                <h3>登录密码</h3>
                <p>修改后请使用新密码重新登录。</p>
              </div>
              <div class="form-group">
                <label class="form-label" for="current-password">当前密码</label>
                <input id="current-password" v-model="passwordForm.current_password" class="form-control" type="password" autocomplete="current-password" required minlength="6" />
              </div>
              <div class="form-group">
                <label class="form-label" for="new-password">新密码</label>
                <input id="new-password" v-model="passwordForm.new_password" class="form-control" type="password" autocomplete="new-password" required minlength="6" maxlength="30" />
              </div>
              <div class="form-group">
                <label class="form-label" for="confirm-password">确认新密码</label>
                <input id="confirm-password" v-model="passwordForm.confirm_password" class="form-control" type="password" autocomplete="new-password" required minlength="6" maxlength="30" />
              </div>
              <button type="submit" class="btn btn-primary submit-btn-save" :disabled="savingPassword">
                <KeyRound :size="16" />
                <span>{{ savingPassword ? '正在更新密码...' : '更新登录密码' }}</span>
              </button>
              <p v-if="passwordMessage" class="save-message" :class="{ error: passwordError }">{{ passwordMessage }}</p>
            </form>
          </div>
        </div>
      </div>
    </section>

    <Transition name="modal">
      <div v-if="editingRide" class="modal-backdrop" @click.self="closeEditRide">
      <form class="edit-ride-modal surface-card" @submit.prevent="submitRideEdit">
        <div class="modal-header">
          <div>
            <span class="eyebrow">编辑招募信息</span>
            <h2>{{ editingRide.title }}</h2>
          </div>
          <button class="modal-close" type="button" aria-label="关闭编辑窗口" @click="closeEditRide">
            <X :size="18" />
          </button>
        </div>

        <div class="edit-form-grid">
          <div class="form-group full">
            <label class="form-label" for="edit-title">车位标题</label>
            <input id="edit-title" v-model.trim="rideForm.title" class="form-control" type="text" required maxlength="100" />
          </div>

          <div class="form-group">
            <label class="form-label" for="edit-product">产品类型</label>
            <select id="edit-product" v-model="rideForm.product" class="form-control" required>
              <option value="chatgpt-plus">ChatGPT Plus</option>
              <option value="chatgpt-team">ChatGPT Business</option>
              <option value="chatgpt-pro">ChatGPT Pro</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label" for="edit-status">招募状态</label>
            <select id="edit-status" v-model="rideForm.status" class="form-control" required>
              <option value="open">招募中</option>
              <option value="closed">已暂停</option>
              <option value="expired">已过期</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="edit-total-seats">总人数</label>
            <input id="edit-total-seats" v-model.number="rideForm.total_seats" class="form-control" type="number" min="2" max="20" required />
          </div>
          <div class="form-group">
            <label class="form-label" for="edit-recruit-seats">上车人数</label>
            <input id="edit-recruit-seats" v-model.number="rideForm.recruit_seats" class="form-control" type="number" min="1" :max="rideForm.total_seats" required />
          </div>
          <div class="form-group">
            <label class="form-label" for="edit-duration">有效期限(月)</label>
            <input id="edit-duration" v-model.number="rideForm.duration" class="form-control" type="number" min="1" max="24" required />
          </div>
          <div class="form-group">
            <label class="form-label" for="edit-price">分摊月费(¥)</label>
            <input id="edit-price" v-model.number="rideForm.price_per_month" class="form-control" type="number" min="1" required />
          </div>
          <div class="form-group">
            <label class="form-label" for="edit-warranty">质保天数</label>
            <input id="edit-warranty" v-model.number="rideForm.warranty_days" class="form-control" type="number" min="1" max="730" required />
          </div>

          <div class="form-group full">
            <label class="form-label" for="edit-desc">公开说明</label>
            <textarea id="edit-desc" v-model.trim="rideForm.description" class="form-control textarea-control" rows="3"></textarea>
          </div>
          <div class="form-group full">
            <label class="form-label" for="edit-contact">隐藏联系方式</label>
            <textarea id="edit-contact" v-model.trim="rideForm.contact_info" class="form-control textarea-control" rows="4" required></textarea>
          </div>
          <div class="form-group full">
            <label class="form-label" for="edit-website">个人网站</label>
            <input id="edit-website" v-model.trim="rideForm.contact_website" class="form-control" type="url" placeholder="https://example.com" />
          </div>
        </div>

        <p v-if="rideEditMessage" class="edit-message" :class="{ error: rideEditError }">{{ rideEditMessage }}</p>
        <div class="modal-actions">
          <button class="btn btn-secondary" type="button" @click="closeEditRide">取消</button>
          <button class="btn btn-primary" type="submit" :disabled="savingRide">
            <Save :size="16" />
            <span>{{ savingRide ? '保存中...' : '保存修改' }}</span>
          </button>
        </div>
      </form>
    </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { computed, markRaw, onMounted, reactive, ref } from 'vue'
import { Copy, Eye, FileChartColumn, KeyRound, PackageOpen, Pencil, PlusCircle, Power, ReceiptText, Save, Settings, Trash2, X } from '@lucide/vue'
import { useUserStore } from '../stores/user'
import { authApi } from '../api/auth'
import { ridesApi } from '../api/rides'
import { ordersApi } from '../api/orders'
import type { Order, ProductType, Ride } from '../types'

interface SalesRide {
  ride_id: number
  ride_title: string
  order_count: number
  unlock_count: number
  revenue: number
  total_seats: number
  recruit_seats: number
  remaining_seats: number
  status: string
  latest_unlock_at?: string | null
}

interface SalesSummary {
  total_revenue: number
  total_orders: number
  total_unlocks: number
  rides: SalesRide[]
}

const userStore = useUserStore()
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt&backgroundColor=0f172a'
const loading = ref(true)
const saving = ref(false)
const savingPassword = ref(false)
const saveMessage = ref('')
const passwordMessage = ref('')
const passwordError = ref(false)
const activeTab = ref<'orders' | 'published' | 'sales' | 'settings'>('orders')
const orders = ref<Order[]>([])
const ownedRides = ref<Ride[]>([])
const sales = ref<SalesSummary | null>(null)
const copyStates = ref<Record<string, boolean>>({})
const actionLoadingId = ref<number | null>(null)
const editingRide = ref<Ride | null>(null)
const savingRide = ref(false)
const rideEditMessage = ref('')
const rideEditError = ref(false)

const tabs = [
  { value: 'orders' as const, label: '我的拼车', icon: markRaw(ReceiptText) },
  { value: 'published' as const, label: '我的发布', icon: markRaw(PackageOpen) },
  { value: 'sales' as const, label: '拼车统计', icon: markRaw(FileChartColumn) },
  { value: 'settings' as const, label: '账户设置', icon: markRaw(Settings) },
]

const unlockedOrders = computed(() => orders.value.filter((order) => order.status === 'paid'))
const rideOnboardSeats = (ride: Ride) => Number(ride.recruit_seats || Math.max((ride.total_seats || 1) - 1, 1))
const rideOccupiedSeats = (ride: Ride) => Math.min(rideOnboardSeats(ride), Number(ride.total_seats || 0))
const orderOnboardSeats = (order: Order) => Number(order.ride_recruit_seats || Math.max((order.ride_total_seats || 1) - 1, 1))
const orderOccupiedSeats = (order: Order) => Math.min(orderOnboardSeats(order), Number(order.ride_total_seats || 0))

const editForm = reactive({
  nickname: '',
  avatar: '',
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const rideForm = reactive({
  title: '',
  product: 'chatgpt-plus' as ProductType,
  total_seats: 2,
  recruit_seats: 1,
  price_per_month: 1,
  duration: 1,
  warranty_days: 30,
  description: '',
  contact_info: '',
  contact_website: '',
  contact_price: 0,
  status: 'open' as Ride['status'],
})

const formattedRegisterDate = computed(() => {
  if (!userStore.user?.created_at) return ''
  return formatDate(userStore.user.created_at)
})

const avatarPreviewUrl = computed(() => editForm.avatar || userStore.user?.avatar || defaultAvatar)

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
    editForm.avatar = userStore.user?.avatar || ''
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
    await userStore.updateProfile(editForm.nickname, editForm.avatar)
    saveMessage.value = '基本信息已成功更新'
  } catch {
    saveMessage.value = '更新失败，请稍后重试'
  } finally {
    saving.value = false
  }
}

const handleAvatarError = (event: Event) => {
  const target = event.target as HTMLImageElement
  if (target.src !== defaultAvatar) {
    target.src = defaultAvatar
  }
}

const handlePasswordChange = async () => {
  passwordMessage.value = ''
  passwordError.value = false
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordError.value = true
    passwordMessage.value = '两次输入的新密码不一致'
    return
  }
  if (passwordForm.current_password === passwordForm.new_password) {
    passwordError.value = true
    passwordMessage.value = '新密码不能与当前密码相同'
    return
  }

  savingPassword.value = true
  try {
    await authApi.changePassword(passwordForm.current_password, passwordForm.new_password)
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    passwordMessage.value = '登录密码已更新'
  } catch (err) {
    const error = err as { response?: { data?: { detail?: string } } }
    passwordError.value = true
    passwordMessage.value = error.response?.data?.detail || '密码更新失败，请稍后重试'
  } finally {
    savingPassword.value = false
  }
}

const openEditRide = (ride: Ride) => {
  editingRide.value = ride
  rideForm.title = ride.title
  rideForm.product = ride.product
  rideForm.total_seats = ride.total_seats
  rideForm.recruit_seats = rideOnboardSeats(ride)
  rideForm.price_per_month = Number(ride.price_per_month)
  rideForm.duration = ride.duration
  rideForm.warranty_days = ride.warranty_days
  rideForm.description = ride.description || ''
  rideForm.contact_info = ride.contact_info || ''
  rideForm.contact_website = ride.contact_website || ''
  rideForm.contact_price = Number(ride.contact_price || 0)
  rideForm.status = ride.status
  rideEditMessage.value = ''
  rideEditError.value = false
}

const closeEditRide = () => {
  if (savingRide.value) return
  editingRide.value = null
  rideEditMessage.value = ''
  rideEditError.value = false
}

const validateRideForm = () => {
  if (!rideForm.title.trim()) return '请填写车位标题'
  if (!rideForm.contact_info.trim() && !rideForm.contact_website.trim()) return '请至少保留一种联系方式'
  if (rideForm.contact_website && !/^https?:\/\/[^\s.]+\.[^\s]+$/i.test(rideForm.contact_website)) return '个人网站需要以 http:// 或 https:// 开头'
  if (rideForm.recruit_seats > rideForm.total_seats) return '上车人数不能超过总人数'
  return ''
}

const submitRideEdit = async () => {
  if (!editingRide.value) return
  const error = validateRideForm()
  if (error) {
    rideEditError.value = true
    rideEditMessage.value = error
    return
  }
  savingRide.value = true
  rideEditMessage.value = ''
  rideEditError.value = false
  try {
    const res = await ridesApi.updateRide(editingRide.value.id, {
      title: rideForm.title,
      product: rideForm.product,
      total_seats: rideForm.total_seats,
      recruit_seats: rideForm.recruit_seats,
      price_per_month: rideForm.price_per_month,
      duration: rideForm.duration,
      warranty_days: rideForm.warranty_days,
      description: rideForm.description,
      contact_info: rideForm.contact_info,
      contact_website: rideForm.contact_website,
      contact_price: rideForm.contact_price,
      status: rideForm.status,
    })
    ownedRides.value = ownedRides.value.map((ride) => (ride.id === res.data.id ? res.data : ride))
    await loadSalesOnly()
    rideEditMessage.value = '招募信息已更新'
    setTimeout(closeEditRide, 500)
  } catch (err) {
    const apiError = err as { response?: { data?: { detail?: string } } }
    rideEditError.value = true
    rideEditMessage.value = apiError.response?.data?.detail || '保存失败，请稍后重试'
  } finally {
    savingRide.value = false
  }
}

const loadSalesOnly = async () => {
  const salesRes = await ordersApi.getMySales()
  sales.value = salesRes.data
}

const toggleRideStatus = async (ride: Ride) => {
  actionLoadingId.value = ride.id
  try {
    const nextStatus = ride.status === 'open' ? 'closed' : 'open'
    const res = await ridesApi.updateRide(ride.id, { status: nextStatus })
    ownedRides.value = ownedRides.value.map((item) => (item.id === ride.id ? res.data : item))
    await loadSalesOnly()
  } finally {
    actionLoadingId.value = null
  }
}

const deleteRide = async (ride: Ride) => {
  if ((ride.purchase_count || 0) > 0) return
  const confirmedDelete = window.confirm(`确认删除「${ride.title}」吗？删除后市场和详情页将不再展示。`)
  if (!confirmedDelete) return
  actionLoadingId.value = ride.id
  try {
    await ridesApi.deleteRide(ride.id)
    ownedRides.value = ownedRides.value.filter((item) => item.id !== ride.id)
    await loadSalesOnly()
  } catch (err) {
    const apiError = err as { response?: { data?: { detail?: string } } }
    window.alert(apiError.response?.data?.detail || '删除失败，请稍后重试')
  } finally {
    actionLoadingId.value = null
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

const orderContactText = (order: Order) => {
  return [
    order.ride_contact_info || '',
    order.ride_contact_website ? `个人网站：${order.ride_contact_website}` : '',
  ].filter(Boolean).join('\n')
}

const productLabel = (product?: string) => {
  if (product === 'chatgpt-team') return 'Business 团队'
  if (product === 'chatgpt-pro') return 'Pro 极客'
  if (product === 'chatgpt-plus') return 'Plus 拼车'
  return '-'
}

const statusLabel = (status?: string) => {
  if (status === 'closed') return '已暂停'
  if (status === 'expired') return '已过期'
  return '招募中'
}

const formatMoney = (value: number | string) => Math.round(Number(value || 0))

const formatDate = (dateText: string) => {
  const date = new Date(dateText)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}
</script>

<style scoped>
.profile-page {
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

/* ===== Skeleton Loading ===== */
.skeleton-workspace {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: var(--spacing-xl);
}

.skel-row {
  display: flex;
  gap: 16px;
  align-items: center;
}

.skel {
  background: var(--bg-tertiary);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--border-radius-sm);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skel-cell {
  height: 16px;
  flex-shrink: 0;
}

.skel-w10 { width: 10%; }
.skel-w15 { width: 15%; }
.skel-w20 { width: 20%; }
.skel-w25 { width: 25%; }

.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-md);
  padding: var(--spacing-lg) var(--spacing-xl);
  background: var(--bg-card);
  border-color: color-mix(in srgb, var(--color-info) 24%, var(--border-color));
  position: relative;
  overflow: hidden;
}

.profile-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--border-color-strong);
  opacity: 0.5;
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
  border: 2px solid var(--bg-card);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.online-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  background: var(--color-success);
  border: 2px solid var(--bg-card);
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
  letter-spacing: 0;
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
  gap: 10px;
}

.stat-card {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: var(--bg-card);
  transition: all var(--transition-fast);
  cursor: default;
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
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card:nth-child(1)::before { background: var(--color-team); }
.stat-card:nth-child(2)::before { background: var(--color-success); }
.stat-card:nth-child(3)::before { background: var(--color-pro); }

.stat-card:hover {
  border-color: var(--border-color-strong);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.stat-card:nth-child(1) .stat-value { color: var(--color-team); }
.stat-card:nth-child(2) .stat-value { color: var(--color-success); }
.stat-card:nth-child(3) .stat-value { color: var(--color-pro); }

.stat-label {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 700;
  line-height: 1.3;
}

.stat-value {
  color: var(--text-primary);
  font-size: 26px;
  font-weight: 800;
  line-height: 1;
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
}

.workspace-tabs {
  display: flex;
  min-width: 0;
  gap: 4px;
  padding: var(--spacing-sm) var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-inset);
  position: relative;
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
  white-space: nowrap;
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
  position: relative;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 2px;
  border-radius: var(--border-radius-full);
  background: var(--color-team);
  animation: tabIndicator 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes tabIndicator {
  from {
    width: 0;
    opacity: 0;
  }
  to {
    width: 24px;
    opacity: 1;
  }
}

.tab-content {
  padding: var(--spacing-xl);
}

.records-table {
  min-width: 800px;
}

.records-table th {
  font-size: 11px;
  letter-spacing: 0.05em;
}

.records-table td {
  padding: 14px 12px;
  color: var(--text-secondary);
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
  position: relative;
  overflow: hidden;
  transition: all var(--transition-fast);
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.summary-card:hover::before {
  opacity: 1;
}

.summary-card:nth-child(1)::before { background: var(--color-team); }
.summary-card:nth-child(2)::before { background: var(--color-success); }

.summary-card:hover {
  border-color: var(--border-color-strong);
  transform: translateY(-1px);
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

/* Published ride manager */
.published-manager {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.published-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-md);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  position: relative;
}

.published-toolbar::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 48px;
  height: 2px;
  background: var(--color-success);
  border-radius: var(--border-radius-full);
  opacity: 0.6;
}

.published-toolbar h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 0;
}

.published-toolbar p,
.manager-note {
  margin: 4px 0 0;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.6;
}

.published-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.manage-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-left: 3px solid transparent;
  border-radius: var(--border-radius-md);
  background: var(--bg-secondary);
  transition: all var(--transition-fast);
}

.manage-card:hover {
  border-color: var(--border-color-strong);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.manage-card.chatgpt-plus:hover { border-left-color: var(--color-plus); }
.manage-card.chatgpt-team:hover { border-left-color: var(--color-team); }
.manage-card.chatgpt-pro:hover { border-left-color: var(--color-pro); }

.manage-card-main {
  min-width: 0;
}

.manage-title-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.manage-title {
  display: block;
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 800;
  line-height: 1.4;
  text-decoration: none;
}

.manage-title:hover {
  color: var(--color-team);
}

.manage-card.chatgpt-plus .manage-title:hover { color: var(--color-plus); }
.manage-card.chatgpt-team .manage-title:hover { color: var(--color-team); }
.manage-card.chatgpt-pro .manage-title:hover { color: var(--color-pro); }

.manage-desc {
  display: -webkit-box;
  margin: 6px 0 14px;
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.55;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.manage-metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}

.manage-metrics div {
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: var(--bg-inset);
}

.manage-metrics span {
  display: block;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
}

.manage-metrics strong {
  display: block;
  margin-top: 3px;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 800;
  white-space: nowrap;
}

.manage-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(72px, 1fr));
  align-content: start;
  gap: 8px;
}

.icon-action {
  display: inline-flex;
  min-height: 36px;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 0 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 750;
  text-decoration: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.icon-action:hover:not(:disabled) {
  background: var(--text-primary);
  border-color: var(--text-primary);
  color: var(--text-inverse);
}

.icon-action.danger {
  color: var(--color-danger);
}

.icon-action.danger:hover:not(:disabled) {
  background: var(--color-danger);
  border-color: var(--color-danger);
  color: var(--text-inverse);
}

.icon-action:disabled {
  cursor: not-allowed;
  opacity: 0.48;
}

.status-chip.closed {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.status-chip.expired {
  background: var(--color-danger-soft);
  color: var(--color-danger);
}

:global([data-theme="dark"] .status-chip.expired ){
  background: rgba(248, 113, 113, 0.12);
  color: #f87171;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  background: rgba(15, 23, 42, 0.52);
  backdrop-filter: blur(8px);
}

.modal-enter-active {
  transition: opacity 0.2s ease;
}

.modal-enter-active .edit-ride-modal {
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.2s ease;
}

.modal-leave-active {
  transition: opacity 0.15s ease;
}

.modal-leave-active .edit-ride-modal {
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.modal-enter-from {
  opacity: 0;
}

.modal-enter-from .edit-ride-modal {
  opacity: 0;
  transform: translateY(16px) scale(0.97);
}

.modal-leave-to {
  opacity: 0;
}

.modal-leave-to .edit-ride-modal {
  opacity: 0;
  transform: translateY(8px) scale(0.98);
}

.edit-ride-modal {
  width: min(760px, 100%);
  max-height: min(86vh, 860px);
  overflow: auto;
  padding: var(--spacing-xl);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.modal-header h2 {
  margin: 4px 0 0;
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 850;
  line-height: 1.35;
  letter-spacing: 0;
}

.modal-close {
  display: inline-flex;
  width: 36px;
  height: 36px;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: var(--bg-inset);
  color: var(--text-secondary);
  cursor: pointer;
}

.modal-close:hover {
  color: var(--text-primary);
  border-color: var(--border-color-strong);
}

.edit-form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.form-group.full {
  grid-column: 1 / -1;
}

.form-label {
  display: inline-flex;
  align-items: center;
  min-height: 18px;
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 750;
  line-height: 1.2;
}

.form-control {
  min-height: 44px;
}

.textarea-control {
  min-height: 96px;
  resize: vertical;
}

.edit-message {
  margin: var(--spacing-md) 0 0;
  color: var(--color-success);
  font-size: 13px;
  font-weight: 750;
}

.edit-message.error {
  color: var(--color-danger);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}

/* Settings Form */
.settings-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-lg);
}

.settings-panel {
  padding: var(--spacing-lg);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  position: relative;
}

.settings-panel:first-child::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-team);
  border-radius: var(--border-radius-md) var(--border-radius-md) 0 0;
  opacity: 0.5;
}

.settings-panel:last-child::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-pro);
  border-radius: var(--border-radius-md) var(--border-radius-md) 0 0;
  opacity: 0.5;
}

.settings-panel-heading h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0;
}

.settings-panel-heading p {
  margin: 4px 0 0;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.5;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.avatar-setting {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.avatar-preview {
  flex: 0 0 48px;
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius-full);
  border: 1px solid var(--border-color-strong);
  background: var(--bg-secondary);
  object-fit: cover;
}

.avatar-setting strong,
.avatar-setting span {
  display: block;
}

.avatar-setting strong {
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 800;
}

.avatar-setting span {
  margin-top: 3px;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.45;
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

.save-message.error {
  color: var(--color-danger);
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
  .stat-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 6px;
  }
  .stat-card {
    min-height: 64px;
    justify-content: space-between;
    padding: 10px 9px;
    border-radius: var(--border-radius-md);
  }
  .stat-label {
    min-height: 28px;
    font-size: 10px;
    line-height: 1.35;
  }
  .stat-value {
    font-size: 22px;
  }
  .stat-value small {
    font-size: 10px;
  }
  .sales-summary-cards {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }
  .workspace-tabs {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  .tab-btn {
    flex: 0 0 auto;
  }
  .rides-grid {
    grid-template-columns: 1fr;
  }
  .published-toolbar,
  .manage-card,
  .settings-grid {
    grid-template-columns: 1fr;
  }
  .published-toolbar {
    align-items: stretch;
  }
  .publish-toolbar-btn {
    width: 100%;
  }
  .manage-metrics,
  .edit-form-grid {
    grid-template-columns: 1fr 1fr;
  }
  .manage-actions {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
  .icon-action {
    min-width: 0;
    padding: 0 6px;
  }
  .modal-backdrop {
    align-items: flex-end;
    padding: var(--spacing-sm);
  }
  .edit-ride-modal {
    max-height: 92vh;
    padding: var(--spacing-lg);
  }
  .modal-actions {
    flex-direction: column-reverse;
  }
  .modal-actions .btn {
    width: 100%;
  }
}

@media (max-width: 520px) {
  .manage-metrics {
    grid-template-columns: 1fr;
  }
  .manage-actions {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .edit-form-grid {
    grid-template-columns: 1fr;
  }
}

.chip-logo {
  width: 14px;
  height: 14px;
  object-fit: contain;
  flex-shrink: 0;
}

.submit-shimmer {
  position: relative;
  overflow: hidden;
}

.submit-shimmer::after {
  content: '';
  position: absolute;
  inset: 0;
  background: transparent;
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.submit-shimmer:hover::after {
  transform: translateX(100%);
}

/* Dark mode polish */
:global([data-theme="dark"] .stat-card:hover ){
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

:global([data-theme="dark"] .manage-card:hover ){
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

:global([data-theme="dark"] .manage-card.chatgpt-plus:hover ){
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
}

:global([data-theme="dark"] .manage-card.chatgpt-team:hover ){
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.1);
}

:global([data-theme="dark"] .manage-card.chatgpt-pro:hover ){
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.1);
}

:global([data-theme="dark"] .settings-panel ){
  background: var(--bg-tertiary);
}

:global([data-theme="dark"] .summary-card:hover ){
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

:global([data-theme="dark"] .btn-copy:hover ){
  background: var(--color-team);
  border-color: var(--color-team);
}
</style>
