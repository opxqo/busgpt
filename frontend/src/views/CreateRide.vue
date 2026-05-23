<template>
  <div class="create-page container">
    <header class="page-header">
      <div>
        <span class="eyebrow">发布商品</span>
        <h1 class="page-title">发布订阅车位</h1>
        <p class="page-subtitle">公开信息用于展示，联系方式会被隐藏，用户支付信息服务费后才能查看。</p>
      </div>
    </header>

    <div class="create-grid">
      <form class="create-form surface-card" @submit.prevent="handleSubmit">
        <section class="form-section">
          <div class="section-heading">
            <Package :size="18" />
            <h2>公开展示信息</h2>
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
              placeholder="例如：ChatGPT Plus 长期车位，空位稳定"
            />
          </div>

          <div class="form-group">
            <label class="form-label">订阅产品</label>
            <div class="product-grid">
              <button
                v-for="product in products"
                :key="product.type"
                type="button"
                class="product-option"
                :class="{ active: form.product === product.type, [product.type]: true }"
                @click="selectProduct(product)"
              >
                <span class="product-chip" :class="product.type">{{ product.label }}</span>
                <strong>${{ formatMoney(product.official_price) }}/月</strong>
                <small>最多 {{ product.max_seats }} 个名额</small>
                <p>{{ product.description }}</p>
              </button>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="total-seats">标注名额</label>
              <input id="total-seats" v-model.number="form.total_seats" class="form-control" type="number" :min="2" :max="maxSeatsAllowed" required />
              <span class="form-help">仅作为公开展示名额，不代表平台托管成员。</span>
            </div>
            <div class="form-group">
              <label class="form-label" for="duration">有效期</label>
              <select id="duration" v-model.number="form.duration" class="form-control" required>
                <option :value="1">1 个月</option>
                <option :value="3">3 个月</option>
                <option :value="6">6 个月</option>
                <option :value="12">12 个月</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" for="seat-price">车位月费</label>
              <input id="seat-price" v-model.number="form.price_per_month" class="form-control" type="number" min="1" required />
              <span class="form-help">展示给车友的每月参考分摊价格。</span>
            </div>
            <div class="form-group">
              <label class="form-label" for="contact-price">信息服务费</label>
              <input id="contact-price" v-model.number="form.contact_price" class="form-control" type="number" min="0" step="0.01" required />
              <span class="form-help">车友支付给平台后解锁联系方式。</span>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="description">公开说明</label>
            <textarea
              id="description"
              v-model.trim="form.description"
              class="form-control textarea-control"
              rows="4"
              placeholder="写清产品类型、车位周期、价格说明、适合人群。不要在这里填写联系方式。"
            ></textarea>
          </div>
        </section>

        <section class="form-section">
          <div class="section-heading">
            <LockKeyhole :size="18" />
            <h2>付费后可见信息</h2>
          </div>

          <div class="contact-list">
            <div
              v-for="method in contactMethods"
              :key="method.value"
              class="contact-editor"
              :class="method.value"
            >
              <div class="contact-editor__head">
                <span class="contact-icon">
                  <component :is="method.icon" :size="17" />
                </span>
                <div>
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
            <label class="form-label" for="contact-note">联系备注</label>
            <textarea
              id="contact-note"
              v-model.trim="form.contact_note"
              class="form-control textarea-control"
              rows="3"
              placeholder="例如：请备注 BusGPT / 晚上 8 点后回复 / 先确认席位周期。"
            ></textarea>
          </div>

          <label class="confirm-row">
            <input v-model="confirmed" type="checkbox" required />
            <span>我确认平台仅展示联系方式，不提供站内聊天、不代收订阅费用。</span>
          </label>
        </section>

        <button type="submit" class="btn btn-primary submit-btn" :disabled="submitting || !confirmed">
          <Send :size="16" />
          {{ submitting ? '发布中...' : '确认发布车位' }}
        </button>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
      </form>

      <aside class="preview-panel surface-card">
        <div class="section-heading">
          <ReceiptText :size="18" />
          <h2>发布预览</h2>
        </div>
        <div class="preview-card">
          <span class="product-chip" :class="form.product">{{ activeProductLabel }}</span>
          <h3>{{ form.title || '车位标题预览' }}</h3>
          <p>{{ form.description || '公开说明会显示在详情页和商品卡片中。' }}</p>
          <div class="preview-metrics">
            <div>
              <span>车位月费</span>
              <strong>¥{{ formatMoney(form.price_per_month) }}</strong>
            </div>
            <div>
              <span>服务费</span>
              <strong>¥{{ formatMoney(form.contact_price) }}</strong>
            </div>
            <div>
              <span>名额</span>
              <strong>{{ form.total_seats }} 个</strong>
            </div>
          </div>
        </div>
        <div class="service-note">
          <ShieldCheck :size="16" />
          <p>联系方式会在详情页锁定。用户完成模拟支付后，系统会创建已支付订单并展示该信息。</p>
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
    color: '#059669',
    max_seats: 4,
    description: '适合个人轻量使用',
  },
  {
    type: 'chatgpt-team',
    label: 'Team',
    official_price: 25,
    color: '#2563eb',
    max_seats: 10,
    description: '适合稳定协作席位',
  },
  {
    type: 'chatgpt-pro',
    label: 'Pro',
    official_price: 200,
    color: '#d97706',
    max_seats: 5,
    description: '高阶需求与重度使用',
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
    label: '微信',
    icon: MessageCircle,
    placeholder: '例如：busgpt_owner',
    help: '适合国内沟通，建议填写微信号而不是昵称。',
  },
  {
    value: 'email' as ContactType,
    label: '邮箱',
    icon: Mail,
    placeholder: '例如：owner@example.com',
    help: '适合异步确认订阅周期、付款方式和账号规则。',
  },
  {
    value: 'telegram' as ContactType,
    label: 'Telegram',
    icon: SendHorizontal,
    placeholder: '例如：@busgpt_owner 或 https://t.me/busgpt_owner',
    help: '适合跨区沟通，可以填写用户名或 t.me 链接。',
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

  if (!email && !wechat && !telegram) return '请至少填写一种联系方式'
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return '请填写有效的邮箱地址'
  if (wechat && !/^[a-zA-Z][-_a-zA-Z0-9]{5,19}$/.test(wechat)) return '请填写有效的微信号'
  if (telegram && !/^(@?[-_a-zA-Z0-9]{5,32}|https:\/\/t\.me\/[-_a-zA-Z0-9]{5,32})$/.test(telegram)) return '请填写有效的 Telegram 用户名或链接'
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
  } catch (err: any) {
    errorMsg.value = err.response?.data?.detail || '发布失败，请检查填写内容'
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

.create-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 340px;
  gap: var(--spacing-lg);
  align-items: start;
}

.create-form,
.preview-panel {
  padding: var(--spacing-lg);
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
  margin-bottom: var(--spacing-lg);
}

.section-heading h2 {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 900;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-sm);
}

.product-option {
  display: flex;
  min-height: 150px;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  padding: 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  text-align: left;
  transition: border-color var(--transition-fast), background-color var(--transition-fast);
}

.product-option.active {
  border-color: var(--color-primary);
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
}

.product-option strong {
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 900;
}

.product-option small,
.product-option p {
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.5;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.contact-list {
  display: grid;
  gap: 12px;
  margin-bottom: var(--spacing-lg);
}

.contact-editor {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.contact-editor__head {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 10px;
  align-items: center;
}

.contact-icon {
  display: inline-flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
}

.contact-editor.email .contact-icon {
  background: #fef2f2;
  color: #dc2626;
}

.contact-editor.wechat .contact-icon {
  background: #e9f9ee;
  color: #07c160;
}

.contact-editor.telegram .contact-icon {
  background: #e8f5ff;
  color: #229ed9;
}

.contact-editor__head strong {
  display: block;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 900;
}

.contact-editor__head span:not(.contact-icon) {
  display: block;
  margin-top: 2px;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.5;
}

.textarea-control {
  min-height: 112px;
  resize: vertical;
}

.confirm-row {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
  align-items: start;
  padding: 12px;
  border-radius: var(--border-radius-md);
  background: var(--color-warning-soft);
  color: #7c4a00;
  font-size: 13px;
  line-height: 1.6;
}

.submit-btn {
  width: 100%;
  margin-top: var(--spacing-xl);
}

.error-msg {
  margin-top: var(--spacing-md);
  color: var(--color-danger);
  font-size: 13px;
  font-weight: 800;
  text-align: center;
}

.preview-panel {
  position: sticky;
  top: var(--spacing-lg);
}

.preview-card {
  padding: 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.preview-card h3 {
  margin: 12px 0 8px;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 900;
  line-height: 1.4;
}

.preview-card p {
  min-height: 42px;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

.preview-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  margin-top: var(--spacing-md);
}

.preview-metrics div {
  padding: 10px;
  border-radius: var(--border-radius-md);
  background: var(--bg-secondary);
}

.preview-metrics span {
  display: block;
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 800;
}

.preview-metrics strong {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 900;
}

.service-note {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px;
  margin-top: var(--spacing-md);
  padding: 12px;
  border-radius: var(--border-radius-md);
  background: var(--color-info-soft);
  color: #315a78;
  font-size: 13px;
  line-height: 1.6;
}

@media (max-width: 1040px) {
  .create-grid {
    grid-template-columns: 1fr;
  }

  .preview-panel {
    position: static;
  }
}

@media (max-width: 700px) {
  .product-grid,
  .form-row,
  .preview-metrics {
    grid-template-columns: 1fr;
  }
}
</style>
