<template>
  <div class="mobile-top-bar">
    <router-link to="/" class="mobile-logo">
      <span class="logo-mark" aria-hidden="true">
        <img :src="logoMarkUrl" alt="" width="28" height="28" />
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

  <aside
    ref="sidebarRoot"
    class="sidebar"
    :class="{ open: mobileOpen, collapsed: sidebarCollapsed }"
    @transitionend="handleSidebarTransitionEnd"
  >
    <button class="sidebar-scrim" type="button" aria-label="关闭导航" @click="mobileOpen = false"></button>
    <div class="sidebar-panel">
      <span
        v-if="activeNavKind"
        class="nav-jelly-block"
        :class="{ admin: activeNavKind === 'admin' }"
        :style="navIndicatorStyle"
        aria-hidden="true"
      ></span>
      <div class="brand-block">
        <router-link
          :to="sidebarCollapsed ? route.fullPath : '/'"
          class="brand"
          :title="sidebarCollapsed ? '展开侧边栏' : '返回首页'"
          @click="handleBrandClick"
        >
          <span class="logo-mark" aria-hidden="true">
            <img :src="logoMarkUrl" alt="" width="28" height="28" />
          </span>
          <span class="brand-text">
            <strong>BusGPT</strong>
            <small>AI 订阅拼车平台</small>
          </span>
        </router-link>
        <button
          class="sidebar-collapse-btn"
          type="button"
          :aria-label="sidebarCollapsed ? '展开侧边栏' : '折叠侧边栏'"
          :title="sidebarCollapsed ? '展开侧边栏' : '折叠侧边栏'"
          @click="toggleSidebar"
        >
          <PanelLeftOpen v-if="sidebarCollapsed" :size="15" />
          <PanelLeftClose v-else :size="15" />
        </button>
      </div>

      <nav class="nav-list" aria-label="主导航">
        <div class="nav-track" data-nav-track="main">
          <router-link
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="nav-item"
            :class="{ active: isRouteActive(item.to) }"
            :data-active="isRouteActive(item.to) ? 'true' : undefined"
            :title="item.label"
            @click="handleNavClick"
          >
            <div class="nav-item-inner">
              <component :is="item.icon" :size="20" class="nav-icon" />
              <span>{{ item.label }}</span>
            </div>
          </router-link>
        </div>
      </nav>

      <nav v-if="userStore.isAdmin" class="nav-list admin-nav" aria-label="管理后台导航">
        <span class="nav-divider">管理后台</span>
        <div class="nav-track" data-nav-track="admin">
          <router-link
            v-for="item in adminNavItems"
            :key="item.to"
            :to="item.to"
            class="nav-item"
            :class="{ active: isRouteActive(item.to) }"
            :data-active="isRouteActive(item.to) ? 'true' : undefined"
            :title="item.label"
            @click="handleNavClick"
          >
            <div class="nav-item-inner">
              <component :is="item.icon" :size="20" class="nav-icon" />
              <span>{{ item.label }}</span>
            </div>
          </router-link>
        </div>
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
          <button type="button" class="theme-toggle-switch" :aria-label="theme === 'light' ? '切换至暗色模式' : '切换至亮色模式'" :title="theme === 'light' ? '切换至暗色模式' : '切换至亮色模式'" @click="toggleTheme">
            <span class="toggle-slider" :class="{ 'is-dark': theme === 'dark' }"></span>
          </button>
        </div>

        <template v-if="userStore.isLoggedIn">
          <router-link to="/profile" class="user-card" :title="userStore.user?.nickname || '我的账户'" @click="mobileOpen = false">
            <img :src="userStore.user?.avatar || defaultAvatar" alt="用户头像" class="avatar" />
            <div class="user-info">
              <strong :title="userStore.user?.nickname || ''">{{ userStore.user?.nickname }}</strong>
              <small :title="userStore.user?.email || ''">{{ userStore.user?.email }}</small>
            </div>
          </router-link>
          <button type="button" class="logout-btn" title="退出登录" @click="openLogoutConfirm">
            <LogOut :size="14" />
            <span>退出登录</span>
          </button>
        </template>
        <router-link v-else to="/login" class="login-btn" title="登录 / 注册" @click="mobileOpen = false">
          <LogIn :size="14" class="login-icon" />
          <span>登录 / 注册</span>
        </router-link>
      </div>
    </div>
  </aside>

  <Transition name="logout-confirm">
    <div
      v-if="showLogoutConfirm"
      class="logout-confirm-backdrop"
      role="dialog"
      aria-modal="true"
      aria-labelledby="logout-confirm-title"
      tabindex="-1"
      @click.self="closeLogoutConfirm"
      @keydown.esc="closeLogoutConfirm"
    >
      <div class="logout-confirm-modal surface-card">
        <div class="logout-confirm-icon" aria-hidden="true">
          <LogOut :size="20" />
        </div>
        <div class="logout-confirm-copy">
          <h2 id="logout-confirm-title">确认退出登录？</h2>
          <p>退出后将回到首页，继续发布或管理车位需要重新登录。</p>
        </div>
        <div class="logout-confirm-actions">
          <button type="button" class="btn btn-secondary" @click="closeLogoutConfirm">取消</button>
          <button type="button" class="btn btn-danger" autofocus @click="confirmLogout">
            <LogOut :size="14" />
            <span>确认退出</span>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onBeforeUnmount, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Boxes, Home, LogIn, LogOut, Menu, PanelLeftClose, PanelLeftOpen, PlusCircle, Search, ShieldCheck, UserRound, Sun, Moon, LayoutDashboard, Users, ParkingSquare, ClipboardList, BarChart3 } from '@lucide/vue'
import { useUserStore } from '../../stores/user'
import logoMarkUrl from '../../assets/logo-mark.svg'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const mobileOpen = ref(false)
const sidebarCollapsed = ref(false)
const sidebarRoot = ref<HTMLElement | null>(null)
const navIndicatorStyle = ref<Record<string, string>>({})
const activeNavKind = ref<'main' | 'admin' | null>(null)
const showLogoutConfirm = ref(false)
const defaultAvatar = 'https://api.dicebear.com/7.x/initials/svg?seed=busgpt&backgroundColor=0f172a'
const sidebarTransitionSettleMs = 480
let indicatorRefreshTimer: ReturnType<typeof setTimeout> | null = null

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

const applySidebarState = () => {
  document.documentElement.classList.toggle('sidebar-collapsed', sidebarCollapsed.value)
  updateIndicator()
  scheduleIndicatorUpdate(sidebarTransitionSettleMs)
}

const initSidebar = () => {
  sidebarCollapsed.value = localStorage.getItem('sidebar-collapsed') === 'true'
  applySidebarState()
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
  localStorage.setItem('sidebar-collapsed', String(sidebarCollapsed.value))
  applySidebarState()
}

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme.value)
  localStorage.setItem('theme', theme.value)
}

onMounted(() => {
  initTheme()
  initSidebar()
  updateIndicator()
  window.addEventListener('resize', updateIndicator)
})

onBeforeUnmount(() => {
  if (indicatorRefreshTimer) {
    clearTimeout(indicatorRefreshTimer)
  }
  window.removeEventListener('resize', updateIndicator)
})

const navItems = computed(() => [
  { to: '/', label: '首页市场', icon: Home },
  { to: '/market', label: '发现车位', icon: Search },
  { to: '/create', label: '发布车位', icon: PlusCircle },
  ...(userStore.isLoggedIn
    ? [{ to: '/profile', label: '我的账户', icon: UserRound }]
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

const isRouteActive = (to: string) => {
  if (to === '/' || to === '/admin') {
    return route.path === to
  }
  return route.path === to || route.path.startsWith(`${to}/`)
}

const readIndicatorMetrics = () => {
  const panel = sidebarRoot.value?.querySelector<HTMLElement>('.sidebar-panel')
  const activeItem = panel?.querySelector<HTMLElement>('.nav-item.active')
  const track = activeItem?.closest<HTMLElement>('.nav-track')

  if (!panel || !activeItem || !track) {
    return { active: false as const }
  }

  const panelRect = panel.getBoundingClientRect()
  const itemRect = activeItem.getBoundingClientRect()
  const kind: 'main' | 'admin' = track.dataset.navTrack === 'admin' ? 'admin' : 'main'

  return {
    active: true as const,
    kind,
    style: {
      '--nav-jelly-x': `${itemRect.left - panelRect.left}px`,
      '--nav-jelly-y': `${itemRect.top - panelRect.top}px`,
      '--nav-jelly-w': `${activeItem.offsetWidth}px`,
      '--nav-jelly-h': `${activeItem.offsetHeight}px`,
      '--nav-jelly-opacity': '1',
    },
  }
}

const updateIndicator = () => {
  nextTick(() => {
    requestAnimationFrame(() => {
      const metrics = readIndicatorMetrics()

      if (metrics.active) {
        navIndicatorStyle.value = metrics.style
        activeNavKind.value = metrics.kind
      } else {
        activeNavKind.value = null
        navIndicatorStyle.value = {
          '--nav-jelly-x': '0px',
          '--nav-jelly-y': '0px',
          '--nav-jelly-w': '0px',
          '--nav-jelly-h': '0px',
          '--nav-jelly-opacity': '0',
        }
      }
    })
  })
}

const scheduleIndicatorUpdate = (delay = 0) => {
  if (indicatorRefreshTimer) {
    clearTimeout(indicatorRefreshTimer)
    indicatorRefreshTimer = null
  }

  if (delay <= 0) {
    updateIndicator()
    return
  }

  indicatorRefreshTimer = setTimeout(() => {
    updateIndicator()
    indicatorRefreshTimer = null
  }, delay)
}

const handleSidebarTransitionEnd = (event: TransitionEvent) => {
  if (event.target !== sidebarRoot.value || event.propertyName !== 'width') {
    return
  }

  updateIndicator()
}

const handleNavClick = () => {
  mobileOpen.value = false
}

const handleBrandClick = (event: MouseEvent) => {
  if (sidebarCollapsed.value) {
    event.preventDefault()
    toggleSidebar()
    return
  }

  mobileOpen.value = false
}

const openLogoutConfirm = () => {
  showLogoutConfirm.value = true
}

const closeLogoutConfirm = () => {
  showLogoutConfirm.value = false
}

const confirmLogout = () => {
  closeLogoutConfirm()
  userStore.logout()
  mobileOpen.value = false
  router.push('/')
}

watch(
  [() => route.path, sidebarCollapsed, () => userStore.isLoggedIn, () => userStore.isAdmin],
  () => {
    updateIndicator()
  },
  { flush: 'post' },
)

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
  min-width: 0;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius-md);
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
  transition: width var(--transition-normal);
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
  overflow-x: hidden;
  position: relative;
}

.brand-block {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 0 4px var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.brand-text {
  display: flex;
  min-width: 0;
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

.sidebar-collapse-btn {
  display: inline-flex;
  flex: 0 0 auto;
  width: 24px;
  height: 24px;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: color-mix(in srgb, var(--bg-secondary) 82%, transparent);
  color: var(--text-muted);
  cursor: pointer;
  box-shadow: none;
  transition: all var(--transition-fast);
}

.sidebar-collapse-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-color-strong);
  background: var(--bg-tertiary);
  transform: translateY(-1px);
}

.nav-list {
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  padding: var(--spacing-md) 0 0;
}

.nav-track {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-jelly-block {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
  width: var(--nav-jelly-w);
  height: var(--nav-jelly-h);
  opacity: var(--nav-jelly-opacity, 1);
  border-radius: var(--border-radius-md);
  background: var(--bg-tertiary);
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--border-color) 72%, transparent);
  transform: translate(var(--nav-jelly-x), var(--nav-jelly-y)) scale(1);
  transform-origin: center;
  transition:
    transform 420ms cubic-bezier(0.2, 1.48, 0.34, 1),
    width 260ms cubic-bezier(0.2, 1, 0.36, 1),
    height 260ms cubic-bezier(0.2, 1, 0.36, 1),
    opacity var(--transition-fast),
    background-color var(--transition-fast),
    box-shadow var(--transition-fast);
  will-change: transform, width, height;
}

.nav-jelly-block.admin {
  background: color-mix(in srgb, var(--bg-tertiary) 88%, var(--color-pro));
}

@media (prefers-reduced-motion: reduce) {
  .nav-jelly-block {
    transition-duration: 0ms;
  }
}

.admin-nav {
  flex: 0;
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-md) 0 var(--spacing-xs);
  margin-top: var(--spacing-md);
  background: transparent;
  border-radius: 0;
}

.nav-divider {
  display: block;
  padding: 0 12px 7px;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  text-align: left;
}

.nav-item {
  display: block;
  box-sizing: border-box;
  text-decoration: none;
  border: 0;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 14px;
  transition: background-color var(--transition-fast), color var(--transition-fast);
  position: relative;
  z-index: 1;
}

.nav-item-inner {
  display: flex;
  min-height: 36px;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  padding: 0 11px;
}

.nav-item-inner span {
  white-space: nowrap;
  line-height: 1;
}

.nav-icon {
  flex: 0 0 20px;
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
  background: transparent;
  font-weight: 700;
}

.nav-item.active::before {
  display: none;
}

.nav-item.active .nav-icon {
  color: var(--text-primary);
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
  margin-top: auto;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.legal-links {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  width: 100%;
  padding: 0 4px;
}

.legal-link {
  flex: 1 1 0;
  color: var(--text-muted);
  font-size: 11px;
  text-align: center;
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
  flex: 0 0 auto;
  color: var(--border-color);
  font-size: 11px;
}

.user-card {
  display: flex;
  gap: 8px;
  align-items: center;
  width: 100%;
  min-width: 0;
  overflow: hidden;
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
  flex: 0 0 30px;
  width: 30px;
  height: 30px;
  border-radius: var(--border-radius-full);
  border: 1px solid var(--border-color);
}

.user-info {
  display: flex;
  flex: 1 1 auto;
  min-width: 0;
  overflow: hidden;
  flex-direction: column;
}

.user-info strong {
  display: block;
  width: 100%;
  min-width: 0;
  overflow: hidden;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-info small {
  display: block;
  width: 100%;
  min-width: 0;
  overflow: hidden;
  color: var(--text-muted);
  font-size: 11px;
  line-height: 1.35;
  text-overflow: ellipsis;
  white-space: nowrap;
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

.login-icon {
  flex: 0 0 auto;
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

.logout-confirm-backdrop {
  position: fixed;
  inset: 0;
  z-index: 120;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
  background: rgba(15, 23, 42, 0.42);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.logout-confirm-modal {
  display: grid;
  width: min(420px, 100%);
  grid-template-columns: 40px 1fr;
  gap: 12px;
  padding: 18px;
}

.logout-confirm-icon {
  display: inline-flex;
  width: 40px;
  height: 40px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  color: var(--color-danger);
  background: var(--color-danger-soft);
  border: 1px solid rgba(239, 68, 68, 0.18);
}

.logout-confirm-copy {
  min-width: 0;
}

.logout-confirm-copy h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 17px;
  font-weight: 800;
  line-height: 1.25;
}

.logout-confirm-copy p {
  margin: 6px 0 0;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.5;
}

.logout-confirm-actions {
  display: flex;
  grid-column: 1 / -1;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 4px;
}

.logout-confirm-enter-active,
.logout-confirm-leave-active {
  transition: opacity var(--transition-fast);
}

.logout-confirm-enter-active .logout-confirm-modal,
.logout-confirm-leave-active .logout-confirm-modal {
  transition: transform var(--transition-fast), opacity var(--transition-fast);
}

.logout-confirm-enter-from,
.logout-confirm-leave-to {
  opacity: 0;
}

.logout-confirm-enter-from .logout-confirm-modal,
.logout-confirm-leave-to .logout-confirm-modal {
  opacity: 0;
  transform: translateY(8px) scale(0.98);
}

.sidebar.collapsed .sidebar-panel {
  padding-right: 10px;
  padding-left: 10px;
}

.sidebar.collapsed .brand-block {
  justify-content: center;
  padding-right: 0;
  padding-left: 0;
}

.sidebar.collapsed .brand {
  width: 44px;
  height: 40px;
  justify-content: center;
}

.sidebar.collapsed .brand:hover {
  background: var(--bg-tertiary);
}

.sidebar.collapsed .sidebar-collapse-btn {
  position: absolute;
  top: 20px;
  left: 50%;
  z-index: 2;
  display: inline-flex;
  opacity: 0;
  pointer-events: none;
  transform: translate(-50%, -50%) scale(0.92);
}

.sidebar.collapsed .brand-block:hover .sidebar-collapse-btn {
  opacity: 1;
  pointer-events: auto;
  transform: translate(-50%, -50%) scale(1);
}

.sidebar.collapsed .sidebar-collapse-btn:hover {
  transform: translate(-50%, -50%) scale(1);
}

.sidebar.collapsed .brand-text,
.sidebar.collapsed .nav-item-inner span,
.sidebar.collapsed .nav-divider,
.sidebar.collapsed .legal-links,
.sidebar.collapsed .theme-label span,
.sidebar.collapsed .theme-toggle-switch,
.sidebar.collapsed .user-info,
.sidebar.collapsed .logout-btn span,
.sidebar.collapsed .login-btn span {
  display: none;
}

.sidebar.collapsed .nav-list {
  align-items: center;
}

.sidebar.collapsed .admin-nav {
  width: 100%;
  align-items: center;
}

.sidebar.collapsed .nav-item {
  width: 44px;
}

.sidebar.collapsed .nav-item-inner {
  min-height: 36px;
  justify-content: center;
  padding: 0;
}

.sidebar.collapsed .nav-track {
  gap: 6px;
}

.sidebar.collapsed .nav-icon {
  flex-basis: 20px;
}

.sidebar.collapsed .sidebar-footer {
  align-items: center;
}

.sidebar.collapsed .theme-toggle-row,
.sidebar.collapsed .user-card,
.sidebar.collapsed .login-btn,
.sidebar.collapsed .logout-btn {
  width: 44px;
  min-height: 40px;
  justify-content: center;
  padding: 0;
}

.sidebar.collapsed .theme-toggle-row {
  display: none;
}

.sidebar.collapsed .login-btn {
  display: inline-flex;
  color: var(--text-secondary);
  background: var(--bg-inset);
  border: 1px solid var(--border-color);
}

.sidebar.collapsed .user-card {
  border-radius: var(--border-radius-lg);
}

.sidebar.collapsed .avatar {
  flex-basis: 28px;
  width: 28px;
  height: 28px;
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

  .sidebar.collapsed .sidebar-panel {
    padding: 18px 12px;
  }

  .sidebar.collapsed .brand-block {
    justify-content: space-between;
    padding: 0 6px var(--spacing-md);
  }

  .sidebar.collapsed .brand {
    width: auto;
    height: auto;
    justify-content: flex-start;
  }

  .sidebar.collapsed .brand-text,
  .sidebar.collapsed .nav-item-inner span,
  .sidebar.collapsed .nav-divider,
  .sidebar.collapsed .legal-links,
  .sidebar.collapsed .theme-label span,
  .sidebar.collapsed .theme-toggle-switch,
  .sidebar.collapsed .user-info,
  .sidebar.collapsed .logout-btn span,
  .sidebar.collapsed .login-btn {
    display: initial;
  }

  .sidebar.collapsed .brand-text,
  .sidebar.collapsed .user-info,
  .sidebar.collapsed .theme-label {
    display: flex;
  }

  .sidebar.collapsed .nav-divider {
    display: block;
  }

  .sidebar.collapsed .legal-links,
  .sidebar.collapsed .theme-toggle-row,
  .sidebar.collapsed .logout-btn,
  .sidebar.collapsed .login-btn {
    display: flex;
  }

  .sidebar.collapsed .nav-list,
  .sidebar.collapsed .admin-nav,
  .sidebar.collapsed .sidebar-footer {
    align-items: stretch;
  }

  .sidebar.collapsed .nav-item,
  .sidebar.collapsed .theme-toggle-row,
  .sidebar.collapsed .user-card,
  .sidebar.collapsed .logout-btn {
    width: auto;
  }

  .sidebar.collapsed .nav-item-inner {
    justify-content: flex-start;
    padding: 0 10px;
  }

  .sidebar-collapse-btn {
    display: none;
  }

  .sidebar.collapsed .sidebar-collapse-btn {
    display: none;
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
:global([data-theme="dark"] .nav-item:hover ){
  background: rgba(255, 255, 255, 0.08);
  color: #f9fafb;
}

:global([data-theme="dark"] .nav-item.active ){
  background: transparent;
  color: #ffffff;
}

:global([data-theme="dark"] .nav-jelly-block ){
  background: rgba(255, 255, 255, 0.13);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.06);
}

:global([data-theme="dark"] .nav-jelly-block.admin ){
  background: rgba(167, 139, 250, 0.18);
  box-shadow: inset 0 0 0 1px rgba(167, 139, 250, 0.12);
}

:global([data-theme="dark"] .nav-item:hover .nav-icon ),
:global([data-theme="dark"] .nav-item.active .nav-icon ){
  color: #ffffff;
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
