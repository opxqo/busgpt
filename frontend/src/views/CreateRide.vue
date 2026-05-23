<template>
  <div class="create-page container">
    <!-- Header -->
    <header class="page-header">
      <div class="header-info">
        <span class="eyebrow">发布共享</span>
        <h1 class="page-title">发布订阅车位</h1>
        <p class="page-subtitle">填写真实的共享车位，设置合理的分摊月费与解锁费，吸纳长期稳定的车友搭伙。</p>
      </div>
    </header>

    <div class="create-grid">
      <!-- Form Area -->
      <form class="create-form surface-card" @submit.prevent="handleSubmit">
        <!-- Section 1: Public Info -->
        <section class="form-section">
          <div class="section-heading">
            <Package :size="18" class="heading-icon" />
            <h2>1. 公开展示信息</h2>
          </div>

          <div class="form-group">
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
                  <span class="product-badge" :class="product.type">{{ product.label }}</span>
                  <span class="seats-limit">限额 {{ product.max_seats }} 人</span>
                </div>
                <strong class="official-cost">${{ formatMoney(product.official_price) }}<small>/月</small></strong>
                <p class="product-desc">{{ product.description }}</p>
              </button>
            </div>
          </div>

          <div class="form-row-2">
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
          </div>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label" for="seat-price">分摊月费 (¥)</label>
              <input id="seat-price" v-model.number="form.price_per_month" class="form-control" type="number" min="1" required />
              <span class="form-help">每位车友每月需支付给您的订阅分摊。</span>
            </div>
            <div class="form-group">
              <label class="form-label" for="contact-price">信息解锁服务费 (¥)</label>
              <input id="contact-price" v-model.number="form.contact_price" class="form-control" type="number" min="0" step="0.01" required />
              <span class="form-help">车友解锁联系方式需支付的服务费。</span>
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
            <LockKeyhole :size="18" class="heading-icon-locked" />
            <h2>2. 付费解锁后可见信息</h2>
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
                :type="method.value === 'email' ? 'email' : 'text'"
                :placeholder="method.placeholder"
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="contact-note">解锁备注信息</label>
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
                <span class="product-chip" :class="form.product">{{ activeProductLabel }} 拼车</span>
                <span class="status-chip open">可解锁</span>
              </div>
              <h3 class="sim-title">{{ form.title || '这里会展示您填写的标题' }}</h3>
              <p class="sim-desc">{{ form.description || '这里会展示公开的拼车规则说明...' }}</p>

              <div class="sim-price-row">
                <div class="sim-price-item">
                  <span class="sim-label">车位租金</span>
                  <strong class="sim-val">¥{{ formatMoney(form.price_per_month) }}<small>/月</small></strong>
                </div>
                <div class="sim-divider"></div>
                <div class="sim-price-item text-right">
                  <span class="sim-label">解锁费用</span>
                  <strong class="sim-val val-purple">¥{{ formatMoney(form.contact_price) }}</strong>
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
            <p>车位发布后将进入拼车市场。乘客需支付您设定的“信息服务费”以解锁联系方式，解锁后乘客会与您直接沟通。</p>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import type { Component } from 'vue'
import { useRouter } from 'vue-router'
import { LockKeyhole, Mail, MessageCircle, Package, ReceiptText, Send, SendHorizontal, ShieldCheck } from '@lucide/vue'
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
    description: 'GPT-4o、高级语音、个人首选',
  },
  {
    type: 'chatgpt-team',
    label: 'Team',
    official_price: 25,
    color: '#3b82f6',
    max_seats: 10,
    description: '高限额、团队专用协作拼车',
  },
  {
    type: 'chatgpt-pro',
    label: 'Pro',
    official_price: 200,
    color: '#8b5cf6',
    max_seats: 5,
    description: '无限制 o1-pro 模型极客最爱',
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
  description: '',
  contacts: {
    email: '',
    wechat: '',
    telegram: '',
  } as Record<ContactType, string>,
  contact_note: '',
  contact_price: 9.9,
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

  if (!email && !wechat && !telegram) return '请至少填写一种隐藏的联系方式'
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return '请填写有效的邮箱地址'
  if (wechat && !/^[a-zA-Z][-_a-zA-Z0-9]{5,19}$/.test(wechat)) return '请填写正确的微信号格式'
  if (telegram && !/^(@?[-_a-zA-Z0-9]{5,32}|https:\/\/t\.me\/[-_a-zA-Z0-9]{5,32})$/.test(telegram)) return '请填写有效的 Telegram 用户名'
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
      description: form.description,
      contact_info: contactInfoPayload.value,
      contact_price: form.contact_price,
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
  padding: var(--spacing-xl);
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-section + .form-section {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-xl);
  border-top: 1px solid var(--border-color);
}

.section-heading {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: var(--spacing-sm);
}

.heading-icon {
  color: var(--text-muted);
}

.heading-icon-locked {
  color: var(--color-pro);
}

.heading-icon-preview {
  color: var(--color-team);
}

.section-heading h2 {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

/* Product selections */
.product-selection-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-sm);
}

.product-option-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  padding: var(--spacing-md);
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
}

.product-option-card.active {
  background: var(--bg-secondary);
  border-width: 2px;
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
}

.product-badge {
  font-size: 10px;
  font-weight: 800;
}

.seats-limit {
  font-size: 10px;
  color: var(--text-secondary);
  font-weight: 600;
}

.official-cost {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-primary);
}

.official-cost small {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
}

.product-desc {
  font-size: 11px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.4;
}

.form-row-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
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
  color: #854d0e;
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
}

.sim-price-item {
  display: flex;
  flex-direction: column;
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
}

.sim-val small {
  font-size: 10px;
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
  border: 1px solid rgba(6, 182, 212, 0.15);
  color: #0e7490;
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
  .product-selection-grid {
    grid-template-columns: 1fr;
  }
  .form-row-2 {
    grid-template-columns: 1fr;
    gap: 0;
  }
}
</style>
