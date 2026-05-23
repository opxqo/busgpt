<template>
  <div class="detail-page container">
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载车位详情中</p>
    </div>

    <div v-else-if="error" class="error-container surface-card">
      <CircleAlert :size="34" />
      <h3>加载失败</h3>
      <p>{{ error }}</p>
      <router-link to="/market" class="btn btn-primary">返回市场</router-link>
    </div>

    <div v-else-if="ride" class="detail-grid">
      <main class="detail-main">
        <section class="listing-header surface-card">
          <div class="header-tags">
            <span class="product-chip" :class="ride.product">{{ productLabel }}</span>
            <span class="status-chip" :class="ride.status">{{ statusLabel }}</span>
          </div>
          <h1>{{ ride.title }}</h1>
          <p>{{ ride.description || '车主暂未填写公开说明。支付信息服务费后可查看隐藏联系方式。' }}</p>

          <div class="metric-grid">
            <div class="metric-primary">
              <span>车位月费</span>
              <strong>¥{{ formatMoney(ride.price_per_month) }}<small>/月</small></strong>
            </div>
            <div>
              <span>已拼人数</span>
              <strong>{{ ride.purchase_count || 0 }}<small> 人</small></strong>
            </div>
            <div>
              <span>还差人数</span>
              <strong>{{ ride.remaining_seats ?? ride.total_seats }}<small> 人</small></strong>
            </div>
            <div>
              <span>总名额</span>
              <strong>{{ ride.total_seats }}<small> 个</small></strong>
            </div>
            <div>
              <span>有效期</span>
              <strong>{{ ride.duration }}<small> 个月</small></strong>
            </div>
            <div>
              <span>服务费</span>
              <strong class="fee">¥{{ formatMoney(ride.contact_price) }}</strong>
            </div>
          </div>
        </section>

        <section class="surface-card info-card">
          <div class="section-title">
            <FileText :size="18" />
            <h2>公开展示信息</h2>
          </div>
          <div class="info-list">
            <div>
              <span>产品类型</span>
              <strong>{{ productLabel }}</strong>
            </div>
            <div>
              <span>最近更新</span>
              <strong>{{ formattedCreatedAt }}</strong>
            </div>
            <div>
              <span>到期时间</span>
              <strong>{{ formattedExpiryDate }}</strong>
            </div>
            <div>
              <span>已解锁次数</span>
              <strong>{{ ride.purchase_count || 0 }} 次</strong>
            </div>
            <div>
              <span>拼车进度</span>
              <strong>{{ ride.purchase_count || 0 }}/{{ ride.total_seats }} 人</strong>
            </div>
          </div>
        </section>

        <section class="surface-card info-card">
          <div class="section-title">
            <ShieldCheck :size="18" />
            <h2>服务边界</h2>
          </div>
          <div class="disclaimer-grid">
            <p>平台仅提供商品信息展示和联系方式展示服务，不提供站内聊天。</p>
            <p>信息服务费不是订阅款，也不代表平台代收后续费用。</p>
            <p>解锁后请自行与车主沟通，谨慎确认订阅周期、账号规则和付款方式。</p>
          </div>
        </section>
      </main>

      <aside class="detail-side">
        <section class="surface-card owner-card">
          <div class="owner-head">
            <img :src="ride.owner?.avatar || defaultAvatar" alt="车主头像" class="avatar" />
            <div>
              <strong>{{ ride.owner?.nickname || '车主' }}</strong>
              <span>车主已验证</span>
            </div>
          </div>
          <div class="owner-facts">
            <span><BadgeCheck :size="14" /> 手机号已绑定</span>
            <span><ReceiptText :size="14" /> {{ ride.purchase_count || 0 }} 次信息解锁</span>
          </div>
        </section>

        <section class="surface-card unlock-card" :class="{ revealed: canSeeContact }">
          <div class="unlock-head">
            <div class="lock-icon">
              <Unlock v-if="canSeeContact" :size="22" />
              <LockKeyhole v-else :size="22" />
            </div>
            <div>
              <h2>{{ canSeeContact ? '联系方式已解锁' : '联系方式已隐藏' }}</h2>
              <p>{{ canSeeContact ? '你可以复制信息，自行联系车主。' : '支付信息服务费后可查看车主联系方式。' }}</p>
            </div>
          </div>

          <div v-if="canSeeContact" class="contact-box">
            <label>车主联系方式</label>
            <div
              v-for="item in contactItems"
              :key="`${item.type}-${item.account}`"
              class="contact-reveal"
              :class="item.type"
            >
              <div class="contact-kind">
                <component :is="item.icon" :size="18" />
                <span>{{ item.label }}</span>
              </div>
              <a v-if="item.href" class="contact-account" :href="item.href" target="_blank" rel="noreferrer">
                {{ item.account }}
                <ExternalLink :size="15" />
              </a>
              <strong v-else class="contact-account">{{ item.account }}</strong>
              <p v-if="item.note">{{ item.note }}</p>
            </div>
            <button type="button" class="btn btn-primary" @click="copyContact">
              <Copy :size="16" />
              {{ copied ? '已复制' : '复制联系方式' }}
            </button>
          </div>

          <div v-else class="locked-box">
            <div class="order-row">
              <span>信息服务费</span>
              <strong>¥{{ formatMoney(ride.contact_price) }}</strong>
            </div>
            <div class="order-row">
              <span>解锁内容</span>
              <strong>邮箱 / 微信 / Telegram</strong>
            </div>
            <div class="order-row">
              <span>当前进度</span>
              <strong>已拼 {{ ride.purchase_count || 0 }} 人，还差 {{ ride.remaining_seats ?? ride.total_seats }} 人</strong>
            </div>
            <label class="terms-row">
              <input v-model="termsAccepted" type="checkbox" />
              <span>我确认该费用仅用于解锁联系方式，后续交易需自行沟通。</span>
            </label>
            <button
              type="button"
              class="btn btn-primary unlock-btn"
              :disabled="unlockDisabled"
              @click="handleUnlock"
            >
              <CreditCard :size="16" />
              {{ purchasing ? '生成订单中...' : unlockButtonText }}
            </button>
            <p v-if="purchaseError" class="purchase-error">{{ purchaseError }}</p>
          </div>
        </section>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  BadgeCheck,
  CircleAlert,
  Copy,
  CreditCard,
  ExternalLink,
  FileText,
  LockKeyhole,
  Mail,
  MessageCircle,
  ReceiptText,
  SendHorizontal,
  ShieldCheck,
  Unlock,
} from '@lucide/vue'
import type { Component } from 'vue'
import { ridesApi } from '../api/rides'
import { ordersApi } from '../api/orders'
import { useUserStore } from '../stores/user'
import type { ContactType } from '../types'
import type { Ride } from '../types'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const ride = ref<Ride | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const purchasing = ref(false)
const purchaseError = ref('')
const termsAccepted = ref(false)
const copied = ref(false)
const rideId = Number(route.params.id)
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt'

const loadRideDetails = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await ridesApi.getRide(rideId)
    ride.value = res.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || '加载详情失败'
  } finally {
    loading.value = false
  }
}

onMounted(loadRideDetails)

const isOwner = computed(() => {
  return !!ride.value && !!userStore.user && ride.value.owner_id === userStore.user.id
})

const canSeeContact = computed(() => {
  return !!ride.value?.contact_info && (isOwner.value || ride.value.is_purchased)
})

type ContactItem = {
  type: ContactType
  label: string
  icon: Component
  account: string
  note: string
  href: string
}

const contactMeta: Record<ContactType, { label: string; icon: Component }> = {
  email: { label: '邮箱', icon: Mail },
  wechat: { label: '微信', icon: MessageCircle },
  telegram: { label: 'Telegram', icon: SendHorizontal },
}

const normalizeTelegramHref = (account: string) => {
  const username = account.replace('https://t.me/', '').replace('http://t.me/', '').replace('@', '').trim()
  return username ? `https://t.me/${username}` : ''
}

const contactHref = (type: ContactType, account: string) => {
  if (type === 'email') return `mailto:${account}`
  if (type === 'telegram') return normalizeTelegramHref(account)
  return ''
}

const buildContactItem = (type: ContactType, account: string, note = ''): ContactItem => ({
  type,
  label: contactMeta[type].label,
  icon: contactMeta[type].icon,
  account: account.trim(),
  note,
  href: contactHref(type, account.trim()),
})

const contactItems = computed<ContactItem[]>(() => {
  const raw = ride.value?.contact_info || ''
  const lines = raw.split('\n').map((line) => line.trim()).filter(Boolean)
  const note = lines
    .filter((line) => line.startsWith('备注：') || line.toLowerCase().startsWith('note:'))
    .map((line) => line.replace(/^备注：/i, '').replace(/^note:\s*/i, '').trim())
    .filter(Boolean)
    .join('；')
  const items: ContactItem[] = []

  const addItem = (type: ContactType, account?: string) => {
    const value = account?.trim()
    if (!value) return
    if (items.some((item) => item.type === type && item.account === value)) return
    items.push(buildContactItem(type, value, note))
  }

  const extractByLabels = (labels: string[]) => {
    const labelPattern = labels.join('|')
    const nextLabelPattern = '邮箱|email|微信|wechat|telegram|电报|tg|备注|note'
    const pattern = new RegExp(`(?:^|\\n|\\s)(?:${labelPattern})\\s*[:：]\\s*([^\\n]+?)(?=\\s+(?:${nextLabelPattern})\\s*[:：]|$)`, 'i')
    return raw.match(pattern)?.[1]?.trim()
  }

  addItem('email', extractByLabels(['邮箱', 'email']))
  addItem('wechat', extractByLabels(['微信', 'wechat']))
  addItem('telegram', extractByLabels(['telegram', '电报', 'tg']))

  lines.forEach((line) => {
    const match = line.match(/^(邮箱|email|微信|wechat|telegram|电报|tg)\s*[:：]\s*(.+)$/i)
    if (!match) return
    const key = (match[1] || '').toLowerCase()
    const value = match[2] || ''
    if (key === '邮箱' || key === 'email') addItem('email', value)
    if (key === '微信' || key === 'wechat') addItem('wechat', value)
    if (key === 'telegram' || key === '电报' || key === 'tg') addItem('telegram', value)
  })

  const oldChannel = lines.find((line) => line.startsWith('联系渠道：'))?.replace('联系渠道：', '').trim()
  const oldAccount = lines.find((line) => line.startsWith('账号：'))?.replace('账号：', '').trim()
  if (oldChannel && oldAccount) {
    const lower = `${oldChannel} ${oldAccount}`.toLowerCase()
    if (lower.includes('telegram') || oldAccount.startsWith('@') || oldAccount.includes('t.me/')) addItem('telegram', oldAccount)
    else if (lower.includes('邮箱') || lower.includes('email') || oldAccount.includes('@')) addItem('email', oldAccount)
    else addItem('wechat', oldAccount)
  }

  const emailMatch = raw.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)
  addItem('email', emailMatch?.[0])

  const telegramMatch = raw.match(/(?:https?:\/\/t\.me\/[-_a-zA-Z0-9]{5,32}|@[-_a-zA-Z0-9]{5,32})/)
  addItem('telegram', telegramMatch?.[0])

  if (!items.length && raw.trim()) addItem('wechat', raw.trim())
  return items
})

const productLabel = computed(() => {
  if (!ride.value) return ''
  if (ride.value.product === 'chatgpt-team') return 'ChatGPT Team'
  if (ride.value.product === 'chatgpt-pro') return 'ChatGPT Pro'
  return 'ChatGPT Plus'
})

const statusLabel = computed(() => {
  if (!ride.value) return ''
  if (ride.value.status === 'closed') return '已关闭'
  if (ride.value.status === 'expired') return '已过期'
  return '可解锁'
})

const formattedCreatedAt = computed(() => {
  if (!ride.value) return ''
  const date = new Date(ride.value.created_at)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
})

const formattedExpiryDate = computed(() => {
  if (!ride.value) return ''
  const date = new Date(ride.value.expires_at)
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
})

const unlockButtonText = computed(() => {
  if (!ride.value) return '解锁联系方式'
  if (isOwner.value) return '车主无需购买'
  if (ride.value.status !== 'open') return '当前不可解锁'
  if ((ride.value.remaining_seats ?? 1) <= 0) return '人数已满'
  return '支付服务费，解锁联系方式'
})

const unlockDisabled = computed(() => {
  return purchasing.value || !termsAccepted.value || isOwner.value || ride.value?.status !== 'open' || ((ride.value?.remaining_seats ?? 1) <= 0)
})

const handleUnlock = async () => {
  if (!ride.value) return
  if (!userStore.isLoggedIn) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  purchaseError.value = ''
  purchasing.value = true
  try {
    await ordersApi.purchaseContact(ride.value.id)
    await loadRideDetails()
  } catch (err: any) {
    purchaseError.value = err.response?.data?.detail || '解锁失败，请稍后重试'
  } finally {
    purchasing.value = false
  }
}

const copyContact = async () => {
  if (!ride.value?.contact_info) return
  await navigator.clipboard.writeText(ride.value.contact_info)
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 1800)
}

const formatMoney = (value: number | string) => Math.round(Number(value || 0))
</script>

<style scoped>
.detail-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: var(--spacing-lg);
  align-items: start;
}

.detail-main,
.detail-side {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.detail-side {
  position: sticky;
  top: var(--spacing-lg);
}

.listing-header,
.info-card,
.owner-card,
.unlock-card {
  padding: var(--spacing-lg);
}

.header-tags {
  display: flex;
  gap: 8px;
  margin-bottom: var(--spacing-md);
}

.listing-header h1 {
  margin-bottom: 10px;
  color: var(--text-primary);
  font-size: 30px;
  font-weight: 900;
  line-height: 1.25;
}

.listing-header p {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.8;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}

.metric-grid div,
.info-list div {
  padding: 13px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.metric-grid span,
.info-list span {
  display: block;
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 800;
}

.metric-grid strong,
.info-list strong {
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 900;
}

.metric-grid small {
  color: var(--text-secondary);
  font-size: 12px;
}

.metric-grid .fee {
  color: var(--color-pro);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: var(--spacing-md);
}

.section-title h2 {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 900;
}

.info-list {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--spacing-sm);
}

.disclaimer-grid {
  display: grid;
  gap: var(--spacing-sm);
}

.disclaimer-grid p {
  padding: 12px;
  border-radius: var(--border-radius-md);
  background: var(--color-warning-soft);
  color: #7c4a00;
  font-size: 13px;
  line-height: 1.7;
}

.owner-head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
}

.owner-head strong {
  display: block;
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 900;
}

.owner-head span,
.owner-facts span {
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 700;
}

.owner-facts {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: var(--spacing-md);
}

.owner-facts span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.unlock-card {
  border-color: rgba(5, 150, 105, 0.25);
}

.unlock-card.revealed {
  background: linear-gradient(180deg, #ffffff 0%, #f2fbf6 100%);
}

.unlock-head {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 12px;
  align-items: start;
  margin-bottom: var(--spacing-lg);
}

.lock-icon {
  display: inline-flex;
  width: 42px;
  height: 42px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.unlock-head h2 {
  margin-bottom: 4px;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 900;
}

.unlock-head p {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

.contact-box label {
  display: block;
  margin-bottom: 8px;
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 800;
}

.contact-reveal {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: var(--spacing-md);
  padding: 14px;
  border: 1px solid var(--contact-border);
  border-radius: var(--border-radius-md);
  background: var(--contact-bg);
  --contact-bg: #f8fff9;
  --contact-border: rgba(5, 150, 105, 0.2);
  --contact-color: var(--color-primary);
  --contact-soft: var(--color-primary-soft);
}

.contact-reveal.email {
  --contact-bg: #fffafa;
  --contact-border: rgba(220, 38, 38, 0.2);
  --contact-color: #dc2626;
  --contact-soft: #fef2f2;
}

.contact-reveal.wechat {
  --contact-bg: #f8fff9;
  --contact-border: rgba(7, 193, 96, 0.24);
  --contact-color: #07c160;
  --contact-soft: #e9f9ee;
}

.contact-reveal.telegram {
  --contact-bg: #f6fbff;
  --contact-border: rgba(34, 158, 217, 0.25);
  --contact-color: #229ed9;
  --contact-soft: #e8f5ff;
}

.contact-kind {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  gap: 7px;
  padding: 5px 9px;
  border-radius: var(--border-radius-full);
  background: var(--contact-soft);
  color: var(--contact-color);
  font-size: 12px;
  font-weight: 900;
}

.contact-account {
  display: inline-flex;
  width: fit-content;
  max-width: 100%;
  align-items: center;
  gap: 6px;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 900;
  overflow-wrap: anywhere;
}

a.contact-account:hover {
  color: var(--contact-color);
  background: transparent;
}

.contact-reveal p {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.7;
}

.locked-box {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.order-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.order-row span {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 700;
}

.order-row strong {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 900;
}

.terms-row {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
  align-items: start;
  padding: 12px;
  border-radius: var(--border-radius-md);
  background: var(--color-warning-soft);
  color: #7c4a00;
  font-size: 12px;
  line-height: 1.6;
  cursor: pointer;
}

.unlock-btn {
  width: 100%;
  margin-top: var(--spacing-sm);
}

.purchase-error {
  color: var(--color-danger);
  font-size: 13px;
  font-weight: 800;
}

@media (max-width: 1080px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }

  .detail-side {
    position: static;
  }
}

@media (max-width: 680px) {
  .listing-header h1 {
    font-size: 24px;
  }

  .metric-grid,
  .info-list {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
