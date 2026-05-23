<template>
  <div class="app-layout">
    <!-- Left Sidebar Navigation -->
    <Sidebar />
    
    <!-- Right Main Content Scroll Area -->
    <div class="main-wrapper">
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <Footer />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import Sidebar from './components/layout/Sidebar.vue'
import Footer from './components/layout/Footer.vue'
import { useUserStore } from './stores/user'

const userStore = useUserStore()

onMounted(() => {
  userStore.init()
})
</script>

<style>
/* Layout styling */
.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-primary);
}

.main-wrapper {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding-left: 248px;
  min-height: 100vh;
  width: 100%;
}

.main-content {
  flex-grow: 1;
  padding: var(--spacing-xl) 0 var(--spacing-xxl);
}

/* Global transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive spacing */
@media (max-width: 768px) {
  .main-wrapper {
    padding-left: 0;
    padding-top: 56px;
  }
  .main-content {
    padding: var(--spacing-lg) 0;
  }
}
</style>
