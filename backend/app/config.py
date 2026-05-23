from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BusGPT"
    API_V1_STR: str = "/api"
    ENVIRONMENT: str = "development"
    
    # Database configuration
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
    BACKEND_CORS_ORIGINS: str = "http://127.0.0.1:5173,http://localhost:5173,http://127.0.0.1:5174,http://localhost:5174,http://127.0.0.1:3000,http://localhost:3000"

    # Payment configuration
    PAYMENT_PROVIDER: str = "mock"
    MOCK_PAYMENT_ENABLED: bool = True
    ORDER_EXPIRE_MINUTES: int = 30

    @property
    def admin_phone_set(self) -> set[str]:
        return {phone.strip() for phone in self.ADMIN_PHONES.split(",") if phone.strip()}

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

    def validate_security_settings(self) -> None:
        if self.ENVIRONMENT.lower() == "test":
            return
        default_secret = "supersecretkeyforbusgptsessiontokens12345!@#%"
        if self.SECRET_KEY == default_secret or len(self.SECRET_KEY) < 32:
            raise RuntimeError("SECRET_KEY must be replaced with a strong random value")

    @property
    def sync_database_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def async_database_url(self) -> str:
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
    @property
    def root_sync_database_url(self) -> str:
        # Used to create database if it doesn't exist
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
