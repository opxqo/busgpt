# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目简介

BusGPT 是一个 AI 订阅拼车平台，主要面向 ChatGPT Plus、Team、Pro 订阅。"Bus"即"拼车"。平台展示车位信息，用户付费后可查看车主联系方式。平台仅提供信息展示和联系方式解锁服务，不涉及站内聊天或订阅代付。

## 仓库结构

前后端分离的 monorepo，无根目录配置文件：

- `backend/` — Python FastAPI + SQLAlchemy + MySQL 后端
- `frontend/` — Vue 3 + Vite + TypeScript 前端 SPA

## 常用命令

### 后端

```bash
cd backend
source .venv/bin/activate          # Python 3.9 虚拟环境
pip install -r requirements.txt    # 安装依赖
uvicorn app.main:app --reload      # 启动开发服务器 (http://127.0.0.1:8000)
python init_db.py                  # 手动初始化数据库（启动时也会自动执行）
```

后端启动时通过 `database.py` 的 `init_db()` 自动建表并写入初始产品数据。

### 前端

```bash
cd frontend
npm install
npm run dev          # Vite 开发服务器
npm run build        # 类型检查 + 生产构建
npm run lint         # oxlint + eslint（均带 --fix）
npm run format       # prettier 格式化 src/
npm run type-check   # vue-tsc --build
```

Node.js 版本要求：^20.19.0 或 >= 22.12.0。

## 架构

### 后端 (FastAPI)

分层结构：`routers/` → `schemas/` → `models/` → `database.py`

- **入口：** `app/main.py` — FastAPI 应用，CORS 允许所有来源，路由注册在 `/api` 前缀下
- **配置：** `app/config.py` — Pydantic Settings，从 `.env` 读取（MySQL 连接、JWT 密钥/过期时间）
- **数据库：** `app/database.py` — 双引擎：async (aiomysql) 处理 API 请求，sync (pymysql) 用于启动/管理任务；`get_db()` 异步依赖注入；`init_db()` 建库建表并执行轻量级列迁移
- **认证：** 手机号 + 密码 → bcrypt 哈希 → JWT (HS256, 7天有效期)，通过 `Authorization: Bearer` 头传递。`routers/auth.py` 中的 `get_current_user` 依赖被其他路由复用
- **核心业务逻辑：** 车位的 `contact_info` 默认隐藏，仅车主本人或已付款用户可查看

数据表：`users`、`products`、`rides`、`orders`、`ride_members`（已定义但未使用，预留功能）

### 前端 (Vue 3)

- **布局：** `App.vue` — 固定左侧边栏 (`components/layout/Sidebar.vue`) + `<router-view>` + 页脚
- **路由：** `router/index.ts` — 受保护路由通过导航守卫跳转到 `/login`
- **状态管理：** Pinia stores (`stores/`) — `user.ts` (认证状态)、`rides.ts` (列表和产品)
- **API 层：** `api/client.ts` — Axios 实例，默认地址 `http://127.0.0.1:8000/api`（可通过 `VITE_API_URL` 覆盖），请求拦截自动附加 Bearer token，401 响应自动清除登录态
- **样式：** 纯 CSS + CSS 自定义属性（`styles/variables.css`），无 Tailwind。产品配色：绿=Plus，蓝=Team，琥珀=Pro

## 约定

- **前端代码风格：** 无分号、单引号、100 字符宽（Prettier）；2 空格缩进；LF 换行
- **Lint 顺序：** oxlint 先行，再 ESLint（flat config，集成 Vue + TypeScript + Prettier）
- **后端配置：** 所有密钥/连接串通过 `.env` 文件（参考 `backend/.env.example`）
- **API 前缀：** 所有后端路由统一在 `/api` 下

## 注意事项

- 项目无测试基础设施
- Alembic 列为依赖但未实际使用，迁移由 `database.py` 的 `_run_lightweight_migrations()` 在启动时自动添加缺失列
- 前端 `src/` 中残留多处模板脚手架文件（`HomeView.vue`、`AboutView.vue`、`HelloWorld.vue`、`counter.ts`、icon 组件等），未被使用
- `ride_members` 模型已定义但无路由引用
