<template>
  <div class="login-page container">
    <!-- Background texture -->
    <div class="login-ambient">
    </div>

    <div class="login-wrapper surface-card">
      <!-- Brand Mark -->
      <div class="login-brand">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
            <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
          </svg>
        </div>
      </div>

      <!-- Title Header -->
      <div class="login-heading">
        <h1>{{ isLoginMode ? '欢迎回来' : '创建全新账户' }}</h1>
        <p>登录后可自由发布共享车位、查看车友联系方式。</p>
      </div>

      <!-- Activation Success Banner -->
      <div v-if="showActivationSuccess" class="activation-banner success">
        <CheckCircle :size="16" />
        <span>邮箱已激活成功！请使用邮箱和密码登录。</span>
      </div>

      <!-- Tab Selectors -->
      <div class="login-tabs">
        <button
          type="button"
          class="tab-btn"
          :class="{ active: isLoginMode }"
          @click="switchMode(true)"
        >
          登 录
        </button>
        <button
          type="button"
          class="tab-btn"
          :class="{ active: !isLoginMode }"
          @click="switchMode(false)"
        >
          注 册
        </button>
        <span class="tab-indicator" :class="{ right: !isLoginMode }"></span>
      </div>

      <!-- Login/Register Form -->
      <form @submit.prevent="handleSubmit" class="login-form" :class="{ 'register-mode': !isLoginMode }">
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

        <!-- Email -->
        <div class="form-group">
          <label class="form-label" for="email">邮箱地址</label>
          <input
            type="email"
            id="email"
            v-model="form.email"
            placeholder="请输入您的邮箱地址"
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
            <span class="checkbox-visual" :class="{ checked: agreementChecked }">
              <Check v-if="agreementChecked" :size="12" />
            </span>
            <input type="checkbox" v-model="agreementChecked" :required="!isLoginMode" class="sr-only" />
            <span class="checkbox-text">我已阅读并完全同意 <a href="#" class="protocol-link" @click.prevent>《用户共享展示服务条款》</a></span>
          </label>
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary submit-btn-action" :disabled="userStore.loading">
          <span>{{ userStore.loading ? '正在核对数据...' : isLoginMode ? '立即登录' : '同意协议并注册' }}</span>
        </button>

        <p class="login-error-msg" v-if="userStore.error">{{ userStore.error }}</p>
      </form>

      <!-- Registration Success: Resend Activation -->
      <div v-if="registrationSuccess && !isLoginMode" class="resend-section">
        <p class="resend-text">
          <MailCheck :size="14" />
          <span>激活邮件已发送至 <strong>{{ form.email }}</strong>，请查收。</span>
        </p>
        <button
          type="button"
          class="btn btn-secondary resend-btn"
          :disabled="resendLoading"
          @click="handleResendActivation"
        >
          {{ resendLoading ? '发送中...' : '未收到？重新发送' }}
        </button>
        <p v-if="resendMessage" class="resend-message">{{ resendMessage }}</p>
      </div>

      <!-- Trust Signals -->
      <div class="login-trust">
        <div class="trust-item">
          <ShieldCheck :size="14" />
          <span>数据加密传输</span>
        </div>
        <div class="trust-divider"></div>
        <div class="trust-item">
          <Users :size="14" />
          <span>{{ formattedUserCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Check, CheckCircle, ShieldCheck, Users, MailCheck } from '@lucide/vue'
import { useUserStore } from '../stores/user'
import { analyticsApi } from '../api/analytics'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const isLoginMode = ref(true)
const agreementChecked = ref(false)
const registrationSuccess = ref(false)
const resendLoading = ref(false)
const resendMessage = ref('')
const totalUsers = ref<number | null>(null)

const showActivationSuccess = computed(() => route.query.activated === 'true')

const form = reactive({
  email: '',
  nickname: '',
  password: '',
})

const formattedUserCount = computed(() => {
  if (totalUsers.value === null) return '用户增长中'
  return `已有 ${new Intl.NumberFormat('zh-CN').format(totalUsers.value)} 位用户`
})

const switchMode = (login: boolean) => {
  isLoginMode.value = login
  registrationSuccess.value = false
  resendMessage.value = ''
}

const handleSubmit = async () => {
  let success = false
  if (isLoginMode.value) {
    success = await userStore.login(form.email, form.password)
  } else {
    if (!agreementChecked.value) {
      alert('请先同意服务条款')
      return
    }
    success = await userStore.register(form.email, form.nickname, form.password)
  }

  if (success) {
    if (isLoginMode.value) {
      const redirectPath = (route.query.redirect as string) || '/'
      router.push(redirectPath)
    } else {
      // Registration succeeded — show activation prompt
      registrationSuccess.value = true
    }
  }
}

const handleResendActivation = async () => {
  resendLoading.value = true
  resendMessage.value = ''
  const success = await userStore.resendActivation(form.email)
  resendLoading.value = false
  if (success) {
    resendMessage.value = '激活邮件已重新发送，请查收。'
  } else {
    resendMessage.value = userStore.error || '发送失败，请稍后重试。'
  }
}

onMounted(() => {
  if (route.query.activated === 'true') {
    isLoginMode.value = true
  }
  loadPlatformStats()
})

const loadPlatformStats = async () => {
  try {
    const res = await analyticsApi.getPlatformStats()
    totalUsers.value = res.data.total_users
  } catch (err) {
    console.error('Failed to load platform stats', err)
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
  position: relative;
  overflow: hidden;
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--bg-secondary) 70%, transparent), var(--bg-primary) 72%),
    linear-gradient(90deg, rgba(16, 185, 129, 0.05), rgba(59, 130, 246, 0.04) 48%, rgba(139, 92, 246, 0.04));
}

/* Background texture */
.login-ambient {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  background:
    linear-gradient(var(--border-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--border-color) 1px, transparent 1px);
  background-size: 42px 42px;
  opacity: 0.28;
  mask-image: linear-gradient(to bottom, black, transparent 82%);
}

.login-ambient::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    repeating-linear-gradient(
      135deg,
      transparent 0,
      transparent 16px,
      color-mix(in srgb, var(--color-team) 12%, transparent) 16px,
      color-mix(in srgb, var(--color-team) 12%, transparent) 17px
    );
  opacity: 0.18;
}

.login-wrapper {
  width: 100%;
  max-width: 420px;
  padding: var(--spacing-xl) var(--spacing-xl) var(--spacing-lg);
  border-color: var(--border-color-strong);
  background: color-mix(in srgb, var(--bg-secondary) 92%, transparent);
  box-shadow: 0 16px 44px rgba(15, 23, 42, 0.08), var(--card-shadow);
  position: relative;
  overflow: hidden;
  animation: cardEntrance 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(12px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.login-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--border-color-strong);
}

.login-brand {
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-lg);
}

.brand-icon {
  display: inline-flex;
  width: 52px;
  height: 52px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-lg);
  background: var(--text-primary);
  color: var(--bg-primary);
  box-shadow: var(--card-shadow);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.brand-icon:hover {
  transform: scale(1.05) rotate(-5deg);
  box-shadow: var(--card-shadow-hover);
}

.login-heading {
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.login-heading h1 {
  margin: var(--spacing-xs) 0;
  color: var(--text-primary);
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.login-heading p {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
  margin: 0;
}

/* Activation Success Banner */
.activation-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: var(--border-radius-md);
  margin-bottom: var(--spacing-md);
  font-size: 13px;
  font-weight: 700;
  animation: fadeIn var(--transition-normal);
}

.activation-banner.success {
  background: var(--color-success-soft);
  color: var(--color-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

/* Tabs */
.login-tabs {
  display: flex;
  position: relative;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: var(--spacing-lg);
}

.tab-btn {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-muted);
  padding: var(--spacing-sm) 0;
  flex: 1;
  text-align: center;
  position: relative;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: color var(--transition-fast);
  z-index: 1;
}

.tab-btn:hover {
  color: var(--text-secondary);
}

.tab-btn.active {
  color: var(--text-primary);
}

.tab-indicator {
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 50%;
  height: 2px;
  background: var(--text-primary);
  border-radius: 1px;
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.tab-indicator.right {
  transform: translateX(100%);
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.login-form .form-control {
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.login-form .form-control:focus {
  border-color: var(--text-primary);
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.login-form .form-group:nth-child(1) .form-control:focus {
  border-color: var(--color-plus);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.login-form .form-group:nth-child(2) .form-control:focus {
  border-color: var(--color-team);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.login-form .form-group:nth-child(3) .form-control:focus {
  border-color: var(--color-pro);
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.login-form .form-group {
  animation: formSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.login-form .form-group:nth-child(1) { animation-delay: 0.05s; }
.login-form .form-group:nth-child(2) { animation-delay: 0.1s; }
.login-form .form-group:nth-child(3) { animation-delay: 0.15s; }
.login-form .form-group:nth-child(4) { animation-delay: 0.2s; }

@keyframes formSlideIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.check-group {
  margin-top: var(--spacing-xs);
}

.checkbox-label {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  cursor: pointer;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.checkbox-visual {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  margin-top: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
  border: 2px solid var(--border-color-strong);
  background: var(--bg-secondary);
  color: white;
  transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1);
}

.checkbox-visual.checked {
  background: var(--color-success);
  border-color: var(--color-success);
  animation: checkPop 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes checkPop {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.checkbox-text {
  font-size: 12px;
  line-height: 1.6;
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
  position: relative;
  overflow: hidden;
}

.submit-btn-action::after {
  content: '';
  position: absolute;
  inset: 0;
  background: transparent;
  transform: translateX(-100%);
  transition: transform 0.5s ease;
}

.submit-btn-action:hover::after {
  transform: translateX(100%);
}

.login-error-msg {
  color: var(--color-danger);
  font-size: 12px;
  font-weight: 700;
  text-align: center;
  margin-top: var(--spacing-sm);
  animation: shake 0.4s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
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

/* Resend Activation Section */
.resend-section {
  margin-top: var(--spacing-md);
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  text-align: center;
  animation: fadeIn 0.3s ease;
}

.resend-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-sm);
  line-height: 1.5;
}

.resend-text strong {
  color: var(--text-primary);
  word-break: break-all;
}

.resend-btn {
  width: 100%;
}

.resend-message {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-success);
  margin-top: var(--spacing-sm);
}

/* Trust Signals */
.login-trust {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
}

.trust-item svg {
  color: var(--color-plus);
  opacity: 0.7;
}

.trust-divider {
  width: 1px;
  height: 14px;
  background: var(--border-color);
}

/* Dark mode */
:global([data-theme="dark"] .login-page ){
  background:
    linear-gradient(180deg, color-mix(in srgb, var(--bg-secondary) 78%, transparent), var(--bg-primary) 74%),
    linear-gradient(90deg, rgba(16, 185, 129, 0.05), rgba(96, 165, 250, 0.04) 48%, rgba(167, 139, 250, 0.04));
}

:global([data-theme="dark"] .login-ambient ){
  opacity: 0.16;
}

:global([data-theme="dark"] .login-wrapper ){
  background: color-mix(in srgb, var(--bg-secondary) 90%, transparent);
  box-shadow: 0 18px 48px rgba(0, 0, 0, 0.32), var(--card-shadow);
}

:global([data-theme="dark"] .login-form .form-group:nth-child(1) .form-control:focus ){
  box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.15);
}

:global([data-theme="dark"] .login-form .form-group:nth-child(2) .form-control:focus ){
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.15);
}

:global([data-theme="dark"] .login-form .form-group:nth-child(3) .form-control:focus ){
  box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15);
}

:global([data-theme="dark"] .trust-item svg ){
  opacity: 0.5;
}

:global([data-theme="dark"] .checkbox-visual ){
  background: var(--bg-tertiary);
  border-color: var(--border-color-strong);
}

/* Responsive */
@media (max-width: 480px) {
  .login-wrapper {
    padding: var(--spacing-lg) var(--spacing-md) var(--spacing-md);
    border-radius: var(--border-radius-md);
  }

  .brand-icon {
    width: 44px;
    height: 44px;
  }

  .login-heading h1 {
    font-size: 20px;
  }

  .login-ambient {
    opacity: 0.16;
  }

  .login-trust {
    flex-direction: column;
    gap: 6px;
  }

  .trust-divider {
    display: none;
  }
}
</style>
