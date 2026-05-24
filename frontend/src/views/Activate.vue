<template>
  <div class="activate-page container">
    <div class="activate-wrapper surface-card">
      <div class="activate-brand">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
            <path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" />
          </svg>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="status === 'loading'" class="activate-content">
        <div class="activate-spinner"></div>
        <h2>正在验证激活链接...</h2>
        <p>请稍候，正在处理您的邮箱验证。</p>
      </div>

      <!-- Success State -->
      <div v-else-if="status === 'success'" class="activate-content">
        <div class="activate-icon success">
          <CheckCircle :size="40" />
        </div>
        <h2>邮箱已激活</h2>
        <p>您的账号已成功激活，现在可以使用邮箱和密码登录了。</p>
        <router-link to="/login?activated=true" class="btn btn-primary activate-btn">
          立即登录
        </router-link>
      </div>

      <!-- Error State -->
      <div v-else class="activate-content">
        <div class="activate-icon error">
          <XCircle :size="40" />
        </div>
        <h2>激活失败</h2>
        <p class="error-reason">{{ errorReason }}</p>
        <div class="activate-actions">
          <router-link to="/login" class="btn btn-primary activate-btn">
            返回登录
          </router-link>
          <router-link to="/login" class="btn btn-secondary">
            重新注册
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { CheckCircle, XCircle } from '@lucide/vue'
import { authApi } from '../api/auth'

const route = useRoute()

const status = ref<'loading' | 'success' | 'error'>('loading')
const errorReason = ref('')

function getErrorMessage(key: string): string {
  const messages: { [k: string]: string } = {
    invalid_token: '激活链接无效，请检查是否完整复制了链接。',
    expired: '激活链接已过期，请重新注册或请求新的激活邮件。',
    user_not_found: '对应的用户不存在，请重新注册。',
  }
  return messages[key] || '激活过程中发生未知错误，请稍后重试。'
}

onMounted(async () => {
  const queryStatus = (route.query.status as string) || ''
  const token = (route.query.token as string) || ''
  const reason = (route.query.reason as string) || ''

  // If redirected from backend with status params (no token needed)
  if (queryStatus) {
    if (queryStatus === 'success') {
      status.value = 'success'
    } else {
      status.value = 'error'
      errorReason.value = getErrorMessage(reason)
    }
    return
  }

  // If token is in query, call API to activate
  if (token) {
    try {
      await authApi.activate(token)
      status.value = 'success'
    } catch (err) {
      status.value = 'error'
      const errorVal = err as { response?: { data?: { detail?: string } } }
      errorReason.value = errorVal.response?.data?.detail || getErrorMessage('unknown')
    }
    return
  }

  // No token and no status — invalid access
  status.value = 'error'
  errorReason.value = '未提供激活令牌，请从邮件中点击激活链接。'
})
</script>

<style scoped>
.activate-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: var(--spacing-xl) 0;
}

.activate-wrapper {
  width: 100%;
  max-width: 420px;
  padding: var(--spacing-xl);
  text-align: center;
  border-color: var(--border-color-strong);
  box-shadow: var(--card-shadow-hover);
  animation: cardEntrance 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
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

.activate-brand {
  display: flex;
  justify-content: center;
  margin-bottom: var(--spacing-xl);
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
}

.activate-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.activate-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--text-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.activate-icon {
  display: flex;
  width: 72px;
  height: 72px;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.activate-icon.success {
  background: var(--color-success-soft);
  color: var(--color-success);
  animation: scaleIn 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.activate-icon.error {
  background: var(--color-danger-soft);
  color: var(--color-danger);
  animation: scaleIn 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes scaleIn {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.activate-content h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary);
}

.activate-content p {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 320px;
}

.error-reason {
  color: var(--color-danger) !important;
  font-weight: 600;
}

.activate-btn {
  min-width: 160px;
}

.activate-actions {
  display: flex;
  gap: var(--spacing-sm);
}
</style>
