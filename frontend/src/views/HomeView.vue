<template>
  <div class="home-page">
    <!-- Hero ambient -->
    <div class="hero-ambient" aria-hidden="true">
      <div class="ambient-orb orb-plus"></div>
      <div class="ambient-orb orb-team"></div>
      <div class="ambient-orb orb-pro"></div>
    </div>

    <!-- Hero Section -->
    <section class="hero container">
      <div class="hero-content anim-fade-up">
        <span class="eyebrow">AI 订阅拼车平台</span>
        <h1 class="hero-title">
          分摊订阅费用<br />
          <span class="hero-gradient">共享 AI 能力</span>
        </h1>
        <p class="hero-subtitle">
          BusGPT 汇聚 ChatGPT Plus、Business、Pro 拼车车位，帮你以更低成本获得完整的 AI 订阅体验。查看车主联系方式，直接沟通拼车。
        </p>
        <div class="hero-actions">
          <router-link to="/market" class="btn btn-primary btn-lg">
            <Search :size="18" />
            <span>发现车位</span>
          </router-link>
          <router-link to="/create" class="btn btn-secondary btn-lg">
            <PlusCircle :size="18" />
            <span>发布车位</span>
          </router-link>
        </div>
        <div class="hero-stats">
          <div class="hero-stat">
            <strong>{{ stats.totalRides }}</strong>
            <span>展示车位</span>
          </div>
          <span class="hero-stat-sep"></span>
          <div class="hero-stat">
            <strong>{{ stats.totalSeats }}</strong>
            <span>总拼车座位</span>
          </div>
          <span class="hero-stat-sep"></span>
          <div class="hero-stat">
            <strong>{{ stats.avgPrice }}</strong>
            <span>均 ¥/月</span>
          </div>
        </div>
      </div>
      <div class="hero-visual anim-fade-up anim-d1">
        <div class="hero-card-stack">
          <div class="hero-card hc-1">
            <span class="product-chip chatgpt-plus">
              <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor"><path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" /></svg>
              <span>Plus 拼车</span>
            </span>
            <strong class="hc-price">¥35<small>/月</small></strong>
            <div class="hc-bar"><div class="hc-fill" style="width: 66%"></div></div>
            <span class="hc-meta">2/3 人已拼</span>
          </div>
          <div class="hero-card hc-2">
            <span class="product-chip chatgpt-team">
              <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor"><path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" /></svg>
              <span>Business 团队</span>
            </span>
            <strong class="hc-price">¥28<small>/月</small></strong>
            <div class="hc-bar"><div class="hc-fill hc-fill-team" style="width: 40%"></div></div>
            <span class="hc-meta">2/5 人已拼</span>
          </div>
          <div class="hero-card hc-3">
            <span class="product-chip chatgpt-pro">
              <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor"><path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" /></svg>
              <span>Pro 极客</span>
            </span>
            <strong class="hc-price">¥90<small>/月</small></strong>
            <div class="hc-bar"><div class="hc-fill hc-fill-pro" style="width: 25%"></div></div>
            <span class="hc-meta">1/4 人已拼</span>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="how-it-works container anim-fade-up anim-d2">
      <span class="eyebrow">使用流程</span>
      <h2 class="section-title">三步完成拼车</h2>
      <div class="steps-grid">
        <div class="step-card surface-card">
          <span class="step-num">1</span>
          <div class="step-icon-wrap step-icon-plus">
            <Search :size="22" />
          </div>
          <h3>挑选车位</h3>
          <p>浏览市场中展示的拼车车位，按产品类型、价格和进度筛选合适的订阅。</p>
        </div>
        <div class="step-arrow" aria-hidden="true">
          <ChevronRight :size="20" />
        </div>
        <div class="step-card surface-card">
          <span class="step-num">2</span>
          <div class="step-icon-wrap step-icon-team">
            <MessageCircle :size="22" />
          </div>
          <h3>联系车主</h3>
          <p>免费解锁车主联系方式，添加微信或 Telegram 沟通拼车细节和付款方式。</p>
        </div>
        <div class="step-arrow" aria-hidden="true">
          <ChevronRight :size="20" />
        </div>
        <div class="step-card surface-card">
          <span class="step-num">3</span>
          <div class="step-icon-wrap step-icon-pro">
            <Sparkles :size="22" />
          </div>
          <h3>开始使用</h3>
          <p>车主邀请您加入团队或共享账号，即可享受完整的 ChatGPT 订阅能力。</p>
        </div>
      </div>
    </section>

    <!-- Product Showcase -->
    <section class="products-section container anim-fade-up anim-d3">
      <span class="eyebrow">支持产品</span>
      <h2 class="section-title">覆盖全系 ChatGPT 订阅</h2>
      <div class="products-grid">
        <div class="product-showcase-card surface-card" :class="'psc-plus'">
          <div class="psc-header">
            <span class="product-chip chatgpt-plus">
              <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor"><path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" /></svg>
              <span>ChatGPT Plus</span>
            </span>
          </div>
          <strong class="psc-price">$20/月</strong>
          <p class="psc-desc">GPT-5.5、深度研究、Agent 与 Codex，个人用户首选。</p>
          <ul class="psc-features">
            <li><Check :size="14" /> GPT-5.5 无限对话</li>
            <li><Check :size="14" /> 深度研究与推理</li>
            <li><Check :size="14" /> Agent 与 Codex</li>
          </ul>
        </div>
        <div class="product-showcase-card surface-card" :class="'psc-team'">
          <div class="psc-header">
            <span class="product-chip chatgpt-team">
              <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor"><path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" /></svg>
              <span>ChatGPT Business</span>
            </span>
          </div>
          <strong class="psc-price">$25/月</strong>
          <p class="psc-desc">Plus 全部能力、团队工作区、连接器与管理后台。</p>
          <ul class="psc-features">
            <li><Check :size="14" /> Plus 全部能力</li>
            <li><Check :size="14" /> 团队工作区与 GPTs</li>
            <li><Check :size="14" /> 管理后台与连接器</li>
          </ul>
        </div>
        <div class="product-showcase-card surface-card" :class="'psc-pro'">
          <div class="psc-header">
            <span class="product-chip chatgpt-pro">
              <svg viewBox="0 0 24 24" class="chip-logo" fill="currentColor"><path d="M9.205 8.658v-2.26c0-.19.072-.333.238-.428l4.543-2.616c.619-.357 1.356-.523 2.117-.523 2.854 0 4.662 2.212 4.662 4.566 0 .167 0 .357-.024.547l-4.71-2.759a.797.797 0 00-.856 0l-5.97 3.473zm10.609 8.8V12.06c0-.333-.143-.57-.429-.737l-5.97-3.473 1.95-1.118a.433.433 0 01.476 0l4.543 2.617c1.309.76 2.189 2.378 2.189 3.948 0 1.808-1.07 3.473-2.76 4.163zM7.802 12.703l-1.95-1.142c-.167-.095-.239-.238-.239-.428V5.899c0-2.545 1.95-4.472 4.591-4.472 1 0 1.927.333 2.712.928L8.23 5.067c-.285.166-.428.404-.428.737v6.898zM12 15.128l-2.795-1.57v-3.33L12 8.658l2.795 1.57v3.33L12 15.128zm1.796 7.23c-1 0-1.927-.332-2.712-.927l4.686-2.712c.285-.166.428-.404.428-.737v-6.898l1.974 1.142c.167.095.238.238.238.428v5.233c0 2.545-1.974 4.472-4.614 4.472zm-5.637-5.303l-4.544-2.617c-1.308-.761-2.188-2.378-2.188-3.948A4.482 4.482 0 014.21 6.327v5.423c0 .333.143.571.428.738l5.947 3.449-1.95 1.118a.432.432 0 01-.476 0zm-.262 3.9c-2.688 0-4.662-2.021-4.662-4.519 0-.19.024-.38.047-.57l4.686 2.71c.286.167.571.167.856 0l5.97-3.448v2.26c0 .19-.07.333-.237.428l-4.543 2.616c-.619.357-1.356.523-2.117.523zm5.899 2.83a5.947 5.947 0 005.827-4.756C22.287 18.339 24 15.84 24 13.296c0-1.665-.713-3.282-1.998-4.448.119-.5.19-.999.19-1.498 0-3.401-2.759-5.947-5.946-5.947-.642 0-1.26.095-1.88.31A5.962 5.962 0 0010.205 0a5.947 5.947 0 00-5.827 4.757C1.713 5.447 0 7.945 0 10.49c0 1.666.713 3.283 1.998 4.448-.119.5-.19 1-.19 1.499 0 3.401 2.759 5.946 5.946 5.946.642 0 1.26-.095 1.88-.309a5.96 5.96 0 004.162 1.713z" /></svg>
              <span>ChatGPT Pro</span>
            </span>
          </div>
          <strong class="psc-price">$200/月</strong>
          <p class="psc-desc">最高用量、GPT-5.5 Pro、扩展深度研究，面向重度用户。</p>
          <ul class="psc-features">
            <li><Check :size="14" /> GPT-5.5 Pro 无限量</li>
            <li><Check :size="14" /> 扩展深度研究</li>
            <li><Check :size="14" /> 最高优先级访问</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Trust Section -->
    <section class="trust-section container anim-fade-up anim-d4">
      <div class="trust-banner surface-card">
        <div class="trust-content">
          <ShieldCheck :size="28" class="trust-icon" />
          <div>
            <h2>安全透明的拼车环境</h2>
            <p>平台仅提供信息展示与联系方式解锁服务，不介入后续交易。所有车主均经平台实名认证，联系方式解锁后可直接沟通。</p>
          </div>
        </div>
        <router-link to="/market" class="btn btn-primary">
          <span>开始浏览车位</span>
          <ArrowRight :size="16" />
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { ArrowRight, Check, ChevronRight, MessageCircle, PlusCircle, Search, ShieldCheck, Sparkles } from '@lucide/vue'
import { ridesApi } from '../api/rides'

const rides = ref<Array<{ total_seats: number; price_per_month: number | string }>>([])

const stats = computed(() => {
  const total = rides.value.length
  const seats = rides.value.reduce((sum, r) => sum + Number(r.total_seats || 0), 0)
  const avg = total ? Math.round(rides.value.reduce((sum, r) => sum + Number(r.price_per_month || 0), 0) / total) : 0
  return { totalRides: total, totalSeats: seats, avgPrice: `¥${avg}` }
})

onMounted(async () => {
  try {
    const res = await ridesApi.getRides()
    rides.value = res.data?.rides || res.data || []
  } catch {
    // silent — stats show 0
  }
})
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xxl);
  padding-top: var(--spacing-xl);
  padding-bottom: var(--spacing-xxl);
  position: relative;
  overflow: hidden;
}

/* Hero ambient orbs */
.hero-ambient {
  position: absolute;
  top: -120px;
  left: 0;
  right: 0;
  height: 600px;
  pointer-events: none;
  overflow: hidden;
}

.ambient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.1;
}

.orb-plus {
  width: 500px;
  height: 500px;
  background: var(--color-plus);
  top: -100px;
  right: -80px;
  animation: orbFloat 25s ease-in-out infinite;
}

.orb-team {
  width: 350px;
  height: 350px;
  background: var(--color-team);
  top: 200px;
  left: -60px;
  animation: orbFloat 30s ease-in-out infinite reverse;
}

.orb-pro {
  width: 250px;
  height: 250px;
  background: var(--color-pro);
  top: 50px;
  left: 40%;
  animation: orbFloat 22s ease-in-out infinite 5s;
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(30px, -25px); }
  66% { transform: translate(-20px, 15px); }
}

/* ===== Animations ===== */
.anim-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.anim-d1 { animation-delay: 0.1s; }
.anim-d2 { animation-delay: 0.18s; }
.anim-d3 { animation-delay: 0.26s; }
.anim-d4 { animation-delay: 0.34s; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== Hero ===== */
.hero {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: var(--spacing-xl);
  align-items: center;
  min-height: 420px;
}

.hero-title {
  font-size: 44px;
  font-weight: 900;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin: var(--spacing-md) 0;
}

.hero-gradient {
  color: var(--color-team);
}

.hero-subtitle {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-secondary);
  max-width: 480px;
  margin-bottom: var(--spacing-lg);
}

.hero-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
}

.btn-lg {
  min-height: 48px;
  padding: 12px 24px;
  font-size: 15px;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.hero-stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.hero-stat strong {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
}

.hero-stat span {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
}

.hero-stat-sep {
  width: 1px;
  height: 32px;
  background: var(--border-color);
}

/* ===== Hero Card Stack ===== */
.hero-visual {
  position: relative;
  height: 360px;
}

.hero-card-stack {
  position: relative;
  width: 100%;
  height: 100%;
}

.hero-card {
  position: absolute;
  width: 280px;
  padding: var(--spacing-md);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--card-shadow);
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease;
  opacity: 0;
  animation: cardFloat 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.hero-card:hover {
  transform: translateY(-6px) scale(1.02) !important;
  box-shadow: var(--card-shadow-hover);
  z-index: 10;
}

.hc-1 {
  top: 0;
  left: 20px;
  transform: rotate(-3deg);
  z-index: 3;
  animation-delay: 0.2s;
}

.hc-2 {
  top: 60px;
  left: 80px;
  transform: rotate(1deg);
  z-index: 2;
  animation-delay: 0.4s;
}

.hc-3 {
  top: 120px;
  left: 40px;
  transform: rotate(-1.5deg);
  z-index: 1;
  animation-delay: 0.6s;
}

@keyframes cardFloat {
  from {
    opacity: 0;
    transform: translateY(30px) rotate(0deg);
  }
  to {
    opacity: 1;
  }
}

.hc-price {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
}

.hc-price small {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.hc-bar {
  height: 4px;
  border-radius: var(--border-radius-full);
  background: var(--bg-tertiary);
  overflow: hidden;
}

.hc-fill {
  height: 100%;
  border-radius: var(--border-radius-full);
  background: var(--color-plus);
  transition: width 1s cubic-bezier(0.22, 1, 0.36, 1);
}

.hc-fill-team { background: var(--color-team); }
.hc-fill-pro { background: var(--color-pro); }

.hc-meta {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
}

/* ===== How It Works ===== */
.how-it-works {
  text-align: center;
}

.section-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  margin: var(--spacing-xs) 0 var(--spacing-xl);
  letter-spacing: 0;
}

.steps-grid {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.step-card {
  flex: 1;
  padding: var(--spacing-lg);
  text-align: center;
  position: relative;
  transition: all var(--transition-fast);
}

.step-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--card-shadow-hover);
}

.step-num {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
  font-size: 48px;
  font-weight: 900;
  color: var(--bg-tertiary);
  line-height: 1;
}

.step-icon-wrap {
  display: inline-flex;
  width: 48px;
  height: 48px;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-lg);
  background: var(--color-plus-soft);
  color: var(--color-plus);
  margin-bottom: var(--spacing-md);
  transition: transform var(--transition-fast);
}

.step-card:hover .step-icon-wrap {
  transform: scale(1.08);
}

.step-icon-team {
  background: var(--color-team-soft);
  color: var(--color-team);
}

.step-icon-pro {
  background: var(--color-pro-soft);
  color: var(--color-pro);
}

.step-card h3 {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs);
}

.step-card p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.step-arrow {
  color: var(--text-muted);
  flex-shrink: 0;
}

/* ===== Products Section ===== */
.products-section {
  text-align: center;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--spacing-md);
}

.product-showcase-card {
  padding: var(--spacing-lg);
  text-align: left;
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.product-showcase-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-plus);
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.product-showcase-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: var(--color-plus);
  opacity: 0;
  filter: blur(50px);
  transition: opacity var(--transition-fast);
  pointer-events: none;
}

.product-showcase-card:hover::before {
  opacity: 1;
}

.product-showcase-card:hover::after {
  opacity: 0.08;
}

.product-showcase-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--card-shadow-hover);
}

.psc-team::after { background: var(--color-team); }
.psc-pro::after { background: var(--color-pro); }

.psc-team::before { background: var(--color-team); }
.psc-pro::before { background: var(--color-pro); }

.psc-header {
  margin-bottom: var(--spacing-md);
}

.psc-price {
  display: block;
  font-size: 28px;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.psc-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 var(--spacing-md);
}

.psc-features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.psc-features li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.psc-features li :deep(svg) {
  color: var(--color-success);
  flex-shrink: 0;
}

/* ===== Trust Section ===== */
.trust-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-lg);
  padding: var(--spacing-xl);
  background: var(--bg-card);
}

.trust-content {
  display: flex;
  gap: var(--spacing-md);
  align-items: flex-start;
}

.trust-icon {
  color: var(--color-success);
  flex-shrink: 0;
  margin-top: 2px;
}

.trust-content h2 {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs);
}

.trust-content p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  max-width: 520px;
}

/* ===== Dark Mode ===== */
:global([data-theme="dark"] .ambient-orb ){
  opacity: 0.06;
  filter: blur(120px);
}

:global([data-theme="dark"] .hero-card ){
  background: var(--bg-tertiary);
  border-color: var(--border-color-strong);
}

:global([data-theme="dark"] .step-card:hover ){
  box-shadow: 0 0 0 1px var(--border-color-strong);
}

:global([data-theme="dark"] .product-showcase-card ){
  background: var(--bg-tertiary);
}

:global([data-theme="dark"] .trust-banner ){
  background: var(--bg-tertiary);
}

:global([data-theme="dark"] .step-num ){
  color: var(--bg-tertiary);
  opacity: 0.6;
}

/* ===== Responsive ===== */
@media (max-width: 1080px) {
  .hero {
    grid-template-columns: 1fr;
    min-height: auto;
  }
  .hero-visual {
    display: none;
  }
  .hero-ambient {
    opacity: 0.5;
  }
}

@media (max-width: 768px) {
  .home-page {
    gap: var(--spacing-xl);
  }
  .hero-title {
    font-size: 32px;
  }
  .hero-actions {
    flex-direction: column;
  }
  .btn-lg {
    width: 100%;
  }
  .hero-stats {
    gap: var(--spacing-md);
  }
  .hero-stat strong {
    font-size: 18px;
  }
  .steps-grid {
    flex-direction: column;
  }
  .step-arrow {
    transform: rotate(90deg);
  }
  .products-grid {
    grid-template-columns: 1fr;
  }
  .trust-banner {
    flex-direction: column;
    align-items: flex-start;
  }
  .section-title {
    font-size: 22px;
  }
}

.chip-logo {
  width: 14px;
  height: 14px;
  object-fit: contain;
  flex-shrink: 0;
}
</style>
