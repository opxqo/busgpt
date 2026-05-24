# BusGPT Zeabur Deployment

This repo is a monorepo. Deploy the backend and frontend as separate Zeabur services.

## Backend Service

Recommended service name: `busgpt`

Use either setup:

1. Root Directory: `/backend`
   - Zeabur will use `backend/Dockerfile`.
2. Root Directory: `/`
   - Zeabur can auto-match `Dockerfile.busgpt` when the service name is `busgpt`.

Do not use a Node.js Dockerfile or `npm start` for the backend.

Leave ENTRYPOINT and CMD overrides empty unless you are intentionally overriding the Dockerfile.
The Dockerfile starts:

```bash
scripts/start.sh
```

The app listens on Zeabur's runtime `PORT` environment variable.

Required environment variables:

```env
ENVIRONMENT=production
DATABASE_URL=mysql+pymysql://root:<password>@175.178.102.49:31921/zeabur
BACKEND_CORS_ORIGINS=https://busgpt.opxqo.com
FRONTEND_URL=https://busgpt.opxqo.com
BACKEND_URL=https://busgpt.opxqo.com
SECRET_KEY=<openssl rand -hex 32>
PAYMENT_PROVIDER=mock
MOCK_PAYMENT_ENABLED=true
ORDER_EXPIRE_MINUTES=30
SMTP_FROM_NAME=BusGPT
SMTP_HOST=smtp.qiye.aliyun.com
SMTP_PASSWORD=<smtp-password>
SMTP_PORT=465
SMTP_USE_SSL=true
SMTP_USERNAME=postmaster@luotao.qzz.io
```

After deployment, check:

```text
/api/health
/api/health/ready
```

Runtime logs should include:

```text
[busgpt] Starting backend
BusGPT backend startup begins
Deployment diagnostics: ...
Running database initialization on startup
Database initialization completed
```

If the container restarts before those lines appear, Zeabur is not running this backend Dockerfile or a command override is still wrong.

## Frontend Service

Root Directory: `/frontend`

Build Command:

```bash
npm ci && npm run build
```

Output Directory:

```text
dist
```

Frontend environment:

```env
VITE_API_URL=https://<backend-domain>/api
```

If the frontend and backend are routed through the same domain with `/api` proxying to the backend, use:

```env
VITE_API_URL=/api
```
