<template>
  <div class="login-page container">
    <div class="login-wrapper surface-card">
      <!-- Title Header -->
      <div class="login-heading">
        <span class="eyebrow">账户中心</span>
        <h1>{{ isLoginMode ? '欢迎回来' : '创建全新账户' }}</h1>
        <p>登录后可自由发布共享车位、生成拼车订单以及解锁车友联系渠道。</p>
      </div>

      <!-- Tab Selectors -->
      <div class="login-tabs">
        <button
          type="button"
          class="tab-btn"
          :class="{ active: isLoginMode }"
          @click="isLoginMode = true"
        >
          登 录
        </button>
        <button
          type="button"
          class="tab-btn"
          :class="{ active: !isLoginMode }"
          @click="isLoginMode = false"
        >
          注 册
        </button>
      </div>

      <!-- Login/Register Form -->
      <form @submit.prevent="handleSubmit" class="login-form">
        <!-- Nickname (Register only) -->
        <div class="form-group animate-fade" v-if="!isLoginMode">
          <label class="form-label" for="nickname">昵称</label>
          <input
            type="text"
            id="nickname"
            v-model="form.nickname"
            placeholder="请填写您的展示昵称"
            :required="!isLoginMode"
            class="form-control"
          />
        </div>

        <!-- Phone -->
        <div class="form-group">
          <label class="form-label" for="phone">绑定手机号码</label>
          <input
            type="tel"
            id="phone"
            v-model="form.phone"
            pattern="^1[3-9]\d{9}$"
            placeholder="请输入您的11位手机号"
            required
            class="form-control"
          />
        </div>

        <!-- Password -->
        <div class="form-group">
          <label class="form-label" for="password">账户登录密码</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            placeholder="请输入密码（最少 6 位）"
            minlength="6"
            required
            class="form-control"
          />
        </div>

        <!-- Terms Agreement (Register only) -->
        <div class="form-group check-group animate-fade" v-if="!isLoginMode">
          <label class="checkbox-label">
            <input type="checkbox" v-model="agreementChecked" :required="!isLoginMode" />
            <span class="checkbox-text">我已阅读并完全同意 <a href="#" class="protocol-link" @click.prevent>《用户共享展示服务条款》</a></span>
          </label>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary submit-btn-action" :disabled="userStore.loading">
          <span>{{ userStore.loading ? '正在核对数据...' : isLoginMode ? '立即登录' : '同意协议并注册' }}</span>
        </button>

        <p class="login-error-msg" v-if="userStore.error">{{ userStore.error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const isLoginMode = ref(true)
const agreementChecked = ref(false)

const form = reactive({
  phone: '',
  nickname: '',
  password: '',
})

const handleSubmit = async () => {
  let success = false
  if (isLoginMode.value) {
    success = await userStore.login(form.phone, form.password)
  } else {
    if (!agreementChecked.value) {
      alert('请先同意服务条款')
      return
    }
    success = await userStore.register(form.phone, form.nickname, form.password)
  }

  if (success) {
    const redirectPath = (route.query.redirect as string) || '/'
    router.push(redirectPath)
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 140px);
  padding: var(--spacing-xl) 0;
}

.login-wrapper {
  width: 100%;
  max-width: 400px;
  padding: var(--spacing-xl);
  border-color: var(--border-color-strong);
  box-shadow: var(--card-shadow-hover);
}

.login-heading {
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.login-heading h1 {
  margin: var(--spacing-xs) 0;
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.login-heading p {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
  margin: 0;
}

.login-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: var(--spacing-lg);
}

.tab-btn {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-secondary);
  padding: var(--spacing-sm) 0;
  flex: 1;
  text-align: center;
  position: relative;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: color var(--transition-fast);
}

.tab-btn:hover,
.tab-btn.active {
  color: var(--text-primary);
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 20%;
  width: 60%;
  height: 2px;
  background-color: var(--text-primary);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.check-group {
  margin-top: var(--spacing-xs);
}

.checkbox-label {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  cursor: pointer;
}

.checkbox-label input {
  margin-top: 3px;
}

.checkbox-text {
  font-size: 11px;
  line-height: 1.4;
  color: var(--text-secondary);
}

.protocol-link {
  color: var(--text-primary);
  font-weight: 700;
  text-decoration: none;
}

.protocol-link:hover {
  text-decoration: underline;
}

.submit-btn-action {
  width: 100%;
  margin-top: var(--spacing-md);
}

.login-error-msg {
  color: var(--color-danger);
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  margin-top: var(--spacing-sm);
}

.animate-fade {
  animation: fadeIn var(--transition-normal);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
