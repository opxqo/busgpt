<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-info">
        <router-link to="/" class="footer-brand">
          <span class="footer-logo-mark">
            <Car :size="16" stroke-width="2.4" />
          </span>
          <span>BusGPT</span>
        </router-link>
        <p class="footer-desc">AI 订阅拼车信息聚合平台。平台不提供站内聊天，也不代收订阅费用。</p>
      </div>
      <div class="footer-links-group">
        <div class="footer-col">
          <span class="footer-col-title">平台</span>
          <router-link to="/market" class="footer-link">发现车位</router-link>
          <router-link to="/create" class="footer-link">发布车位</router-link>
          <router-link to="/profile" class="footer-link">个人中心</router-link>
        </div>
        <div class="footer-col">
          <span class="footer-col-title">法律</span>
          <a href="/privacy-policy.html" class="footer-link">隐私政策</a>
          <a href="/platform-spec.html" class="footer-link">平台规范</a>
        </div>
      </div>
    </div>
    <div class="container footer-bottom">
      <p class="copyright">&copy; {{ new Date().getFullYear() }} BusGPT. All rights reserved.</p>
      <a href="https://beian.miit.gov.cn/" target="_blank" rel="noopener noreferrer" class="icp-link">鄂ICP备2023027796号-5</a>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { Car } from '@lucide/vue'
</script>

<style scoped>
.footer {
  margin-top: auto;
  padding: var(--spacing-xl) 0 var(--spacing-lg);
  border-top: none;
  background: var(--bg-secondary);
  position: relative;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--border-color-strong);
  opacity: 0.5;
}

.footer-inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-xxl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.footer-info {
  max-width: 420px;
}

.footer-brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 800;
  text-decoration: none;
  letter-spacing: -0.01em;
  transition: opacity var(--transition-fast);
}

.footer-brand:hover {
  opacity: 0.8;
}

.footer-brand:hover .footer-logo-mark {
  transform: rotate(-5deg) scale(1.05);
}

.footer-logo-mark {
  display: inline-flex;
  width: 28px;
  height: 28px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-sm);
  background: var(--text-primary);
  color: var(--bg-primary);
  transition: transform var(--transition-fast);
}

.footer-desc {
  color: var(--text-muted);
  font-size: 13px;
  line-height: 1.6;
  margin: 0;
}

.footer-links-group {
  display: flex;
  gap: var(--spacing-xxl);
}

.footer-col {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.footer-col-title {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: var(--spacing-xs);
}

.footer-link {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: color var(--transition-fast);
  position: relative;
  display: inline-block;
}

.footer-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--text-primary);
  transform: scaleX(0);
  transform-origin: center;
  transition: transform var(--transition-fast);
}

.footer-link:hover {
  color: var(--text-primary);
}

.footer-link:hover::after {
  transform: scaleX(1);
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-md);
}

.copyright {
  color: var(--text-muted);
  font-size: 12px;
  margin: 0;
}

.icp-link {
  color: var(--text-muted);
  font-size: 12px;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.icp-link:hover {
  color: var(--text-secondary);
}

/* Dark mode */
:global([data-theme="dark"] .footer ){
  background: var(--bg-secondary);
}

:global([data-theme="dark"] .footer::before ){
  opacity: 0.3;
}

@media (max-width: 720px) {
  .footer-inner {
    flex-direction: column;
    gap: var(--spacing-lg);
  }
  .footer-links-group {
    gap: var(--spacing-xl);
  }
}
</style>
