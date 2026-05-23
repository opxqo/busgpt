from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app.config import settings

# Create async engine and sessionmaker
async_engine = create_async_engine(settings.async_database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

# Create sync engine for startup/admin tasks
sync_engine = create_engine(settings.sync_database_url, echo=False)
SessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Async database session dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

def _quote_identifier(identifier: str) -> str:
    return f"`{identifier.replace('`', '``')}`"


def _is_mysql_database() -> bool:
    return make_url(settings.sync_database_url).drivername.startswith("mysql")


def _ensure_column(conn, table_name: str, column_name: str, definition: str):
    exists = conn.execute(
        text(
            """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = :schema
              AND TABLE_NAME = :table_name
              AND COLUMN_NAME = :column_name
            """
        ),
        {
            "schema": settings.database_name,
            "table_name": table_name,
            "column_name": column_name,
        },
    ).scalar()
    if not exists:
        conn.execute(text(f"ALTER TABLE {_quote_identifier(table_name)} ADD COLUMN {_quote_identifier(column_name)} {definition}"))


def _ensure_index(conn, table_name: str, index_name: str, definition: str):
    exists = conn.execute(
        text(
            """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_SCHEMA = :schema
              AND TABLE_NAME = :table_name
              AND INDEX_NAME = :index_name
            """
        ),
        {
            "schema": settings.database_name,
            "table_name": table_name,
            "index_name": index_name,
        },
    ).scalar()
    if not exists:
        conn.execute(text(f"ALTER TABLE {_quote_identifier(table_name)} ADD INDEX {_quote_identifier(index_name)} ({definition})"))


def _run_lightweight_migrations():
    if not _is_mysql_database():
        return

    with sync_engine.begin() as conn:
        _ensure_column(conn, "users", "role", "VARCHAR(20) NOT NULL DEFAULT 'user'")
        _ensure_column(conn, "rides", "contact_info", "TEXT")
        _ensure_column(conn, "rides", "contact_website", "VARCHAR(255) NOT NULL DEFAULT ''")
        _ensure_column(conn, "rides", "contact_price", "NUMERIC(10, 2) NOT NULL DEFAULT 0")
        _ensure_column(conn, "rides", "warranty_days", "INT NOT NULL DEFAULT 30")
        _ensure_column(conn, "rides", "recruit_seats", "INT NOT NULL DEFAULT 1")
        _ensure_column(conn, "orders", "payment_provider", "VARCHAR(30) NOT NULL DEFAULT 'mock'")
        _ensure_column(conn, "orders", "payment_no", "VARCHAR(64)")
        _ensure_column(conn, "orders", "payment_status", "VARCHAR(20) NOT NULL DEFAULT 'paid'")
        _ensure_column(conn, "orders", "paid_at", "DATETIME NULL")
        _ensure_column(conn, "orders", "contact_unlocked_at", "DATETIME NULL")
        _ensure_column(conn, "orders", "expired_at", "DATETIME NULL")
        _ensure_column(conn, "orders", "idempotency_key", "VARCHAR(64)")
        _ensure_column(conn, "orders", "updated_at", "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
        _ensure_index(conn, "orders", "ix_orders_status", "`status`")
        _ensure_index(conn, "orders", "ix_orders_payment_status", "`payment_status`")
        _ensure_index(conn, "orders", "ix_orders_expired_at", "`expired_at`")
        _ensure_index(conn, "orders", "ix_orders_paid_at", "`paid_at`")
        _ensure_index(conn, "orders", "ix_orders_contact_unlocked_at", "`contact_unlocked_at`")
        _ensure_index(conn, "orders", "ix_orders_idempotency_key", "`idempotency_key`")
        _ensure_index(conn, "rides", "ix_rides_created_at", "`created_at`")
        _ensure_index(conn, "rides", "ix_rides_product_created_at", "`product`, `created_at`")
        _ensure_index(conn, "rides", "ix_rides_status_created_at", "`status`, `created_at`")
        conn.execute(text("UPDATE users SET role = 'user' WHERE role IS NULL OR role = ''"))
        conn.execute(text("UPDATE rides SET status = 'open' WHERE status = 'full'"))
        conn.execute(text("UPDATE rides SET warranty_days = IF(duration >= 12, 365, duration * 30) WHERE warranty_days IS NULL OR warranty_days <= 0 OR (warranty_days = 30 AND duration <> 1)"))
        conn.execute(text("UPDATE rides SET recruit_seats = GREATEST(total_seats - 1, 1) WHERE recruit_seats IS NULL OR recruit_seats <= 1"))
        conn.execute(text("UPDATE orders SET status = 'paid' WHERE status IS NULL OR status = ''"))
        conn.execute(text("UPDATE orders SET payment_status = status WHERE payment_status IS NULL OR payment_status = ''"))
        conn.execute(text("UPDATE orders SET payment_provider = 'mock' WHERE payment_provider IS NULL OR payment_provider = ''"))
        conn.execute(text("UPDATE orders SET paid_at = created_at WHERE status = 'paid' AND paid_at IS NULL"))
        conn.execute(text("UPDATE orders SET contact_unlocked_at = COALESCE(paid_at, created_at) WHERE status = 'paid' AND contact_unlocked_at IS NULL"))


# Synchronously ensure the database exists and create all tables
def init_db():
    if _is_mysql_database():
        database_name = settings.database_name
        if not database_name:
            raise RuntimeError("MySQL DATABASE_URL must include a database name")

        # Connect without database name first to create it.
        temp_engine = create_engine(settings.root_sync_database_url, echo=False)
        with temp_engine.connect() as conn:
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS {_quote_identifier(database_name)} "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
            conn.commit()
        temp_engine.dispose()

    # Import models here to ensure they are registered on Base
    from app.models.user import User
    from app.models.ride import Ride
    from app.models.product import Product
    from app.models.order import Order
    from app.models.ride_member import RideMember

    # Create tables
    Base.metadata.create_all(bind=sync_engine)
    _run_lightweight_migrations()

    # Seed/update initial product data
    db = SessionLocal()
    try:
        product_defaults = [
            {
                "type": "chatgpt-plus",
                "label": "Plus",
                "official_price": 20.00,
                "color": "#10b981",
                "max_seats": 4,
                "description": "GPT-5.5、深度研究、Agent 与 Codex",
            },
            {
                "type": "chatgpt-team",
                "label": "Business",
                "official_price": 25.00,
                "color": "#3b82f6",
                "max_seats": 10,
                "description": "Plus 能力、团队工作区、连接器与管理",
            },
            {
                "type": "chatgpt-pro",
                "label": "Pro",
                "official_price": 200.00,
                "color": "#f59e0b",
                "max_seats": 5,
                "description": "最高用量、GPT-5.5 Pro、扩展深度研究",
            },
        ]

        for data in product_defaults:
            product = db.query(Product).filter(Product.type == data["type"]).first()
            if product:
                product.label = data["label"]
                product.official_price = data["official_price"]
                product.color = data["color"]
                product.max_seats = data["max_seats"]
                product.description = data["description"]
            else:
                db.add(Product(**data))
        db.commit()
        print("Successfully synced product types.")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error seeding database: {e}") from e
    finally:
        db.close()
