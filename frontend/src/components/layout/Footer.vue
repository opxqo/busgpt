<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-info">
        <router-link to="/" class="footer-brand">BusGPT</router-link>
        <p class="footer-desc">AI 订阅拼车信息聚合平台。平台不提供站内聊天，也不代收订阅费用。</p>
      </div>
      <div class="footer-links">
        <router-link to="/market" class="footer-link">发现车位</router-link>
        <router-link to="/create" class="footer-link">发布车位</router-link>
        <router-link to="/profile" class="footer-link">个人中心</router-link>
      </div>
    </div>
    <div class="container footer-bottom">
      <p class="copyright">&copy; {{ new Date().getFullYear() }} BusGPT. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: auto;
  padding: var(--spacing-xl) 0 var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.footer-inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-lg);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.footer-info {
  max-width: 480px;
}

.footer-brand {
  display: inline-block;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 800;
  text-decoration: none;
  letter-spacing: -0.01em;
}

.footer-desc {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xs);
}

.footer-link {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer-link:hover {
  color: var(--text-primary);
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
}

@media (max-width: 720px) {
  .footer-inner {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  .footer-links {
    gap: var(--spacing-sm);
  }
}
</style>
