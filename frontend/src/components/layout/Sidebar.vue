<template>
  <div class="mobile-top-bar">
    <router-link to="/" class="mobile-logo">
      <span class="logo-mark">B</span>
      <span>BusGPT</span>
    </router-link>
    <button class="icon-btn" type="button" aria-label="打开导航" @click="mobileOpen = true">
      <Menu :size="22" />
    </button>
  </div>

  <aside class="sidebar" :class="{ open: mobileOpen }">
    <button class="sidebar-scrim" type="button" aria-label="关闭导航" @click="mobileOpen = false"></button>
    <div class="sidebar-panel">
      <div class="brand-block">
        <router-link to="/" class="brand" @click="mobileOpen = false">
          <span class="logo-mark">B</span>
          <span class="brand-text">
            <strong>BusGPT</strong>
            <small>AI 订阅信息台</small>
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
          <component :is="item.icon" :size="18" />
          <span>{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="notice-card">
        <ShieldCheck :size="18" />
        <div>
          <strong>信息展示服务</strong>
          <p>平台仅展示车位信息，支付信息服务费后解锁联系方式。</p>
        </div>
      </div>

      <div class="sidebar-footer">
        <template v-if="userStore.isLoggedIn">
          <router-link to="/profile" class="user-card" @click="mobileOpen = false">
            <img :src="userStore.user?.avatar || defaultAvatar" alt="用户头像" class="avatar" />
            <span>
              <strong>{{ userStore.user?.nickname }}</strong>
              <small>我的解锁与发布</small>
            </span>
          </router-link>
          <button type="button" class="logout-btn" @click="handleLogout">
            <LogOut :size="16" />
            退出登录
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Boxes, Home, LogOut, Menu, PlusCircle, Search, ShieldCheck, UserRound } from '@lucide/vue'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()
const router = useRouter()
const mobileOpen = ref(false)
const defaultAvatar = 'https://api.dicebear.com/7.x/bottts/svg?seed=busgpt'

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
  background: rgba(255, 255, 255, 0.94);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(12px);
}

.mobile-logo,
.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
  font-weight: 800;
}

.logo-mark {
  display: inline-flex;
  width: 32px;
  height: 32px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  background: var(--text-primary);
  color: var(--text-inverse);
  font-size: 16px;
  font-weight: 900;
}

.icon-btn {
  display: inline-flex;
  width: 42px;
  height: 42px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
}

.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  z-index: 80;
  width: 248px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
}

.sidebar-scrim {
  display: none;
}

.sidebar-panel {
  display: flex;
  height: 100%;
  flex-direction: column;
  padding: var(--spacing-lg);
}

.brand-block {
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.brand-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-text small {
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
}

.nav-list {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 6px;
  padding: var(--spacing-lg) 0;
}

.nav-item {
  display: flex;
  min-height: 42px;
  align-items: center;
  gap: 10px;
  padding: 0 12px;
  border-radius: var(--border-radius-md);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 800;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

.nav-item:hover,
.nav-item.active {
  color: var(--text-primary);
  background: var(--bg-inset);
}

.nav-item.active {
  box-shadow: inset 3px 0 0 var(--color-primary);
}

.notice-card {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 10px;
  padding: 12px;
  border: 1px solid rgba(15, 106, 191, 0.18);
  border-radius: var(--border-radius-lg);
  background: var(--color-info-soft);
  color: var(--color-info);
}

.notice-card strong {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
}

.notice-card p {
  color: #315a78;
  font-size: 12px;
  line-height: 1.5;
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.user-card {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 10px;
  align-items: center;
  color: var(--text-primary);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
}

.user-card span {
  display: flex;
  min-width: 0;
  flex-direction: column;
}

.user-card strong {
  overflow: hidden;
  font-size: 13px;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-card small {
  color: var(--text-muted);
  font-size: 12px;
}

.login-btn,
.logout-btn {
  display: inline-flex;
  min-height: 40px;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: var(--border-radius-md);
  font-size: 13px;
  font-weight: 800;
}

.login-btn {
  color: var(--text-inverse);
  background: var(--color-primary);
}

.logout-btn {
  color: var(--text-secondary);
  background: var(--bg-inset);
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
  }

  .sidebar-scrim {
    display: block;
    position: fixed;
    inset: 0;
    opacity: 0;
    background: rgba(25, 31, 36, 0.28);
    transition: opacity var(--transition-normal);
  }

  .sidebar-panel {
    width: 286px;
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
</style>
