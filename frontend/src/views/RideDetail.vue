<template>
  <div class="detail-page container">
    <!-- Toast Notifications -->
    <Teleport to="body">
      <Transition name="toast">
        <div v-if="toast.visible" class="toast-bar" :class="toast.type">
          <component :is="toast.icon" :size="16" />
          <span>{{ toast.message }}</span>
        </div>
      </Transition>
    </Teleport>

    <!-- Skeleton Loading -->
    <div v-if="loading" class="skeleton-wrapper">
      <div class="skeleton-breadcrumb">
        <div class="skel skel-text skel-w80"></div>
      </div>
      <div class="detail-grid">
        <div class="detail-main">
          <section class="surface-card skel-card">
            <div class="skel skel-tags">
              <div class="skel skel-chip"></div>
              <div class="skel skel-chip skel-w60"></div>
            </div>
            <div class="skel skel-title"></div>
            <div class="skel skel-text skel-w100"></div>
            <div class="skel skel-text skel-w80"></div>
            <div class="skel-metric-grid">
              <div v-for="i in 5" :key="i" class="skel skel-metric-box"></div>
            </div>
          </section>
          <section class="surface-card skel-card">
            <div class="skel skel-text skel-w40 skel-mb16"></div>
            <div class="skel-spec-grid">
              <div v-for="i in 5" :key="i" class="skel skel-spec-item"></div>
            </div>
          </section>
          <section class="surface-card skel-card">
            <div class="skel skel-text skel-w50 skel-mb16"></div>
            <div class="skel skel-text skel-w100"></div>
            <div class="skel skel-text skel-w90"></div>
            <div class="skel skel-text skel-w70"></div>
          </section>
        </div>
        <div class="detail-side">
          <section class="surface-card skel-card">
            <div class="skel-owner">
              <div class="skel skel-avatar"></div>
              <div>
                <div class="skel skel-text skel-w80 skel-mb8"></div>
                <div class="skel skel-text skel-w60"></div>
              </div>
            </div>
          </section>
          <section class="surface-card skel-card skel-contact">
            <div class="skel skel-text skel-w60 skel-mb8"></div>
            <div class="skel skel-text skel-w100 skel-mb8"></div>
            <div class="skel skel-text skel-w80"></div>
          </section>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container surface-card anim-fade-up">
      <CircleAlert :size="38" class="error-icon" />
      <h3>详情获取失败</h3>
      <p>{{ error }}</p>
      <router-link to="/market" class="btn btn-primary">返回拼车市场</router-link>
    </div>

    <!-- Main Content -->
    <template v-else-if="ride">
      <!-- Breadcrumb Nav -->
      <nav class="breadcrumb anim-fade-up anim-d1">
        <router-link to="/market" class="breadcrumb-link">
          <ArrowLeft :size="14" />
          <span>拼车市场</span>
        </router-link>
        <ChevronRight :size="12" class="breadcrumb-sep" />
        <span class="breadcrumb-current">{{ ride.title }}</span>
      </nav>

      <div class="detail-grid">
        <div class="detail-main">
          <!-- Main Info Header -->
          <section class="listing-header surface-card anim-fade-up anim-d2">
            <div class="header-top-row">
              <div class="header-tags">
                <span class="product-chip" :class="ride.product">
                  <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                    <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
                  </svg>
                  <span>{{ productLabel }}</span>
                </span>
                <span class="status-chip" :class="ride.status">{{ statusLabel }}</span>
              </div>
              <button class="btn-icon" title="分享" @click="handleShare">
                <Share2 :size="16" />
              </button>
            </div>
            <h1 class="ride-title">{{ ride.title }}</h1>
            <p class="ride-description">
              {{ ride.description || '该车位主人比较神秘，暂未填写详细的公开说明。' }}
            </p>

            <div class="metric-grid">
              <div class="metric-box highlighted">
                <span class="metric-label">车位租金</span>
                <strong class="metric-val price-val">¥<span class="price-num">{{ formatMoney(ride.price_per_month) }}</span><small>/月</small></strong>
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
              <div class="metric-box warranty-metric">
                <span class="metric-label">质保天数</span>
                <strong class="metric-val highlight-info">{{ warrantyDays }}<small> 天</small></strong>
              </div>
            </div>
          </section>

          <!-- Specifications -->
          <section class="surface-card info-card anim-fade-up anim-d3">
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
                <span class="spec-label">质保承诺</span>
                <strong class="spec-val">{{ warrantyDays }} 天</strong>
              </div>
              <div class="spec-item">
                <span class="spec-label">车位总容量</span>
                <strong class="spec-val">{{ ride.total_seats }} 人位</strong>
              </div>
            </div>
          </section>

          <!-- Disclaimer -->
          <section class="surface-card info-card disclaimer-card anim-fade-up anim-d4">
            <div class="section-title" @click="disclaimerOpen = !disclaimerOpen" role="button" tabindex="0">
              <ShieldCheck :size="18" class="section-icon-safety" />
              <h2>服务边界与免责声明</h2>
              <ChevronDown :size="16" class="collapse-icon" :class="{ rotated: disclaimerOpen }" />
            </div>
            <Transition name="collapse">
              <div v-show="disclaimerOpen" class="disclaimer-content">
                <p>1. 平台仅提供共享信息的发布与展示服务，我们不组织拼车，亦无站内交谈渠道。</p>
                <p>2. 信息解锁服务费由平台收取引导对接，非拼车月租金，解锁后平台不介入后续交易。</p>
                <p>3. 拼车具有一定的线下风险，请添加车主后自行核实订阅账号的性质、周期及支付方式。</p>
              </div>
            </Transition>
          </section>
        </div>

        <!-- Sidebar Sticky Controls -->
        <div class="detail-side">
          <!-- Seller Info -->
          <section class="surface-card owner-card anim-fade-up anim-d3">
            <div class="owner-header">
              <div class="owner-avatar-wrap">
                <img :src="ride.owner?.avatar || defaultAvatar" alt="车主头像" class="owner-avatar" />
              </div>
              <div class="owner-meta">
                <strong>{{ ride.owner?.nickname || '认证车友' }}</strong>
                <span class="badge"><BadgeCheck :size="12" /> 车主已认证</span>
              </div>
            </div>
            <div class="owner-stats">
              <div class="owner-stat-item">
                <ReceiptText :size="14" />
                <span>当前车位已对接 {{ ride.purchase_count || 0 }} 次</span>
              </div>
            </div>
          </section>

          <!-- Contact Info Card -->
          <section class="surface-card contact-card anim-fade-up anim-d4">
            <div class="contact-header">
              <div class="contact-icon-wrap">
                <MessageCircle :size="20" />
              </div>
              <div>
                <h2>车主联系方式</h2>
                <p>添加车主后请自行沟通拼车细节。</p>
              </div>
            </div>

            <div v-if="contactItems.length" class="contact-panel">
              <div class="contacts-list">
                <div
                  v-for="(item, index) in contactItems"
                  :key="`${item.type}-${item.account}`"
                  class="contact-row-new"
                  :class="item.type"
                >
                  <div class="brand-logo-wrapper" :class="item.type">
                    <svg v-if="item.type === 'wechat'" viewBox="0 0 576 512" class="brand-logo-svg">
                      <path fill="currentColor" d="M385.2 167.6c6.4 0 12.6.3 18.8 1.1C387.4 90.3 303.3 32 207.7 32 100.5 32 13 104.8 13 197.4c0 53.4 29.3 97.5 77.9 131.6l-19.3 58.6 68-34.1c24.4 4.8 43.8 9.7 68.2 9.7 6.2 0 12.1-.3 18.3-.8-4-12.9-6.2-26.6-6.2-40.8-.1-84.9 72.9-154 165.3-154zm-104.5-52.9c14.5 0 24.2 9.7 24.2 24.4 0 14.5-9.7 24.2-24.2 24.2-14.8 0-29.3-9.7-29.3-24.2.1-14.7 14.6-24.4 29.3-24.4zm-136.4 48.6c-14.5 0-29.3-9.7-29.3-24.2 0-14.8 14.8-24.4 29.3-24.4 14.8 0 24.4 9.7 24.4 24.4 0 14.6-9.6 24.2-24.4 24.2zM563 319.4c0-77.9-77.9-141.3-165.4-141.3-92.7 0-165.4 63.4-165.4 141.3S305 460.7 397.6 460.7c19.3 0 38.9-5.1 58.6-9.9l53.4 29.3-14.8-48.6C534 402.1 563 363.2 563 319.4zm-219.1-24.5c-9.7 0-19.3-9.7-19.3-19.6 0-9.7 9.7-19.3 19.3-19.3 14.8 0 24.4 9.7 24.4 19.3 0 10-9.7 19.6-24.4 19.6zm107.1 0c-9.7 0-19.3-9.7-19.3-19.6 0-9.7 9.7-19.3 19.3-19.3 14.5 0 24.4 9.7 24.4 19.3.1 10-9.9 19.6-24.4 19.6z"/>
                    </svg>
                    <svg v-else-if="item.type === 'telegram'" viewBox="0 0 496 512" class="brand-logo-svg">
                      <path fill="currentColor" d="M248,8C111.033,8,0,119.033,0,256S111.033,504,248,504,496,392.967,496,256,384.967,8,248,8ZM362.952,176.66c-3.732,39.215-19.881,134.378-28.1,178.3-3.476,18.584-10.322,24.816-16.948,25.425-14.4,1.326-25.338-9.517-39.287-18.661-21.827-14.308-34.158-23.215-55.346-37.177-24.485-16.135-8.612-25,5.342-39.5,3.652-3.793,67.107-61.51,68.335-66.746.153-.655.3-3.1-1.154-4.384s-3.59-.849-5.135-.5q-3.283.746-104.608,69.142-14.845,10.194-26.894,9.934c-8.855-.191-25.888-5.006-38.551-9.123-15.531-5.048-27.875-7.717-26.8-16.291q.84-6.7,18.45-13.7,108.446-47.248,144.628-62.3c68.872-28.647,83.183-33.623,92.511-33.789,2.052-.034,6.639.474,9.61,2.885a10.452,10.452,0,0,1,3.53,6.716A43.765,43.765,0,0,1,362.952,176.66Z"/>
                    </svg>
                    <svg v-else-if="item.type === 'email'" viewBox="0 0 512 512" class="brand-logo-svg">
                      <path fill="currentColor" d="M48 96h416c26.5 0 48 21.5 48 48v224c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V144c0-26.5 21.5-48 48-48z"/>
                      <path fill="#ffffff" d="M460.6 156.4c5.1 6.2 4.1 15.4-2.2 20.4L280.7 319.1c-14.5 11.6-35 11.6-49.5 0L53.6 176.8c-6.3-5-7.3-14.2-2.2-20.4s14.2-7.3 20.4-2.2L249.5 296.5c3.8 3 9.2 3 13 0L440.2 154.2c6.2-5.1 15.4-4.1 20.4 2.2z"/>
                    </svg>
                    <Globe v-else-if="item.type === 'website'" :size="22" />
                  </div>
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
                  <button type="button" class="btn-copy-item" @click="copyIndividualContact(item.account, index)">
                    <Check v-if="individualCopied[index]" :size="12" class="copy-check" />
                    <Copy v-else :size="12" />
                    <span class="copy-text">{{ individualCopied[index] ? '已复制' : '复制' }}</span>
                  </button>
                </div>
              </div>
              <button type="button" class="btn btn-secondary action-btn-full" @click="copyContact">
                <Copy :size="16" />
                <span>{{ copied ? '已成功复制全部' : '复制全部联系方式' }}</span>
              </button>
            </div>

            <div v-else class="no-contact-hint">
              <p>车主暂未填写联系方式，请通过市场页面留言联系。</p>
            </div>
          </section>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowLeft,
  BadgeCheck,
  Check,
  ChevronDown,
  ChevronRight,
  CircleAlert,
  Copy,
  ExternalLink,
  FileText,
  Globe,
  Mail,
  MessageCircle,
  ReceiptText,
  SendHorizontal,
  Share2,
  ShieldCheck,
} from '@lucide/vue'
import type { Component } from 'vue'
import { ridesApi } from '../api/rides'
import type { ContactType, Ride } from '../types'

const route = useRoute()

const ride = ref<Ride | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const copied = ref(false)
const individualCopied = ref<Record<number, boolean>>({})
const disclaimerOpen = ref(true)
const rideId = Number(route.params.id)
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt&backgroundColor=0f172a'

// Toast system
const toast = reactive({
  visible: false,
  message: '',
  type: 'success' as 'success' | 'error' | 'info',
  icon: Check as Component,
  timer: 0,
})

function showToast(message: string, type: 'success' | 'error' | 'info' = 'success', icon: Component = Check) {
  toast.message = message
  toast.type = type
  toast.icon = icon
  toast.visible = true
  clearTimeout(toast.timer)
  toast.timer = window.setTimeout(() => {
    toast.visible = false
  }, 2500)
}

onMounted(loadRideDetails)

const copyIndividualContact = async (account: string, index: number) => {
  try {
    await navigator.clipboard.writeText(account)
    individualCopied.value[index] = true
    showToast('已复制到剪贴板', 'success')
    setTimeout(() => {
      individualCopied.value[index] = false
    }, 1800)
  } catch {
    showToast('复制失败，请手动选择复制', 'error')
  }
}

async function loadRideDetails() {
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
  website: { label: '个人网站', icon: Globe },
}

const normalizeTelegramHref = (account: string) => {
  const username = account.replace('https://t.me/', '').replace('http://t.me/', '').replace('@', '').trim()
  return username ? `https://t.me/${username}` : ''
}

const contactHref = (type: ContactType, account: string) => {
  if (type === 'email') return `mailto:${account}`
  if (type === 'telegram') return normalizeTelegramHref(account)
  if (type === 'website') return account
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

  addItem('website', ride.value?.contact_website)

  const extractByLabels = (labels: string[]) => {
    const labelPattern = labels.join('|')
    const nextLabelPattern = '邮箱|email|微信|wechat|telegram|电报|tg|个人网站|网站|website|site|url|备注|note'
    const pattern = new RegExp(`(?:^|\\n|\\s)(?:${labelPattern})\\s*[:：]\\s*([^\\n]+?)(?=\\s+(?:${nextLabelPattern})\\s*[:：]|$)`, 'i')
    return raw.match(pattern)?.[1]?.trim()
  }

  addItem('email', extractByLabels(['邮箱', 'email']))
  addItem('wechat', extractByLabels(['微信', 'wechat']))
  addItem('telegram', extractByLabels(['telegram', '电报', 'tg']))
  addItem('website', extractByLabels(['个人网站', '网站', 'website', 'site', 'url']))

  lines.forEach((line) => {
    const match = line.match(/^(邮箱|email|微信|wechat|telegram|电报|tg|个人网站|网站|website|site|url)\s*[:：]\s*(.+)$/i)
    if (!match) return
    const key = (match[1] || '').toLowerCase()
    const value = match[2] || ''
    if (key === '邮箱' || key === 'email') addItem('email', value)
    if (key === '微信' || key === 'wechat') addItem('wechat', value)
    if (key === 'telegram' || key === '电报' || key === 'tg') addItem('telegram', value)
    if (key === '个人网站' || key === '网站' || key === 'website' || key === 'site' || key === 'url') addItem('website', value)
  })

  const oldChannel = lines.find((line) => line.startsWith('联系渠道：'))?.replace('联系渠道：', '').trim()
  const oldAccount = lines.find((line) => line.startsWith('账号：'))?.replace('账号：', '').trim()
  if (oldChannel && oldAccount) {
    const lower = `${oldChannel} ${oldAccount}`.toLowerCase()
    if (lower.includes('telegram') || oldAccount.startsWith('@') || oldAccount.includes('t.me/')) addItem('telegram', oldAccount)
    else if (/^https?:\/\//i.test(oldAccount)) addItem('website', oldAccount)
    else if (lower.includes('邮箱') || lower.includes('email') || oldAccount.includes('@')) addItem('email', oldAccount)
    else addItem('wechat', oldAccount)
  }

  const emailMatch = raw.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)
  addItem('email', emailMatch?.[0])

  const telegramMatch = raw.match(/(?:https?:\/\/t\.me\/[-_a-zA-Z0-9]{5,32}|@[-_a-zA-Z0-9]{5,32})/)
  addItem('telegram', telegramMatch?.[0])

  const websiteMatch = raw.match(/https?:\/\/(?!t\.me\/)[^\s]+/i)
  addItem('website', websiteMatch?.[0])

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
  if (ride.value.status === 'closed') return '人数已满'
  if (ride.value.status === 'expired') return '已过期'
  return '招募中'
})

const warrantyDays = computed(() => {
  if (!ride.value) return 0
  return Number(ride.value.warranty_days || (ride.value.duration >= 12 ? 365 : ride.value.duration * 30))
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

const copyContact = async () => {
  const contactText = [ride.value?.contact_info, ride.value?.contact_website ? `个人网站：${ride.value.contact_website}` : ''].filter(Boolean).join('\n')
  if (!contactText) return
  try {
    await navigator.clipboard.writeText(contactText)
    copied.value = true
    showToast('全部联系方式已复制', 'success')
    setTimeout(() => {
      copied.value = false
    }, 1800)
  } catch {
    showToast('复制失败，请手动选择', 'error')
  }
}

const handleShare = async () => {
  const url = window.location.href
  const title = ride.value?.title || 'BusGPT 拼车'
  if (navigator.share) {
    try {
      await navigator.share({ title, url })
    } catch { /* user cancelled */ }
  } else {
    try {
      await navigator.clipboard.writeText(url)
      showToast('链接已复制到剪贴板', 'success')
    } catch {
      showToast('分享失败', 'error')
    }
  }
}

const formatMoney = (value: number | string) => Math.round(Number(value || 0))
</script>

<style scoped>
/* ===== Page Layout ===== */
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

/* ===== Animations ===== */
.anim-fade-up {
  animation: fadeUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.anim-d1 { animation-delay: 0.05s; }
.anim-d2 { animation-delay: 0.1s; }
.anim-d3 { animation-delay: 0.18s; }
.anim-d4 { animation-delay: 0.26s; }

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
.skeleton-wrapper {
  pointer-events: none;
}

.skel {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, var(--bg-inset) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--border-radius-sm);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skel-card {
  padding: var(--spacing-lg) var(--spacing-xl);
}

.skel-breadcrumb {
  margin-bottom: var(--spacing-sm);
}

.skel-tags {
  display: flex;
  gap: 8px;
  margin-bottom: var(--spacing-md);
}

.skel-chip {
  width: 90px;
  height: 24px;
  border-radius: var(--border-radius-full);
}

.skel-title {
  height: 32px;
  width: 70%;
  margin-bottom: var(--spacing-sm);
}

.skel-text {
  height: 14px;
  margin-bottom: 8px;
}

.skel-w40 { width: 40%; }
.skel-w50 { width: 50%; }
.skel-w60 { width: 60%; }
.skel-w70 { width: 70%; }
.skel-w80 { width: 80%; }
.skel-w90 { width: 90%; }
.skel-w100 { width: 100%; }
.skel-mb8 { margin-bottom: 8px; }
.skel-mb16 { margin-bottom: var(--spacing-md); }

.skel-metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-sm);
  margin-top: var(--spacing-xl);
}

.skel-metric-box {
  height: 72px;
  border-radius: var(--border-radius-md);
}

.skel-spec-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.skel-spec-item {
  height: 44px;
  border-radius: var(--border-radius-md);
}

.skel-owner {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.skel-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius-full);
  flex-shrink: 0;
}

.skel-contact {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.skel-btn {
  height: 44px;
  border-radius: var(--border-radius-md);
}

/* ===== Breadcrumb ===== */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-muted);
  padding: var(--spacing-xs) 0;
}

.breadcrumb-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transition-fast);
}

.breadcrumb-link:hover {
  color: var(--text-primary);
}

.breadcrumb-sep {
  color: var(--text-muted);
}

.breadcrumb-current {
  color: var(--text-primary);
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 280px;
}

/* ===== Listing Header ===== */
.listing-header,
.info-card,
.owner-card,
.unlock-card {
  padding: var(--spacing-lg) var(--spacing-xl);
}

.header-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.header-tags {
  display: flex;
  gap: 8px;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.btn-icon:hover {
  border-color: var(--border-color-strong);
  color: var(--text-primary);
  background: var(--bg-tertiary);
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

/* ===== Metric Grid ===== */
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
  transition: all var(--transition-fast);
  cursor: default;
}

.metric-box:hover {
  border-color: var(--border-color-strong);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.metric-box.highlighted {
  border-color: var(--border-color-strong);
  background: var(--bg-secondary);
}

.metric-box.warranty-metric {
  border-color: color-mix(in srgb, var(--color-info) 36%, transparent);
  background: color-mix(in srgb, var(--color-info) 12%, var(--bg-inset));
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
  transition: color var(--transition-fast);
}

.metric-val small {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.price-val {
  color: var(--text-primary);
}

.price-num {
  display: inline-block;
  transition: transform var(--transition-fast);
}

.metric-box:hover .price-num {
  transform: scale(1.05);
}

.highlight-green {
  color: var(--color-success);
}

.highlight-purple {
  color: var(--color-pro);
}

.highlight-info {
  color: var(--color-info);
}

/* ===== Specs ===== */
.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  user-select: none;
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
  flex: 1;
}

.collapse-icon {
  color: var(--text-muted);
  transition: transform var(--transition-fast);
  flex-shrink: 0;
}

.collapse-icon.rotated {
  transform: rotate(180deg);
}

.collapse-enter-active,
.collapse-leave-active {
  transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
  overflow: hidden;
}

.collapse-enter-from,
.collapse-leave-to {
  opacity: 0;
  max-height: 0;
  margin-top: 0;
  padding-top: 0;
}

.collapse-enter-to,
.collapse-leave-from {
  opacity: 1;
  max-height: 200px;
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
  transition: border-color var(--transition-fast);
}

.spec-item:hover {
  border-color: var(--border-color-strong);
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

/* ===== Disclaimer ===== */
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

/* ===== Owner Card ===== */
.owner-card {
  overflow: hidden;
}

.owner-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  min-width: 0;
}

.owner-avatar-wrap {
  display: inline-flex;
  width: 56px;
  height: 56px;
  flex: 0 0 56px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-full);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.owner-avatar {
  display: block;
  width: 100%;
  height: 100%;
  max-width: none;
  object-fit: cover;
}

.owner-meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
  gap: 4px;
}

.owner-meta strong {
  font-size: 15px;
  font-weight: 800;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.badge {
  font-size: 11px;
  color: var(--color-success);
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
  white-space: nowrap;
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
  min-width: 0;
}

.owner-stat-item span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ===== Contact Card ===== */
.contact-card {
  border-color: var(--border-color-strong);
}

.contact-header {
  display: flex;
  gap: var(--spacing-md);
  align-items: flex-start;
  margin-bottom: var(--spacing-lg);
}

.contact-icon-wrap {
  display: inline-flex;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: var(--color-success-soft);
  color: var(--color-success);
  flex-shrink: 0;
}

.contact-header h2 {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 2px;
}

.contact-header p {
  font-size: 11px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0;
}

.no-contact-hint {
  padding: var(--spacing-md);
  background: var(--bg-inset);
  border-radius: var(--border-radius-md);
  text-align: center;
}

.no-contact-hint p {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0;
}

.action-btn-full {
  width: 100%;
  margin-top: var(--spacing-xs);
}

/* ===== Contact Panel ===== */
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

.brand-logo-wrapper.website {
  background: var(--color-pro-soft);
  color: var(--color-pro);
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

.copy-check {
  color: var(--color-success);
}

/* ===== Toast ===== */
.toast-bar {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2000;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: var(--border-radius-full);
  font-size: 13px;
  font-weight: 700;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  white-space: nowrap;
}

.toast-bar.success {
  background: var(--color-success);
  color: #fff;
}

.toast-bar.error {
  background: var(--color-danger);
  color: #fff;
}

.toast-bar.info {
  background: var(--text-primary);
  color: var(--text-inverse);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-12px) scale(0.95);
}

/* ===== Responsive ===== */
@media (max-width: 1080px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
  .detail-side {
    position: static;
  }
}

@media (max-width: 768px) {
  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .spec-list {
    grid-template-columns: 1fr;
  }
  .ride-title {
    font-size: 22px;
  }
  .skel-metric-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .skel-spec-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .listing-header,
  .info-card,
  .owner-card,
  .contact-card {
    padding: var(--spacing-lg);
  }

  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .contact-row-new {
    grid-template-columns: 1fr;
    justify-items: start;
  }

  .breadcrumb-current {
    max-width: 160px;
  }
}

.chip-logo {
  width: 14px;
  height: 14px;
  object-fit: contain;
  flex-shrink: 0;
}
</style>
