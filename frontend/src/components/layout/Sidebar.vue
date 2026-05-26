<template>
  <div class="mobile-top-bar">
    <router-link to="/" class="mobile-logo">
      <span class="logo-mark" aria-hidden="true">
        <img :src="logoMarkUrl" alt="" />
      </span>
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
          <span class="logo-mark" aria-hidden="true">
            <img :src="logoMarkUrl" alt="" />
          </span>
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
            <kbd v-if="item.shortcut" class="nav-shortcut">{{ item.shortcut }}</kbd>
          </div>
        </router-link>
      </nav>

      <nav v-if="userStore.isAdmin" class="nav-list admin-nav" aria-label="管理后台导航">
        <span class="nav-divider">管理后台</span>
        <router-link
          v-for="item in adminNavItems"
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
        <div class="legal-links">
          <a href="/privacy-policy.html" class="legal-link">隐私政策</a>
          <span class="legal-sep">·</span>
          <a href="/platform-spec.html" class="legal-link">平台规范</a>
        </div>

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
              <small>{{ userStore.user?.email }}</small>
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
import { Boxes, Home, LogOut, Menu, PlusCircle, Search, ShieldCheck, UserRound, Sun, Moon, LayoutDashboard, Users, ParkingSquare, ClipboardList, BarChart3 } from '@lucide/vue'
import { useUserStore } from '../../stores/user'
import logoMarkUrl from '../../assets/logo-mark.svg'

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
  { to: '/', label: '首页市场', icon: Home, shortcut: '' },
  { to: '/market', label: '发现车位', icon: Search, shortcut: '/' },
  { to: '/create', label: '发布车位', icon: PlusCircle, shortcut: '' },
  ...(userStore.isLoggedIn
    ? [{ to: '/profile', label: '我的账户', icon: UserRound, shortcut: '' }]
    : []),
])

const adminNavItems = computed(() => [
  { to: '/admin', label: '平台概览', icon: LayoutDashboard },
  { to: '/admin/users', label: '用户管理', icon: Users },
  { to: '/admin/rides', label: '车位管理', icon: ParkingSquare },
  { to: '/admin/orders', label: '订单管理', icon: ClipboardList },
  { to: '/admin/analytics', label: '数据分析', icon: BarChart3 },
  { to: '/admin/products', label: '产品维护', icon: Boxes },
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
  width: 28px;
  height: 28px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: transparent;
}

.logo-mark img {
  display: block;
  width: 100%;
  height: 100%;
  flex-shrink: 0;
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
  width: var(--sidebar-width);
  background: var(--bg-primary);
  border-right: 1px solid var(--border-color);
  box-shadow: var(--sidebar-shadow);
}

:global([data-theme="dark"] .sidebar ){
  background: var(--bg-secondary);
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
  padding: 18px 12px;
}

.brand-block {
  padding: 0 6px var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.brand-text strong {
  font-size: 15px;
  font-weight: 800;
  color: var(--text-primary);
}

.brand-text small {
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 600;
}

.nav-list {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 4px;
  padding: var(--spacing-md) 0;
}

.admin-nav {
  flex: 0;
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-md) 0 var(--spacing-xs);
  margin-top: var(--spacing-xs);
  background: transparent;
  border-radius: 0;
}

.nav-divider {
  display: block;
  padding: 0 14px var(--spacing-sm);
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
}

.nav-item {
  display: block;
  text-decoration: none;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 13px;
  transition: all var(--transition-fast);
  position: relative;
}

.nav-item-inner {
  display: flex;
  min-height: 34px;
  align-items: center;
  gap: 9px;
  padding: 0 10px;
}

.nav-icon {
  color: var(--text-muted);
  transition: color var(--transition-fast);
}

.nav-item:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
  box-shadow: inset 0 0 0 1px var(--border-color);
}

.nav-item:hover .nav-icon {
  color: var(--text-primary);
}

.nav-item.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  box-shadow: var(--card-shadow);
  font-weight: 700;
}

.nav-item.active::before {
  display: none;
}

.admin-nav .nav-item.active {
  color: var(--text-primary);
  background: var(--bg-secondary);
}

.admin-nav .nav-item.active::before {
  background: var(--color-pro);
  box-shadow: 0 0 8px rgba(139, 92, 246, 0.25);
}

.admin-nav .nav-item.active .nav-icon {
  color: var(--text-primary);
}

.nav-item.active .nav-icon {
  color: var(--text-primary);
}

.nav-shortcut {
  display: inline-flex;
  height: 18px;
  min-width: 18px;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  margin-left: auto;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: var(--bg-inset);
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 700;
  font-family: inherit;
  line-height: 1;
}

.notice-card {
  display: none;
  gap: 10px;
  padding: 14px;
  border: 1px solid var(--border-color);
  border-left: 3px solid var(--color-plus);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  transition: all var(--transition-fast);
}

.notice-card:hover {
  border-color: var(--border-color-strong);
  background: var(--bg-tertiary);
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
  gap: 10px;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.legal-links {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 var(--spacing-sm);
}

.legal-link {
  color: var(--text-muted);
  font-size: 11px;
  text-decoration: none;
  transition: color var(--transition-fast);
  position: relative;
}

.legal-link:hover {
  color: var(--text-primary);
}

.legal-link::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--text-primary);
  transform: scaleX(0);
  transform-origin: center;
  transition: transform var(--transition-fast);
}

.legal-link:hover::after {
  transform: scaleX(1);
}

.legal-sep {
  color: var(--border-color);
  font-size: 11px;
}

.user-card {
  display: flex;
  gap: 8px;
  align-items: center;
  text-decoration: none;
  padding: 7px 8px;
  border-radius: var(--border-radius-md);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.user-card:hover {
  background: var(--bg-tertiary);
  border-color: var(--border-color-strong);
}

.user-card:hover .avatar {
  box-shadow: 0 0 0 2px var(--color-team-soft);
}

.avatar {
  width: 30px;
  height: 30px;
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
  min-height: 34px;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: var(--border-radius-md);
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  color: var(--text-inverse);
  background: var(--color-team);
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.login-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  background: transparent;
  transform: translateX(-100%);
  transition: transform 0.5s ease;
}

.login-btn:hover {
  background: var(--color-primary-hover);
}

.login-btn:hover::after {
  transform: translateX(100%);
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
  padding: 8px 10px;
  margin-bottom: var(--spacing-md);
  border-radius: var(--border-radius-md);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

.theme-toggle-row:hover {
  border-color: var(--border-color-strong);
  background: var(--bg-tertiary);
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
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color-strong);
  cursor: pointer;
  padding: 0;
  transition: background-color var(--transition-fast), border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.theme-toggle-switch:focus {
  outline: none;
}

.theme-toggle-switch:focus-visible,
.icon-btn:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 2px;
}

:global([data-theme="dark"] .theme-toggle-switch ){
  background: var(--bg-inset);
  border-color: var(--border-color-strong);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.08);
}

.toggle-slider {
  position: absolute;
  top: 1px;
  left: 1px;
  width: 18px;
  height: 18px;
  border-radius: var(--border-radius-full);
  background: var(--text-muted);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), background-color var(--transition-fast), box-shadow var(--transition-fast);
}

:global([data-theme="dark"] .toggle-slider ){
  background: var(--text-primary);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.14);
}

.toggle-slider.is-dark {
  transform: translateX(18px);
}

/* Dark mode */
:global([data-theme="dark"] .nav-item.active::before ){
  box-shadow: 0 0 8px rgba(243, 240, 233, 0.15);
}

:global([data-theme="dark"] .admin-nav .nav-item.active::before ){
  box-shadow: 0 0 8px rgba(167, 139, 250, 0.3);
}

:global([data-theme="dark"] .notice-card ){
  background: var(--bg-inset);
}

:global([data-theme="dark"] .user-card:hover ){
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

:global([data-theme="dark"] .user-card:hover .avatar ){
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
}

:global([data-theme="dark"] .login-btn ){
  background: var(--text-primary);
  color: var(--text-inverse);
  border: 1px solid var(--text-primary);
}

:global([data-theme="dark"] .login-btn:hover ){
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  box-shadow: 0 2px 12px rgba(255, 255, 255, 0.12);
}
</style>
