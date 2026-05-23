<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div>
        <router-link to="/" class="footer-brand">BusGPT</router-link>
        <p>商品展示与联系方式解锁服务。平台不提供站内聊天，也不代收订阅费用。</p>
      </div>
      <div class="footer-links">
        <router-link to="/market">发现车位</router-link>
        <router-link to="/create">发布车位</router-link>
        <router-link to="/profile">我的解锁</router-link>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: auto;
  padding: var(--spacing-xl) 0;
  border-top: 1px solid var(--border-color);
  background: rgba(255, 255, 255, 0.72);
}

.footer-inner {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-lg);
}

.footer-brand {
  display: inline-block;
  margin-bottom: 8px;
  color: var(--text-primary);
  font-size: 18px;
  font-weight: 900;
}

p,
.footer-links a {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.7;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.footer-links a {
  font-weight: 700;
}

@media (max-width: 720px) {
  .footer-inner {
    flex-direction: column;
  }
}
</style>
