<template>
  <div class="mobile-top-bar">
    <router-link to="/" class="mobile-logo">
      <span class="logo-mark">B</span>
      <span>BusGPT</span>
    </router-link>
    <div class="mobile-top-actions">
      <button class="icon-btn theme-toggle-btn" type="button" :aria-label="theme === 'light' ? '切换至暗色模式' : '切换至亮色模式'" @click="toggleTheme">
        <Sun v-if="theme === 'dark'" :size="20" />
        <Moon v-else :size="20" />
      </button>
      <button class="icon-btn" type="button" aria-label="打开导航" @click="mobileOpen = true">
        <Menu :size="22" />
      </button>
    </div>
  </div>

  <aside class="sidebar" :class="{ open: mobileOpen }">
    <button class="sidebar-scrim" type="button" aria-label="关闭导航" @click="mobileOpen = false"></button>
    <div class="sidebar-panel">
      <div class="brand-block">
        <router-link to="/" class="brand" @click="mobileOpen = false">
          <span class="logo-mark">B</span>
          <span class="brand-text">
            <strong>BusGPT</strong>
            <small>AI 订阅拼车平台</small>
          </span>
        </router-link>
      </div>

      <nav class="nav-list" aria-label="主导航">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          active-class="active"
          @click="mobileOpen = false"
        >
          <div class="nav-item-inner">
            <component :is="item.icon" :size="18" class="nav-icon" />
            <span>{{ item.label }}</span>
          </div>
        </router-link>
      </nav>

      <div class="notice-card">
        <ShieldCheck :size="16" class="notice-icon" />
        <div>
          <strong>信息共享服务</strong>
          <p>平台仅作车位信息聚合。查看联系方式后自行沟通后续交易。</p>
        </div>
      </div>

      <div class="sidebar-footer">
        <div class="theme-toggle-row">
          <span class="theme-label">
            <Sun v-if="theme === 'dark'" :size="15" />
            <Moon v-else :size="15" />
            <span>{{ theme === 'dark' ? '暗色模式' : '亮色模式' }}</span>
          </span>
          <button type="button" class="theme-toggle-switch" :aria-label="theme === 'light' ? '切换至暗色模式' : '切换至亮色模式'" @click="toggleTheme">
            <span class="toggle-slider" :class="{ 'is-dark': theme === 'dark' }"></span>
          </button>
        </div>

        <template v-if="userStore.isLoggedIn">
          <router-link to="/profile" class="user-card" @click="mobileOpen = false">
            <img :src="userStore.user?.avatar || defaultAvatar" alt="用户头像" class="avatar" />
            <div class="user-info">
              <strong>{{ userStore.user?.nickname }}</strong>
              <small>{{ userStore.user?.phone }}</small>
            </div>
          </router-link>
          <button type="button" class="logout-btn" @click="handleLogout">
            <LogOut :size="14" />
            <span>退出登录</span>
          </button>
        </template>
        <router-link v-else to="/login" class="login-btn" @click="mobileOpen = false">
          登录 / 注册
        </router-link>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Boxes, Home, LogOut, Menu, PlusCircle, Search, ShieldCheck, UserRound, Sun, Moon } from '@lucide/vue'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()
const router = useRouter()
const mobileOpen = ref(false)
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt&backgroundColor=0f172a'

const theme = ref<'light' | 'dark'>('light')

const initTheme = () => {
  const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null
  if (savedTheme) {
    theme.value = savedTheme
  } else {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    theme.value = prefersDark ? 'dark' : 'light'
  }
  document.documentElement.setAttribute('data-theme', theme.value)
}

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme.value)
  localStorage.setItem('theme', theme.value)
}

onMounted(() => {
  initTheme()
})

const navItems = computed(() => [
  { to: '/', label: '首页市场', icon: Home },
  { to: '/market', label: '发现车位', icon: Search },
  { to: '/create', label: '发布车位', icon: PlusCircle },
  ...(userStore.isLoggedIn
    ? [
        { to: '/profile', label: '我的账户', icon: UserRound },
        ...(userStore.isAdmin ? [{ to: '/products', label: '产品维护', icon: Boxes }] : []),
      ]
    : []),
])

const handleLogout = () => {
  userStore.logout()
  mobileOpen.value = false
  router.push('/')
}
</script>

<style scoped>
.mobile-top-bar {
  display: none;
  position: fixed;
  inset: 0 0 auto 0;
  z-index: 60;
  height: 56px;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-md);
  background: var(--bg-glass);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.mobile-top-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.mobile-logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
  font-weight: 800;
  text-decoration: none;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: var(--text-primary);
  text-decoration: none;
}

.logo-mark {
  display: inline-flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  color: var(--text-inverse);
  font-size: 18px;
  font-weight: 900;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.15);
}

.icon-btn {
  display: inline-flex;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
}

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 80;
  width: 248px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  box-shadow: var(--sidebar-shadow);
}

.sidebar-scrim {
  display: none;
  background: transparent;
  border: none;
}

.sidebar-panel {
  display: flex;
  height: 100%;
  flex-direction: column;
  padding: var(--spacing-lg) var(--spacing-md);
}

.brand-block {
  padding: 0 var(--spacing-sm) var(--spacing-lg) var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.brand-text strong {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
}

.brand-text small {
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 600;
}

.nav-list {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-lg) 0;
}

.nav-item {
  display: block;
  text-decoration: none;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 14px;
  transition: all var(--transition-fast);
}

.nav-item-inner {
  display: flex;
  min-height: 42px;
  align-items: center;
  gap: 12px;
  padding: 0 14px;
}

.nav-icon {
  color: var(--text-muted);
  transition: color var(--transition-fast);
}

.nav-item:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.nav-item:hover .nav-icon {
  color: var(--text-primary);
}

.nav-item.active {
  color: var(--text-primary);
  background: var(--bg-tertiary);
  font-weight: 700;
  box-shadow: inset 4px 0 0 var(--text-primary);
}

.nav-item.active .nav-icon {
  color: var(--text-primary);
}

.notice-card {
  display: flex;
  gap: 10px;
  padding: 14px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.notice-icon {
  color: var(--color-plus);
  flex-shrink: 0;
  margin-top: 2px;
}

.notice-card strong {
  display: block;
  margin-bottom: 2px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
}

.notice-card p {
  color: var(--text-secondary);
  font-size: 11px;
  line-height: 1.5;
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

.user-card {
  display: flex;
  gap: 12px;
  align-items: center;
  text-decoration: none;
  padding: 6px;
  border-radius: var(--border-radius-md);
  transition: background-color var(--transition-fast);
}

.user-card:hover {
  background: var(--bg-tertiary);
}

.avatar {
  width: 38px;
  height: 38px;
  border-radius: var(--border-radius-full);
  border: 1px solid var(--border-color);
}

.user-info {
  display: flex;
  min-width: 0;
  flex-direction: column;
}

.user-info strong {
  overflow: hidden;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-info small {
  color: var(--text-muted);
  font-size: 11px;
}

.login-btn {
  display: inline-flex;
  min-height: 42px;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: var(--border-radius-md);
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  color: var(--text-inverse);
  background: var(--color-primary);
  transition: background-color var(--transition-fast);
}

.login-btn:hover {
  background: var(--color-primary-hover);
}

.logout-btn {
  display: inline-flex;
  min-height: 36px;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: var(--border-radius-md);
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.logout-btn:hover {
  color: var(--color-danger);
  background: var(--color-danger-soft);
  border-color: rgba(239, 68, 68, 0.2);
}

@media (max-width: 768px) {
  .mobile-top-bar {
    display: flex;
  }

  .sidebar {
    width: 100%;
    pointer-events: none;
    background: transparent;
    border-right: 0;
    box-shadow: none;
    transform: none;
  }

  .sidebar-scrim {
    display: block;
    position: fixed;
    inset: 0;
    opacity: 0;
    background: rgba(15, 23, 42, 0.3);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    transition: opacity var(--transition-normal);
  }

  .sidebar-panel {
    width: 280px;
    max-width: calc(100vw - 40px);
    background: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
    transform: translateX(-100%);
    transition: transform var(--transition-normal);
  }

  .sidebar.open {
    pointer-events: auto;
  }

  .sidebar.open .sidebar-scrim {
    opacity: 1;
  }

  .sidebar.open .sidebar-panel {
    transform: translateX(0);
  }
}

.theme-toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  margin-bottom: var(--spacing-md);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.theme-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.theme-toggle-switch {
  position: relative;
  width: 40px;
  height: 22px;
  border-radius: var(--border-radius-full);
  background: var(--border-color-strong);
  border: none;
  cursor: pointer;
  padding: 0;
  transition: background-color var(--transition-fast);
}

.theme-toggle-switch:focus {
  outline: none;
}

.theme-toggle-switch:focus-visible,
.icon-btn:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 2px;
}

[data-theme="dark"] .theme-toggle-switch {
  background: var(--color-success);
}

.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 18px;
  height: 18px;
  border-radius: var(--border-radius-full);
  background: var(--bg-secondary);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform var(--transition-fast);
}

.toggle-slider.is-dark {
  transform: translateX(18px);
}
</style>
