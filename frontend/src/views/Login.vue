<template>
  <div class="login-page container">
    <div class="login-wrapper surface-card">
      <div class="login-heading">
        <span class="eyebrow">BusGPT</span>
        <h1>{{ isLoginMode ? '登录账户' : '创建账户' }}</h1>
        <p>登录后可以发布车位、支付信息服务费并查看已解锁联系方式。</p>
      </div>
      <!-- Tabs -->
      <div class="login-tabs">
        <button 
          class="tab-btn" 
          :class="{ active: isLoginMode }" 
          @click="isLoginMode = true"
        >
          登 录
        </button>
        <button 
          class="tab-btn" 
          :class="{ active: !isLoginMode }" 
          @click="isLoginMode = false"
        >
          注 册
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="login-form">
        <!-- Nickname (Register only) -->
        <div class="form-group" v-if="!isLoginMode">
          <label class="form-label" for="nickname">昵称</label>
          <input 
            type="text" 
            id="nickname" 
            v-model="form.nickname" 
            placeholder="请输入您的昵称" 
            :required="!isLoginMode"
            class="form-control"
          />
        </div>

        <!-- Phone -->
        <div class="form-group">
          <label class="form-label" for="phone">手机号</label>
          <input 
            type="tel" 
            id="phone" 
            v-model="form.phone" 
            pattern="^1[3-9]\d{9}$"
            placeholder="请输入您的手机号" 
            required 
            class="form-control"
          />
        </div>

        <!-- Password -->
        <div class="form-group">
          <label class="form-label" for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="form.password" 
            placeholder="请输入密码 (至少 6 位)" 
            minlength="6"
            required 
            class="form-control"
          />
        </div>

        <!-- Agreement (Register only) -->
        <div class="form-group check-group" v-if="!isLoginMode">
          <label class="checkbox-label">
            <input type="checkbox" v-model="agreementChecked" required />
            <span>我已阅读并同意 <a href="#" class="protocol-link">《信息展示服务条款》</a></span>
          </label>
        </div>

        <!-- Submit -->
        <button type="submit" class="submit-btn" :disabled="userStore.loading">
          {{ userStore.loading ? '处理中...' : isLoginMode ? '立即登录' : '同意协议并注册' }}
        </button>

        <p class="error-msg" v-if="userStore.error">{{ userStore.error }}</p>
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
      alert('请勾选服务协议')
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
  min-height: calc(100vh - 120px);
  padding: var(--spacing-xl) 0;
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
  padding: var(--spacing-xl);
}

.login-heading {
  margin-bottom: var(--spacing-lg);
}

.login-heading h1 {
  margin: 4px 0 8px;
  color: var(--text-primary);
  font-size: 24px;
  font-weight: 900;
}

.login-heading p {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.7;
}

.login-tabs {
  display: flex;
  justify-content: space-around;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: var(--spacing-xl);
}

.tab-btn {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-secondary);
  padding: var(--spacing-sm) 0;
  flex: 1;
  text-align: center;
  position: relative;
  transition: color var(--transition-fast);
}

.tab-btn:hover, .tab-btn.active {
  color: var(--text-primary);
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 20%;
  width: 60%;
  height: 2px;
  background-color: var(--color-primary);
}

.login-form {
  display: flex;
  flex-direction: column;
}

.check-group {
  margin-top: -2px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 12px;
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
}

.protocol-link {
  color: var(--color-primary);
}

.submit-btn {
  width: 100%;
  padding: 11px;
  font-weight: 700;
  font-size: 14px;
  border-radius: var(--border-radius-md);
  background-color: var(--color-primary);
  color: #ffffff;
  margin-top: var(--spacing-md);
  transition: background-color var(--transition-fast);
}

.submit-btn:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-msg {
  color: var(--color-danger);
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  margin-top: var(--spacing-md);
}
</style>
