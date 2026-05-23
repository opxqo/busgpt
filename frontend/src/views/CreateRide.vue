<template>
  <div class="create-page container">
    <!-- Header -->
    <header class="page-header">
      <div class="header-info">
        <span class="eyebrow">发布共享</span>
        <h1 class="page-title">发布订阅车位</h1>
        <p class="page-subtitle">填写真实的共享车位，设置合理的分摊月费，吸纳长期稳定的车友搭伙。</p>
      </div>
    </header>

    <div class="create-grid">
      <!-- Form Area -->
      <form class="create-form surface-card" @submit.prevent="handleSubmit">
        <!-- Section 1: Public Info -->
        <section class="form-section">
          <div class="section-heading">
            <span class="section-index">1</span>
            <Package :size="18" class="heading-icon" />
            <div class="section-heading-copy">
              <h2>公开展示信息</h2>
              <p>这些内容会出现在市场卡片和详情页，用于帮助车友快速判断车位是否合适。</p>
            </div>
          </div>

          <div class="form-group form-group-title">
            <label class="form-label" for="title">车位标题</label>
            <input
              id="title"
              v-model.trim="form.title"
              class="form-control"
              type="text"
              required
              maxlength="100"
              placeholder="例如：ChatGPT Plus 独享车位，空位稳定速来"
            />
          </div>

          <div class="form-group">
            <label class="form-label">订阅产品类型</label>
            <div class="product-selection-grid">
              <button
                v-for="product in products"
                :key="product.type"
                type="button"
                class="product-option-card"
                :class="{ active: form.product === product.type, [product.type]: true }"
                @click="selectProduct(product)"
              >
                <div class="card-top-row">
                  <span class="product-badge" :class="product.type">
                    <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                      <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
                    </svg>
                    <span>{{ product.label }}</span>
                  </span>
                  <span class="seats-limit">限额 {{ product.max_seats }} 人</span>
                </div>
                <strong class="official-cost">${{ formatMoney(product.official_price) }}<small>/月</small></strong>
                <p class="product-desc">{{ product.description }}</p>
              </button>
            </div>
          </div>

          <div class="form-row-3">
            <div class="form-group">
              <label class="form-label" for="total-seats">车位可容纳总人数</label>
              <input
                id="total-seats"
                v-model.number="form.total_seats"
                class="form-control"
                type="number"
                :min="2"
                :max="maxSeatsAllowed"
                required
              />
              <span class="form-help">该车位包含车主本人的总拼车位数。</span>
            </div>
            <div class="form-group">
              <label class="form-label" for="duration">车位有效期限</label>
              <div class="select-wrapper">
                <select id="duration" v-model.number="form.duration" class="form-control" required>
                  <option :value="1">1 个月</option>
                  <option :value="3">3 个月</option>
                  <option :value="6">6 个月</option>
                  <option :value="12">12 个月</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" for="seat-price">分摊月费 (¥)</label>
              <input id="seat-price" v-model.number="form.price_per_month" class="form-control" type="number" min="1" required />
              <span class="form-help">每位车友每月需支付给您的订阅分摊。</span>
            </div>
            <div class="form-group">
              <label class="form-label" for="warranty-days">质保天数</label>
              <input
                id="warranty-days"
                v-model.number="form.warranty_days"
                class="form-control"
                type="number"
                min="1"
                max="730"
                required
              />
              <span class="form-help">保障可用天数，同步展示在市场卡片和详情页。</span>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="description">详细拼车说明</label>
            <textarea
              id="description"
              v-model.trim="form.description"
              class="form-control textarea-control"
              rows="4"
              placeholder="请明确写清拼车规则、使用频率要求、续费方式及适合人群，请勿在此透露联系方式。"
            ></textarea>
          </div>
        </section>

        <!-- Section 2: Contact Info -->
        <section class="form-section">
          <div class="section-heading">
            <span class="section-index">2</span>
            <MessageCircle :size="18" class="heading-icon-contact" />
            <div class="section-heading-copy">
              <h2>联系方式信息</h2>
              <p>联系方式不会作为公开说明展示，用于车友确认后继续沟通拼车细节。</p>
            </div>
          </div>

          <div class="contacts-form-list">
            <div
              v-for="method in contactMethods"
              :key="method.value"
              class="contact-input-box"
              :class="method.value"
            >
              <div class="input-box-header">
                <div class="method-icon-wrap">
                  <component :is="method.icon" :size="16" />
                </div>
                <div class="method-meta">
                  <strong>{{ method.label }}</strong>
                  <span>{{ method.help }}</span>
                </div>
              </div>
              <input
                v-model.trim="form.contacts[method.value]"
                class="form-control"
                :type="method.value === 'email' ? 'email' : method.value === 'website' ? 'url' : 'text'"
                :placeholder="method.placeholder"
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="contact-note">备注信息</label>
            <textarea
              id="contact-note"
              v-model.trim="form.contact_note"
              class="form-control textarea-control"
              rows="3"
              placeholder="例如：添加好友请备注“BusGPT拼车”，收到后会在晚上统一处理。"
            ></textarea>
          </div>

          <label class="agreement-checkbox">
            <input v-model="confirmed" type="checkbox" required />
            <span class="checkbox-text">我保证填写的内容均真实准确，并自愿遵守信息共享平台规范。</span>
          </label>
        </section>

        <button type="submit" class="btn btn-primary submit-btn" :disabled="submitting || !confirmed">
          <Send :size="16" />
          <span>{{ submitting ? '正在创建并发布车位...' : '立即确认并发布' }}</span>
        </button>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
      </form>

      <!-- Preview Column (Sticky) -->
      <aside class="preview-column">
        <div class="preview-sticky">
          <div class="section-heading">
            <ReceiptText :size="18" class="heading-icon-preview" />
            <h2>实时效果预览</h2>
          </div>
          <div class="preview-card-wrapper">
            <!-- Simulated Ride Card -->
            <article class="simulated-card">
              <div class="sim-header">
                <span class="product-chip" :class="form.product">
                  <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
                    <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
                  </svg>
                  <span>{{ activeProductLabel }} 拼车</span>
                </span>
                <span class="status-chip open">招募中</span>
              </div>
              <h3 class="sim-title">{{ form.title || '这里会展示您填写的标题' }}</h3>
              <p class="sim-desc">{{ form.description || '这里会展示公开的拼车规则说明...' }}</p>

              <div class="sim-price-row">
                <div class="sim-price-item">
                  <span class="sim-label">车位租金</span>
                  <strong class="sim-val">¥{{ formatMoney(form.price_per_month) }}<small>/月</small></strong>
                </div>
                <span class="sim-price-divider" :class="form.product" aria-hidden="true"></span>
                <div class="sim-price-item sim-guarantee-item">
                  <span class="sim-label">质保天数</span>
                  <strong class="sim-val sim-guarantee-val" :class="form.product">{{ form.warranty_days }}<small>天</small></strong>
                </div>
              </div>

              <div class="sim-footer">
                <div class="sim-facts">
                  <span>已拼 0/{{ form.total_seats }} 人</span>
                  <span>{{ form.duration }}个月有效期</span>
                </div>
              </div>
            </article>
          </div>
          <div class="preview-info-box">
            <ShieldCheck :size="16" class="safety-icon" />
            <p>车位发布后将进入拼车市场，车友可直接查看您的联系方式并与您沟通拼车细节。</p>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import type { Component } from 'vue'
import { useRouter } from 'vue-router'
import { Globe, Mail, MessageCircle, Package, ReceiptText, Send, SendHorizontal, ShieldCheck } from '@lucide/vue'
import { ridesApi } from '../api/rides'
import type { ContactType, Product, ProductType } from '../types'

const router = useRouter()
const submitting = ref(false)
const errorMsg = ref<string | null>(null)
const confirmed = ref(false)

const products = ref<Product[]>([
  {
    type: 'chatgpt-plus',
    label: 'Plus',
    official_price: 20,
    color: '#10b981',
    max_seats: 4,
    description: 'GPT-5.5、深度研究、Agent 与 Codex',
  },
  {
    type: 'chatgpt-team',
    label: 'Business',
    official_price: 25,
    color: '#3b82f6',
    max_seats: 10,
    description: 'Plus 能力、团队工作区、连接器与管理',
  },
  {
    type: 'chatgpt-pro',
    label: 'Pro',
    official_price: 200,
    color: '#8b5cf6',
    max_seats: 5,
    description: '最高用量、GPT-5.5 Pro、扩展深度研究',
  },
])

type ContactMethod = {
  value: ContactType
  label: string
  icon: Component
  placeholder: string
  help: string
}

const form = reactive({
  title: '',
  product: 'chatgpt-plus' as ProductType,
  total_seats: 4,
  price_per_month: 35,
  duration: 3,
  warranty_days: 90,
  description: '',
  contacts: {
    email: '',
    wechat: '',
    telegram: '',
    website: '',
  } as Record<ContactType, string>,
  contact_note: '',
})

const contactMethods: ContactMethod[] = [
  {
    value: 'wechat' as ContactType,
    label: '微信账号',
    icon: MessageCircle,
    placeholder: '例如：wechat_account',
    help: '最常用的联系渠道。请准确填写微信号。',
  },
  {
    value: 'email' as ContactType,
    label: '电子邮箱',
    icon: Mail,
    placeholder: '例如：owner@example.com',
    help: '适合异步沟通及账号规则确认。',
  },
  {
    value: 'telegram' as ContactType,
    label: 'Telegram ID',
    icon: SendHorizontal,
    placeholder: '例如：@username 或 https://t.me/username',
    help: '适合跨境车友沟通。可填用户名或直达链接。',
  },
  {
    value: 'website' as ContactType,
    label: '个人网站',
    icon: Globe,
    placeholder: '例如：https://example.com',
    help: '可填写个人主页、作品集或可信资料页。',
  },
]

onMounted(async () => {
  try {
    const res = await ridesApi.getProducts()
    if (res.data?.length) {
      products.value = res.data
    }
  } catch (err) {
    console.error('Failed to load products', err)
  }
})

const activeProductObj = computed(() => {
  return products.value.find((product) => product.type === form.product) || products.value[0]
})

const durationToWarrantyDays = (duration: number) => (duration >= 12 ? 365 : duration * 30)
const activeProductLabel = computed(() => activeProductObj.value?.label || 'Plus')
const maxSeatsAllowed = computed(() => activeProductObj.value?.max_seats || 4)
const contactInfoPayload = computed(() => {
  const lines = contactMethods
    .map((method) => {
      const account = form.contacts[method.value].trim()
      return account ? `${method.label}：${account}` : ''
    })
    .filter(Boolean)
  if (form.contact_note) lines.push(`备注：${form.contact_note}`)
  return lines.join('\n')
})

watch(
  () => form.duration,
  (duration) => {
    form.warranty_days = durationToWarrantyDays(duration)
  }
)

const selectProduct = (product: Product) => {
  form.product = product.type
  form.total_seats = product.max_seats
  if (product.type === 'chatgpt-plus') form.price_per_month = 35
  if (product.type === 'chatgpt-team') form.price_per_month = 28
  if (product.type === 'chatgpt-pro') form.price_per_month = 90
}

const validateContact = () => {
  const email = form.contacts.email.trim()
  const wechat = form.contacts.wechat.trim()
  const telegram = form.contacts.telegram.trim()
  const website = form.contacts.website.trim()

  if (!email && !wechat && !telegram && !website) return '请至少填写一种隐藏的联系方式'
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return '请填写有效的邮箱地址'
  if (wechat && !/^[a-zA-Z][-_a-zA-Z0-9]{5,19}$/.test(wechat)) return '请填写正确的微信号格式'
  if (telegram && !/^(@?[-_a-zA-Z0-9]{5,32}|https:\/\/t\.me\/[-_a-zA-Z0-9]{5,32})$/.test(telegram)) return '请填写有效的 Telegram 用户名'
  if (website && !/^https?:\/\/[^\s.]+\.[^\s]+$/i.test(website)) return '请填写以 http:// 或 https:// 开头的个人网站地址'
  return ''
}

const handleSubmit = async () => {
  const contactError = validateContact()
  if (contactError) {
    errorMsg.value = contactError
    return
  }
  submitting.value = true
  errorMsg.value = null
  try {
    const res = await ridesApi.createRide({
      title: form.title,
      product: form.product,
      total_seats: form.total_seats,
      price_per_month: form.price_per_month,
      duration: form.duration,
      warranty_days: form.warranty_days,
      description: form.description,
      contact_info: contactInfoPayload.value,
      contact_website: form.contacts.website.trim(),
      contact_price: 0,
    })
    router.push(`/ride/${res.data.id}`)
  } catch (err) {
    const error = err as { response?: { data?: { detail?: string } } }
    errorMsg.value = error.response?.data?.detail || '发布失败，请检查填写参数'
  } finally {
    submitting.value = false
  }
}

const formatMoney = (value: number | string) => Math.round(Number(value || 0))
</script>

<style scoped>
.create-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.page-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: var(--spacing-lg);
}

.create-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: var(--spacing-xl);
  align-items: start;
}

.create-form {
  padding: 0;
  overflow: hidden;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 28px 32px 32px;
}

.form-section + .form-section {
  margin-top: 0;
  padding-top: 28px;
  border-top: 1px solid var(--border-color);
}

.section-heading {
  display: grid;
  grid-template-columns: auto auto minmax(0, 1fr);
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 2px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.section-index {
  display: inline-flex;
  width: 24px;
  height: 24px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-full);
  background: var(--color-primary);
  color: var(--text-inverse);
  font-size: 12px;
  font-weight: 800;
  line-height: 1;
}

.heading-icon {
  margin-top: 3px;
  color: var(--text-muted);
}

.heading-icon-contact {
  margin-top: 3px;
  color: var(--color-success);
}

.heading-icon-preview {
  color: var(--color-team);
}

.section-heading-copy {
  min-width: 0;
}

.section-heading h2 {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

.section-heading p {
  margin: 5px 0 0;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.5;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.form-group-title {
  padding-top: 2px;
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

.form-help {
  color: var(--text-muted);
  font-size: 11px;
  line-height: 1.45;
}

.form-control {
  min-height: 44px;
}

/* Product selections */
.product-selection-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.product-option-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  min-height: 128px;
  padding: 14px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  text-align: left;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.product-option-card:hover {
  border-color: var(--border-color-strong);
  background: var(--bg-secondary);
  transform: translateY(-1px);
}

.product-option-card.active {
  background: var(--bg-secondary);
  border-width: 1px;
}

.product-option-card.chatgpt-plus.active {
  border-color: var(--color-plus);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.product-option-card.chatgpt-team.active {
  border-color: var(--color-team);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.product-option-card.chatgpt-pro.active {
  border-color: var(--color-pro);
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.card-top-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
  align-items: center;
  gap: 10px;
}

.product-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  min-width: 0;
  color: var(--text-secondary);
  font-size: 10px;
  font-weight: 800;
  line-height: 1.2;
}

.product-option-card.active .product-badge.chatgpt-plus {
  color: var(--color-plus);
}

.product-option-card.active .product-badge.chatgpt-team {
  color: var(--color-team);
}

.product-option-card.active .product-badge.chatgpt-pro {
  color: var(--color-pro);
}

.product-badge .chip-logo {
  width: 14px;
  height: 14px;
  color: currentColor;
  opacity: 0.95;
}

.seats-limit {
  font-size: 10px;
  color: var(--text-muted);
  font-weight: 600;
  white-space: nowrap;
}

.product-option-card.active .seats-limit,
.product-option-card:hover .seats-limit {
  color: var(--text-secondary);
}

.official-cost {
  margin-top: 2px;
  font-size: 18px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1;
}

.official-cost small {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.product-desc {
  font-size: 11px;
  color: var(--text-secondary);
  display: -webkit-box;
  flex: 1;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  margin: 0;
  line-height: 1.45;
}

.form-row-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.form-row-3 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: 16px;
  row-gap: 18px;
}

.textarea-control {
  min-height: 112px;
  resize: vertical;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23475569' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 32px;
}

/* Contacts boxes */
.contacts-form-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.contact-input-box {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.input-box-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.method-icon-wrap {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.contact-input-box.wechat .method-icon-wrap {
  background: #dcfce7;
  color: #15803d;
}

.contact-input-box.email .method-icon-wrap {
  background: #fee2e2;
  color: #b91c1c;
}

.contact-input-box.telegram .method-icon-wrap {
  background: #e0f2fe;
  color: #0369a1;
}

.contact-input-box.website .method-icon-wrap {
  background: var(--color-pro-soft);
  color: var(--color-pro);
}

.method-meta {
  display: flex;
  flex-direction: column;
}

.method-meta strong {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.method-meta span {
  font-size: 11px;
  color: var(--text-muted);
}

.agreement-checkbox {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  margin-top: var(--spacing-md);
  cursor: pointer;
}

.agreement-checkbox input {
  margin-top: 3px;
}

.checkbox-text {
  font-size: 12px;
  color: var(--color-warning);
  line-height: 1.5;
}

.submit-btn {
  width: 100%;
  margin-top: var(--spacing-lg);
}

.error-msg {
  color: var(--color-danger);
  font-size: 13px;
  font-weight: 700;
  text-align: center;
  margin-top: var(--spacing-sm);
}

/* Preview column */
.preview-column {
  position: sticky;
  top: var(--spacing-md);
}

.preview-sticky {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.preview-card-wrapper {
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--card-shadow);
}

/* Simulated Ride Card */
.simulated-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color-strong);
  border-radius: var(--border-radius-md);
}

.sim-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sim-title {
  font-size: 15px;
  font-weight: 800;
  color: var(--text-primary);
  margin: var(--spacing-xs) 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sim-desc {
  font-size: 12px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 36px;
}

.sim-price-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.sim-price-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}

.sim-guarantee-item {
  align-items: flex-end;
}

.sim-price-divider {
  width: 3px;
  height: 24px;
  align-self: center;
  border-radius: var(--border-radius-full);
  background: var(--color-plus);
}

.sim-price-divider.chatgpt-team {
  background: var(--color-team);
}

.sim-price-divider.chatgpt-pro {
  background: var(--color-pro);
}

.sim-label {
  font-size: 9px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
}

.sim-val {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.1;
}

.sim-val small {
  font-size: 10px;
  margin-left: 1px;
  color: currentColor;
}

.sim-guarantee-val {
  color: var(--color-plus);
}

.sim-guarantee-val.chatgpt-team {
  color: var(--color-team);
}

.sim-guarantee-val.chatgpt-pro {
  color: var(--color-pro);
}

.val-purple {
  color: var(--color-pro);
}

.sim-divider {
  width: 1px;
  height: 20px;
  background: var(--border-color);
}

.sim-footer {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 600;
  border-top: 1px dashed var(--border-color);
  padding-top: var(--spacing-sm);
}

.sim-facts {
  display: flex;
  justify-content: space-between;
}

.preview-info-box {
  display: flex;
  gap: 8px;
  padding: 12px;
  border-radius: var(--border-radius-md);
  background: var(--color-info-soft);
  border: 1px solid var(--border-color);
  color: var(--color-info);
}

.safety-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.preview-info-box p {
  font-size: 11px;
  line-height: 1.5;
  margin: 0;
}

@media (max-width: 1080px) {
  .create-grid {
    grid-template-columns: 1fr;
  }
  .preview-column {
    position: static;
  }
}

@media (max-width: 700px) {
  .create-form {
    padding: var(--spacing-lg);
  }
  .product-selection-grid {
    grid-template-columns: 1fr;
  }
  .form-row-2 {
    grid-template-columns: 1fr;
    gap: 0;
  }
  .form-row-3 {
    grid-template-columns: 1fr;
  }
}

.chip-logo {
  width: 14px;
  height: 14px;
  object-fit: contain;
  flex-shrink: 0;
}
</style>
