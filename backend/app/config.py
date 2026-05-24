from pathlib import Path
from typing import Any, Optional

from sqlalchemy.engine import URL, make_url
from pydantic_settings import BaseSettings

BACKEND_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    PROJECT_NAME: str = "BusGPT"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Database configuration
    DATABASE_URL: Optional[str] = None
    ASYNC_DATABASE_URL: Optional[str] = None
    ROOT_DATABASE_URL: Optional[str] = None
    DB_HOST: str = "127.0.0.1"
    DB_PORT: str = "3306"
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "busgpt"
    
    # JWT authentication configuration
    SECRET_KEY: str = "supersecretkeyforbusgptsessiontokens12345!@#%"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ADMIN_PHONES: str = ""
    ADMIN_EMAILS: str = ""
    BACKEND_CORS_ORIGINS: str = "http://127.0.0.1:5173,http://localhost:5173,http://127.0.0.1:5174,http://localhost:5174,http://127.0.0.1:3000,http://localhost:3000"

    # SMTP email configuration
    SMTP_HOST: str = "smtp.qiye.aliyun.com"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_NAME: str = "BusGPT"
    SMTP_USE_SSL: bool = True

    # URLs used by email activation links
    BACKEND_URL: str = "http://127.0.0.1:8000"
    FRONTEND_URL: str = "http://127.0.0.1:5173"

    # Payment configuration
    PAYMENT_PROVIDER: str = "mock"
    MOCK_PAYMENT_ENABLED: bool = True
    ORDER_EXPIRE_MINUTES: int = 30

    @property
    def admin_phone_set(self) -> set[str]:
        return {phone.strip() for phone in self.ADMIN_PHONES.split(",") if phone.strip()}

    @property
    def admin_email_set(self) -> set[str]:
        return {email.strip().lower() for email in self.ADMIN_EMAILS.split(",") if email.strip()}

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

    def validate_security_settings(self) -> None:
        if self.ENVIRONMENT.lower() == "test":
            return
        default_secret = "supersecretkeyforbusgptsessiontokens12345!@#%"
        if self.SECRET_KEY == default_secret or len(self.SECRET_KEY) < 32:
            raise RuntimeError("SECRET_KEY must be replaced with a strong random value")

    def deployment_diagnostics(self) -> dict[str, Any]:
        db_url = make_url(self.sync_database_url)
        root_url = make_url(self.root_sync_database_url)
        return {
            "environment": self.ENVIRONMENT,
            "api_prefix": self.API_V1_STR,
            "database_driver": db_url.drivername,
            "database_host": db_url.host,
            "database_port": db_url.port,
            "database_name": db_url.database,
            "root_database_driver": root_url.drivername,
            "root_database_host": root_url.host,
            "root_database_port": root_url.port,
            "cors_origins": self.cors_origins,
            "frontend_url": self.FRONTEND_URL,
            "backend_url": self.BACKEND_URL,
            "payment_provider": self.PAYMENT_PROVIDER,
            "mock_payment_enabled": self.MOCK_PAYMENT_ENABLED,
            "order_expire_minutes": self.ORDER_EXPIRE_MINUTES,
            "smtp_host": self.SMTP_HOST,
            "smtp_port": self.SMTP_PORT,
            "smtp_use_ssl": self.SMTP_USE_SSL,
            "smtp_username_configured": bool(self.SMTP_USERNAME),
            "smtp_password_configured": bool(self.SMTP_PASSWORD),
            "secret_key_configured": bool(self.SECRET_KEY),
            "secret_key_length": len(self.SECRET_KEY),
            "admin_email_count": len(self.admin_email_set),
            "admin_phone_count": len(self.admin_phone_set),
        }

    def _fallback_mysql_url(self, database: Optional[str] = None) -> URL:
        return URL.create(
            "mysql+pymysql",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=int(self.DB_PORT),
            database=database,
        )

    @staticmethod
    def _sync_to_async_url(database_url: str) -> str:
        url = make_url(database_url)
        driver_map = {
            "mysql": "mysql+aiomysql",
            "mysql+pymysql": "mysql+aiomysql",
            "sqlite": "sqlite+aiosqlite",
            "sqlite+pysqlite": "sqlite+aiosqlite",
        }
        return url.set(drivername=driver_map.get(url.drivername, url.drivername)).render_as_string(hide_password=False)

    @staticmethod
    def _database_name(database_url: str) -> str:
        return make_url(database_url).database or ""

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return self._fallback_mysql_url(self.DB_NAME).render_as_string(hide_password=False)

    @property
    def async_database_url(self) -> str:
        if self.ASYNC_DATABASE_URL:
            return self.ASYNC_DATABASE_URL
        return self._sync_to_async_url(self.sync_database_url)
        
    @property
    def root_sync_database_url(self) -> str:
        # Used to create MySQL database if it doesn't exist.
        if self.ROOT_DATABASE_URL:
            return self.ROOT_DATABASE_URL
        url = make_url(self.sync_database_url)
        if not url.drivername.startswith("mysql"):
            return self.sync_database_url
        return url.set(database="").render_as_string(hide_password=False)

    @property
    def database_name(self) -> str:
        return self._database_name(self.sync_database_url) or self.DB_NAME

    class Config:
        env_file = str(BACKEND_DIR / ".env")
        case_sensitive = True

settings = Settings()
