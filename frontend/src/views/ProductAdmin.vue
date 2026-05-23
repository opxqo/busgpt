<template>
  <div class="products-page container">
    <header class="page-header surface-card">
      <div>
        <span class="eyebrow">产品维护</span>
        <h1 class="page-title">订阅产品信息</h1>
        <p class="page-subtitle">维护市场里可发布的产品档位、官方价格、最大拼车人数和展示说明。</p>
      </div>
      <button type="button" class="btn btn-secondary" :disabled="loading" @click="loadProducts">
        <RefreshCw :size="16" />
        刷新
      </button>
    </header>

    <div v-if="loading" class="loading-container surface-card">
      <div class="spinner"></div>
      <p>加载产品信息中</p>
    </div>

    <section v-else class="product-grid">
      <article v-for="product in productForms" :key="product.type" class="product-card surface-card">
        <div class="product-card__header">
          <span class="product-chip" :class="product.type">
            <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor">
              <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
            </svg>
            <span>{{ product.type }}</span>
          </span>
          <span class="color-dot" :style="{ backgroundColor: product.color }"></span>
        </div>

        <form class="product-form" @submit.prevent="saveProduct(product)">
          <div class="form-group">
            <label class="form-label" :for="`${product.type}-label`">展示名称</label>
            <input :id="`${product.type}-label`" v-model.trim="product.label" class="form-control" type="text" required />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label" :for="`${product.type}-price`">官方月费</label>
              <input
                :id="`${product.type}-price`"
                v-model.number="product.official_price"
                class="form-control"
                type="number"
                min="0"
                step="0.01"
                required
              />
            </div>
            <div class="form-group">
              <label class="form-label" :for="`${product.type}-seats`">最大人数</label>
              <input
                :id="`${product.type}-seats`"
                v-model.number="product.max_seats"
                class="form-control"
                type="number"
                min="2"
                max="50"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" :for="`${product.type}-color`">主题颜色</label>
            <div class="color-field">
              <input v-model="product.color" class="color-input" type="color" aria-label="选择产品颜色" />
              <input :id="`${product.type}-color`" v-model.trim="product.color" class="form-control" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" :for="`${product.type}-description`">产品说明</label>
            <textarea
              :id="`${product.type}-description`"
              v-model.trim="product.description"
              class="form-control textarea"
              rows="4"
            ></textarea>
          </div>

          <div class="product-summary">
            <div>
              <span>官方价</span>
              <strong>¥{{ formatMoney(product.official_price) }}/月</strong>
            </div>
            <div>
              <span>建议拼车上限</span>
              <strong>{{ product.max_seats }} 人</strong>
            </div>
          </div>

          <button type="submit" class="btn btn-primary" :disabled="savingType === product.type">
            <Save :size="16" />
            {{ savingType === product.type ? '保存中...' : '保存产品' }}
          </button>
        </form>
      </article>
    </section>

    <p v-if="message" class="feedback" role="status">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RefreshCw, Save } from '@lucide/vue'
import { ridesApi } from '../api/rides'
import { useUserStore } from '../stores/user'
import type { Product } from '../types'

const userStore = useUserStore()
const loading = ref(true)
const savingType = ref('')
const message = ref('')
const productForms = ref<Product[]>([])

const loadProducts = async () => {
  if (!userStore.isAdmin) {
    loading.value = false
    message.value = '只有管理员可以维护产品信息'
    return
  }
  loading.value = true
  message.value = ''
  try {
    const res = await ridesApi.getProducts()
    productForms.value = res.data.map((product: Product) => ({ ...product }))
  } catch {
    message.value = '产品信息加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

const saveProduct = async (product: Product) => {
  savingType.value = product.type
  message.value = ''
  try {
    const { type, ...payload } = product
    const res = await ridesApi.updateProduct(type, payload)
    Object.assign(product, res.data)
    message.value = `${product.label} 已保存`
  } catch {
    message.value = '保存失败，请确认当前账号拥有管理员权限'
  } finally {
    savingType.value = ''
  }
}

const formatMoney = (value: number | string) => Math.round(Number(value || 0))

onMounted(loadProducts)
</script>

<style scoped>
.products-page {
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
}

.page-title {
  margin: 4px 0 6px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.product-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
}

.product-card__header,
.color-field,
.product-summary {
  display: flex;
  align-items: center;
}

.product-card__header {
  justify-content: space-between;
}

.color-dot {
  width: 24px;
  height: 24px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-full);
}

.product-form {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.color-field {
  gap: var(--spacing-sm);
}

.color-input {
  width: 44px;
  height: 44px;
  flex: 0 0 44px;
  padding: 3px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-secondary);
  cursor: pointer;
}

.textarea {
  min-height: 104px;
  resize: vertical;
  line-height: 1.6;
}

.product-summary {
  justify-content: space-between;
  gap: var(--spacing-md);
  margin-top: auto;
  margin-bottom: var(--spacing-md);
  padding: 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
}

.product-summary span {
  display: block;
  margin-bottom: 4px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 800;
}

.product-summary strong {
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 900;
}

.feedback {
  color: var(--color-primary);
  font-size: 13px;
  font-weight: 900;
}

@media (max-width: 1080px) {
  .product-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .product-grid,
  .form-row {
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
