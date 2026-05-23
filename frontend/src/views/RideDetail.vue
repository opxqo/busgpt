<template>
  <div class="detail-page container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>正在获取车位详细信息...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container surface-card">
      <CircleAlert :size="38" class="error-icon" />
      <h3>详情获取失败</h3>
      <p>{{ error }}</p>
      <router-link to="/market" class="btn btn-primary">返回拼车市场</router-link>
    </div>

    <!-- Main Content -->
    <div v-else-if="ride" class="detail-grid">
      <div class="detail-main">
        <!-- Main Info Header -->
        <section class="listing-header surface-card">
          <div class="header-tags">
            <span class="product-chip" :class="ride.product">
              <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
              </svg>
              <span>{{ productLabel }}</span>
            </span>
            <span class="status-chip" :class="ride.status">{{ statusLabel }}</span>
          </div>
          <h1 class="ride-title">{{ ride.title }}</h1>
          <p class="ride-description">
            {{ ride.description || '该车位主人比较神秘，暂未填写详细的公开说明。支付信息服务费解锁后可以直接添加车主交流。' }}
          </p>

          <div class="metric-grid">
            <div class="metric-box highlighted">
              <span class="metric-label">车位租金</span>
              <strong class="metric-val">¥{{ formatMoney(ride.price_per_month) }}<small>/月</small></strong>
            </div>
            <div class="metric-box">
              <span class="metric-label">已拼人数</span>
              <strong class="metric-val">{{ ride.purchase_count || 0 }}<small> 人</small></strong>
            </div>
            <div class="metric-box">
              <span class="metric-label">剩余空位</span>
              <strong class="metric-val highlight-green">{{ ride.remaining_seats ?? ride.total_seats }}<small> 人</small></strong>
            </div>
            <div class="metric-box">
              <span class="metric-label">拼车期限</span>
              <strong class="metric-val">{{ ride.duration }}<small> 个月</small></strong>
            </div>
            <div class="metric-box">
              <span class="metric-label">信息解锁费</span>
              <strong class="metric-val highlight-purple">¥{{ formatMoney(ride.contact_price) }}</strong>
            </div>
          </div>
        </section>

        <!-- Specifications -->
        <section class="surface-card info-card">
          <div class="section-title">
            <FileText :size="18" class="section-icon" />
            <h2>拼车基本参数</h2>
          </div>
          <div class="spec-list">
            <div class="spec-item">
              <span class="spec-label">订阅产品</span>
              <strong class="spec-val">{{ productLabel }}</strong>
            </div>
            <div class="spec-item">
              <span class="spec-label">最近更新</span>
              <strong class="spec-val">{{ formattedCreatedAt }}</strong>
            </div>
            <div class="spec-item">
              <span class="spec-label">预期到期时间</span>
              <strong class="spec-val">{{ formattedExpiryDate }}</strong>
            </div>
            <div class="spec-item">
              <span class="spec-label">车位总容量</span>
              <strong class="spec-val">{{ ride.total_seats }} 人位</strong>
            </div>
          </div>
        </section>

        <!-- Disclaimer -->
        <section class="surface-card info-card disclaimer-card">
          <div class="section-title">
            <ShieldCheck :size="18" class="section-icon-safety" />
            <h2>服务边界与免责声明</h2>
          </div>
          <div class="disclaimer-content">
            <p>1. 平台仅提供共享信息的发布与展示服务，我们不组织拼车，亦无站内交谈渠道。</p>
            <p>2. 信息解锁服务费由平台收取引导对接，非拼车月租金，解锁后平台不介入后续交易。</p>
            <p>3. 拼车具有一定的线下风险，请添加车主后自行核实订阅账号的性质、周期及支付方式。</p>
          </div>
        </section>
      </div>

      <!-- Sidebar Sticky Controls -->
      <div class="detail-side">
        <!-- Seller Info -->
        <section class="surface-card owner-card">
          <div class="owner-header">
            <img :src="ride.owner?.avatar || defaultAvatar" alt="车主头像" class="avatar" />
            <div class="owner-meta">
              <strong>{{ ride.owner?.nickname || '认证车友' }}</strong>
              <span class="badge"><BadgeCheck :size="12" /> 车主已认证</span>
            </div>
          </div>
          <div class="owner-stats">
            <div class="owner-stat-item">
              <ReceiptText :size="14" />
              <span>已成功发出 {{ ride.purchase_count || 0 }} 个车位</span>
            </div>
          </div>
        </section>

        <!-- Contact Reveal Info Box -->
        <section class="surface-card unlock-card" :class="{ revealed: canSeeContact }">
          <div class="unlock-header">
            <div class="lock-indicator" :class="{ unlocked: canSeeContact }">
              <Unlock v-if="canSeeContact" :size="20" />
              <LockKeyhole v-else :size="20" />
            </div>
            <div class="unlock-title-wrap">
              <h2>{{ canSeeContact ? '联系方式已解锁' : '联系方式已锁定' }}</h2>
              <p>{{ canSeeContact ? '已成功取得车主联系方式，请私下沟通。' : '解锁后可实时查阅微信、Telegram、邮箱等。' }}</p>
            </div>
          </div>

          <!-- Revealed Contacts -->
          <div v-if="canSeeContact" class="contact-panel">
            <label class="panel-title-label">车主联系账号</label>
            <div class="contacts-list">
              <div
                v-for="(item, index) in contactItems"
                :key="`${item.type}-${item.account}`"
                class="contact-row-new"
                :class="item.type"
              >
                <!-- Brand logo wrapper -->
                <div class="brand-logo-wrapper" :class="item.type">
                  <!-- WeChat Official Green Logo -->
                  <svg v-if="item.type === 'wechat'" viewBox="0 0 576 512" class="brand-logo-svg">
                    <path fill="currentColor" d="M385.2 167.6c6.4 0 12.6.3 18.8 1.1C387.4 90.3 303.3 32 207.7 32 100.5 32 13 104.8 13 197.4c0 53.4 29.3 97.5 77.9 131.6l-19.3 58.6 68-34.1c24.4 4.8 43.8 9.7 68.2 9.7 6.2 0 12.1-.3 18.3-.8-4-12.9-6.2-26.6-6.2-40.8-.1-84.9 72.9-154 165.3-154zm-104.5-52.9c14.5 0 24.2 9.7 24.2 24.4 0 14.5-9.7 24.2-24.2 24.2-14.8 0-29.3-9.7-29.3-24.2.1-14.7 14.6-24.4 29.3-24.4zm-136.4 48.6c-14.5 0-29.3-9.7-29.3-24.2 0-14.8 14.8-24.4 29.3-24.4 14.8 0 24.4 9.7 24.4 24.4 0 14.6-9.6 24.2-24.4 24.2zM563 319.4c0-77.9-77.9-141.3-165.4-141.3-92.7 0-165.4 63.4-165.4 141.3S305 460.7 397.6 460.7c19.3 0 38.9-5.1 58.6-9.9l53.4 29.3-14.8-48.6C534 402.1 563 363.2 563 319.4zm-219.1-24.5c-9.7 0-19.3-9.7-19.3-19.6 0-9.7 9.7-19.3 19.3-19.3 14.8 0 24.4 9.7 24.4 19.3 0 10-9.7 19.6-24.4 19.6zm107.1 0c-9.7 0-19.3-9.7-19.3-19.6 0-9.7 9.7-19.3 19.3-19.3 14.5 0 24.4 9.7 24.4 19.3.1 10-9.9 19.6-24.4 19.6z"/>
                  </svg>
                  <!-- Telegram Official Blue Logo -->
                  <svg v-else-if="item.type === 'telegram'" viewBox="0 0 496 512" class="brand-logo-svg">
                    <path fill="currentColor" d="M248,8C111.033,8,0,119.033,0,256S111.033,504,248,504,496,392.967,496,256,384.967,8,248,8ZM362.952,176.66c-3.732,39.215-19.881,134.378-28.1,178.3-3.476,18.584-10.322,24.816-16.948,25.425-14.4,1.326-25.338-9.517-39.287-18.661-21.827-14.308-34.158-23.215-55.346-37.177-24.485-16.135-8.612-25,5.342-39.5,3.652-3.793,67.107-61.51,68.335-66.746.153-.655.3-3.1-1.154-4.384s-3.59-.849-5.135-.5q-3.283.746-104.608,69.142-14.845,10.194-26.894,9.934c-8.855-.191-25.888-5.006-38.551-9.123-15.531-5.048-27.875-7.717-26.8-16.291q.84-6.7,18.45-13.7,108.446-47.248,144.628-62.3c68.872-28.647,83.183-33.623,92.511-33.789,2.052-.034,6.639.474,9.61,2.885a10.452,10.452,0,0,1,3.53,6.716A43.765,43.765,0,0,1,362.952,176.66Z"/>
                  </svg>
                  <!-- Mail Envelope Logo -->
                  <svg v-else-if="item.type === 'email'" viewBox="0 0 512 512" class="brand-logo-svg">
                    <path fill="currentColor" d="M48 96h416c26.5 0 48 21.5 48 48v224c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V144c0-26.5 21.5-48 48-48z"/>
                    <path fill="#ffffff" d="M460.6 156.4c5.1 6.2 4.1 15.4-2.2 20.4L280.7 319.1c-14.5 11.6-35 11.6-49.5 0L53.6 176.8c-6.3-5-7.3-14.2-2.2-20.4s14.2-7.3 20.4-2.2L249.5 296.5c3.8 3 9.2 3 13 0L440.2 154.2c6.2-5.1 15.4-4.1 20.4 2.2z"/>
                  </svg>
                </div>

                <!-- Account info -->
                <div class="contact-details-wrap">
                  <span class="contact-type-label">{{ item.label }}</span>
                  <div class="account-link-container">
                    <a v-if="item.href" :href="item.href" target="_blank" rel="noreferrer" class="account-anchor">
                      <span>{{ item.account }}</span>
                      <ExternalLink :size="12" class="ext-icon" />
                    </a>
                    <span v-else class="account-plain-text">{{ item.account }}</span>
                  </div>
                  <p v-if="item.note" class="contact-note-text" :title="item.note">{{ item.note }}</p>
                </div>

                <!-- Individual Copy Button -->
                <button type="button" class="btn-copy-item" @click="copyIndividualContact(item.account, index)">
                  <Copy v-if="!individualCopied[index]" :size="12" />
                  <span class="copy-text">{{ individualCopied[index] ? '已复制' : '复制' }}</span>
                </button>
              </div>
            </div>
            <button type="button" class="btn btn-secondary action-btn-full" @click="copyContact">
              <Copy :size="16" />
              <span>{{ copied ? '已成功复制全部' : '复制全部联系方式' }}</span>
            </button>
          </div>

          <!-- Locked View (Pay to unlock) -->
          <div v-else class="locked-panel">
            <div class="unlock-cost-row">
              <span class="cost-label">信息解锁服务费</span>
              <strong class="cost-value">¥{{ formatMoney(ride.contact_price) }}</strong>
            </div>

            <div class="progress-preview">
              <div class="progress-text">
                <span>目前拼车进度</span>
                <span>{{ ride.purchase_count || 0 }} / {{ ride.total_seats }} 人</span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" :style="{ width: `${(occupiedSeats / ride.total_seats) * 100}%` }"></div>
              </div>
            </div>

            <label class="agreement-checkbox">
              <input v-model="termsAccepted" type="checkbox" />
              <span class="checkbox-text">我已知晓该笔服务费仅用于解锁车主联系账号，后续交易风险由本人承担。</span>
            </label>

            <button
              type="button"
              class="btn btn-primary action-btn-full"
              :disabled="unlockDisabled"
              @click="handleUnlock"
            >
              <CreditCard :size="16" />
              <span>{{ purchasing ? '正在生成订单并付款...' : unlockButtonText }}</span>
            </button>
            <p v-if="purchaseError" class="unlock-error-msg">{{ purchaseError }}</p>
          </div>
        </section>
      </div>
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
import type { ContactType, Ride } from '../types'

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
const individualCopied = ref<Record<number, boolean>>({})
const rideId = Number(route.params.id)
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt&backgroundColor=0f172a'

const copyIndividualContact = async (account: string, index: number) => {
  await navigator.clipboard.writeText(account)
  individualCopied.value[index] = true
  setTimeout(() => {
    individualCopied.value[index] = false
  }, 1800)
}

const loadRideDetails = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await ridesApi.getRide(rideId)
    ride.value = res.data
  } catch (err) {
    const errorVal = err as { response?: { data?: { detail?: string } } }
    error.value = errorVal.response?.data?.detail || '加载车位详情失败，请检查网络或车位是否已被删除'
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

const occupiedSeats = computed(() => Number(ride.value?.purchase_count || 0))

type ContactItem = {
  type: ContactType
  label: string
  icon: Component
  account: string
  note: string
  href: string
}

const contactMeta: Record<ContactType, { label: string; icon: Component }> = {
  email: { label: '电子邮箱', icon: Mail },
  wechat: { label: '微信账号', icon: MessageCircle },
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
  if (ride.value.status === 'closed') return '人数已满/关闭'
  if (ride.value.status === 'expired') return '车位已过期'
  return '接受解锁'
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
  if (isOwner.value) return '车主无需解锁'
  if (ride.value.status !== 'open') return '当前状态不可解锁'
  if ((ride.value.remaining_seats ?? 1) <= 0) return '车位已满'
  if (!userStore.isLoggedIn) return '登录并支付服务费'
  return '支付服务费解锁联系方式'
})

const unlockDisabled = computed(() => {
  return (
    purchasing.value ||
    (userStore.isLoggedIn && !termsAccepted.value) ||
    isOwner.value ||
    ride.value?.status !== 'open' ||
    (ride.value?.remaining_seats ?? 1) <= 0
  )
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
  } catch (err) {
    const errorVal = err as { response?: { data?: { detail?: string } } }
    purchaseError.value = errorVal.response?.data?.detail || '解锁联系方式失败，请稍后重试'
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
  grid-template-columns: 1fr 360px;
  gap: var(--spacing-xl);
  align-items: start;
}

.detail-main {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.detail-side {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  position: sticky;
  top: var(--spacing-md);
}

.listing-header,
.info-card,
.owner-card,
.unlock-card {
  padding: var(--spacing-lg) var(--spacing-xl);
}

.header-tags {
  display: flex;
  gap: 8px;
  margin-bottom: var(--spacing-md);
}

.ride-title {
  font-size: 28px;
  font-weight: 800;
  line-height: 1.3;
  letter-spacing: 0;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.ride-description {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: var(--spacing-sm);
  margin-top: var(--spacing-xl);
}

.metric-box {
  padding: 14px 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  text-align: center;
}

.metric-box.highlighted {
  border-color: var(--border-color-strong);
}

.metric-label {
  display: block;
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  text-transform: uppercase;
}

.metric-val {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
}

.metric-val small {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.highlight-green {
  color: var(--color-success);
}

.highlight-purple {
  color: var(--color-pro);
}

/* Specs layout */
.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
}

.section-icon {
  color: var(--text-muted);
}

.section-icon-safety {
  color: var(--color-warning);
}

.section-title h2 {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

.spec-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.spec-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.spec-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 600;
}

.spec-val {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 700;
}

/* Disclaimer text styles */
.disclaimer-card {
  border-color: rgba(245, 158, 11, 0.15);
}

.disclaimer-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.disclaimer-content p {
  font-size: 13px;
  line-height: 1.6;
  color: var(--color-warning);
  margin: 0;
}

/* Owner Side Card */
.owner-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.owner-meta {
  display: flex;
  flex-direction: column;
}

.owner-meta strong {
  font-size: 15px;
  font-weight: 800;
  color: var(--text-primary);
}

.badge {
  font-size: 11px;
  color: var(--color-success);
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.owner-stats {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 600;
  padding-top: var(--spacing-sm);
  border-top: 1px solid var(--border-color);
}

.owner-stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Unlock Card Styling */
.unlock-card {
  border-color: var(--border-color-strong);
}

.unlock-card.revealed {
  border-color: var(--border-color);
  background: var(--bg-secondary);
}

.unlock-header {
  display: flex;
  gap: var(--spacing-md);
  align-items: flex-start;
  margin-bottom: var(--spacing-lg);
}

.lock-indicator {
  display: inline-flex;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.lock-indicator.unlocked {
  background: var(--color-success-soft);
  color: var(--color-success);
}

.unlock-title-wrap h2 {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 2px;
}

.unlock-title-wrap p {
  font-size: 11px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0;
}

/* Pay and Locked Panel */
.locked-panel {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.unlock-cost-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.cost-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 600;
}

.cost-value {
  font-size: 20px;
  font-weight: 800;
  color: var(--color-pro);
}

.progress-preview {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 600;
}

.progress-bar-bg {
  height: 6px;
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: var(--color-success);
  border-radius: var(--border-radius-full);
}

.agreement-checkbox {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  cursor: pointer;
}

.agreement-checkbox input {
  margin-top: 3px;
}

.checkbox-text {
  font-size: 11px;
  line-height: 1.5;
  color: var(--text-secondary);
}

.action-btn-full {
  width: 100%;
  margin-top: var(--spacing-xs);
}

.unlock-error-msg {
  font-size: 11px;
  color: var(--color-danger);
  font-weight: 700;
  margin-top: -6px;
}

/* Revealed Panel Contacts */
.contact-panel {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.panel-title-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.contacts-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.contact-row-new {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--spacing-md);
  padding: 12px;
  border-radius: var(--border-radius-md);
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  transition: all var(--transition-fast);
}

.contact-row-new:hover {
  border-color: var(--border-color-strong);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}

/* Brand icon wrap colors */
.brand-logo-wrapper {
  width: 38px;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  flex-shrink: 0;
}

.brand-logo-wrapper.wechat {
  background: rgba(7, 193, 96, 0.08);
  color: #07c160;
}

.brand-logo-wrapper.telegram {
  background: rgba(38, 165, 228, 0.08);
  color: #26a5e4;
}

.brand-logo-wrapper.email {
  background: rgba(37, 99, 235, 0.08);
  color: #2563eb;
}

.brand-logo-svg {
  width: 22px;
  height: 22px;
}

.contact-details-wrap {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.contact-type-label {
  font-size: 10px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.account-link-container {
  display: flex;
  align-items: center;
}

.account-anchor {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  word-break: break-all;
}

.account-anchor:hover {
  color: var(--text-primary);
  text-decoration: underline;
}

.ext-icon {
  color: var(--text-muted);
  flex-shrink: 0;
}

.account-plain-text {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  word-break: break-all;
}

.contact-note-text {
  margin: 0;
  font-size: 11px;
  color: var(--text-secondary);
  font-style: italic;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Individual Copy Button */
.btn-copy-item {
  display: inline-flex;
  height: 28px;
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

.btn-copy-item:hover {
  background: var(--text-primary);
  color: var(--text-inverse);
  border-color: var(--text-primary);
}

@media (max-width: 1080px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  .detail-side {
    position: static;
  }
}

.chip-logo {
  width: 14px;
  height: 14px;
  object-fit: contain;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .metric-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .spec-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .listing-header,
  .info-card,
  .owner-card,
  .unlock-card {
    padding: var(--spacing-lg);
  }

  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .contact-row-new {
    grid-template-columns: 1fr;
    justify-items: start;
  }
}
</style>
