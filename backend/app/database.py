import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
from sqlalchemy.engine import make_url

from app.config import settings

logger = logging.getLogger("busgpt.database")

# Create async engine and sessionmaker.
# SQLAlchemy's pool_pre_ping is currently incompatible with aiomysql's ping()
# signature in this stack, causing intermittent TypeError on connection reuse.
async_engine = create_async_engine(settings.async_database_url, echo=True, pool_recycle=1800)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

# Create sync engine for startup/admin tasks
sync_engine = create_engine(settings.sync_database_url, echo=False, pool_pre_ping=True)
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
        logger.info("Adding missing column %s.%s", table_name, column_name)
        conn.execute(text(f"ALTER TABLE {_quote_identifier(table_name)} ADD COLUMN {_quote_identifier(column_name)} {definition}"))
        return True
    return False


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
        logger.info("Adding missing index %s on %s", index_name, table_name)
        conn.execute(text(f"ALTER TABLE {_quote_identifier(table_name)} ADD INDEX {_quote_identifier(index_name)} ({definition})"))


def _ensure_unique_index(conn, table_name: str, index_name: str, definition: str, columns: str):
    existing_unique = conn.execute(
        text(
            """
            SELECT COUNT(*)
            FROM (
                SELECT INDEX_NAME, GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) AS indexed_columns
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = :schema
                  AND TABLE_NAME = :table_name
                  AND NON_UNIQUE = 0
                GROUP BY INDEX_NAME
            ) AS unique_indexes
            WHERE indexed_columns = :columns
            """
        ),
        {
            "schema": settings.database_name,
            "table_name": table_name,
            "columns": columns,
        },
    ).scalar()
    if not existing_unique:
        logger.info("Adding missing unique index %s on %s", index_name, table_name)
        conn.execute(text(f"ALTER TABLE {_quote_identifier(table_name)} ADD UNIQUE INDEX {_quote_identifier(index_name)} ({definition})"))


def _ensure_nullable_column(conn, table_name: str, column_name: str, definition: str):
    is_nullable = conn.execute(
        text(
            """
            SELECT IS_NULLABLE
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
    if is_nullable == "NO":
        logger.info("Making column nullable %s.%s", table_name, column_name)
        conn.execute(text(f"ALTER TABLE {_quote_identifier(table_name)} MODIFY COLUMN {_quote_identifier(column_name)} {definition}"))


def _table_exists(conn, table_name: str) -> bool:
    exists = conn.execute(
        text(
            """
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = :schema
              AND TABLE_NAME = :table_name
            """
        ),
        {"schema": settings.database_name, "table_name": table_name},
    ).scalar()
    return bool(exists)


def _column_exists(conn, table_name: str, column_name: str) -> bool:
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
    return bool(exists)


def _repair_datetime_columns_before_create_all():
    if not _is_mysql_database():
        return

    datetime_columns_by_table = {
        "users": [
            ("created_at", "DATETIME NOT NULL"),
            ("updated_at", "DATETIME NOT NULL"),
        ],
        "rides": [
            ("created_at", "DATETIME NOT NULL"),
            ("updated_at", "DATETIME NOT NULL"),
        ],
        "orders": [
            ("created_at", "DATETIME NOT NULL"),
            ("updated_at", "DATETIME NOT NULL"),
            ("paid_at", "DATETIME NULL"),
            ("contact_unlocked_at", "DATETIME NULL"),
            ("expired_at", "DATETIME NULL"),
        ],
        "ride_members": [
            ("joined_at", "DATETIME NOT NULL"),
        ],
        "activation_tokens": [
            ("created_at", "DATETIME NOT NULL"),
            ("expires_at", "DATETIME NOT NULL"),
        ],
    }

    with sync_engine.begin() as conn:
        for table_name, columns in datetime_columns_by_table.items():
            if not _table_exists(conn, table_name):
                continue

            existing_columns = [
                (column_name, definition)
                for column_name, definition in columns
                if _column_exists(conn, table_name, column_name)
            ]
            if not existing_columns:
                continue

            logger.info(
                "Repairing datetime column defaults before create_all: %s.%s",
                table_name,
                ",".join(column_name for column_name, _ in existing_columns),
            )
            modifications = [
                f"MODIFY COLUMN {_quote_identifier(column_name)} {definition}"
                for column_name, definition in existing_columns
            ]
            conn.execute(text(f"ALTER TABLE {_quote_identifier(table_name)} {', '.join(modifications)}"))


def _run_lightweight_migrations():
    if not _is_mysql_database():
        logger.info("Skipping lightweight migrations because database is not MySQL")
        return

    logger.info("Running lightweight database migrations")
    with sync_engine.begin() as conn:
        _ensure_column(conn, "users", "role", "VARCHAR(20) NOT NULL DEFAULT 'user'")
        _ensure_column(conn, "users", "is_active", "BOOLEAN NOT NULL DEFAULT TRUE")
        _ensure_column(conn, "rides", "contact_info", "TEXT")
        _ensure_column(conn, "rides", "contact_website", "VARCHAR(255) NOT NULL DEFAULT ''")
        _ensure_column(conn, "rides", "contact_price", "NUMERIC(10, 2) NOT NULL DEFAULT 0")
        _ensure_column(conn, "rides", "warranty_days", "INT NOT NULL DEFAULT 30")
        recruit_seats_added = _ensure_column(conn, "rides", "recruit_seats", "INT NOT NULL DEFAULT 1")
        _ensure_column(conn, "orders", "payment_provider", "VARCHAR(30) NOT NULL DEFAULT 'mock'")
        _ensure_column(conn, "orders", "payment_no", "VARCHAR(64)")
        _ensure_column(conn, "orders", "payment_status", "VARCHAR(20) NOT NULL DEFAULT 'paid'")
        _ensure_column(conn, "orders", "paid_at", "DATETIME NULL")
        _ensure_column(conn, "orders", "contact_unlocked_at", "DATETIME NULL")
        _ensure_column(conn, "orders", "expired_at", "DATETIME NULL")
        _ensure_column(conn, "orders", "idempotency_key", "VARCHAR(64)")
        _ensure_column(conn, "orders", "updated_at", "DATETIME NULL")
        _ensure_column(conn, "users", "email", "VARCHAR(255) NULL")
        _ensure_column(conn, "users", "email_verified_at", "DATETIME NULL")
        _ensure_nullable_column(conn, "users", "phone", "VARCHAR(20) NULL")
        conn.execute(text("UPDATE users SET email = CONCAT('legacy-user-', id, '@busgpt.local') WHERE email IS NULL OR email = ''"))
        conn.execute(text("UPDATE users SET email_verified_at = created_at WHERE email_verified_at IS NULL AND email LIKE 'legacy-user-%@busgpt.local'"))
        _ensure_unique_index(conn, "users", "uq_users_email", "`email`", "email")
        _ensure_column(conn, "activation_tokens", "token_hash", "VARCHAR(64) NOT NULL")
        _ensure_unique_index(conn, "activation_tokens", "uq_activation_tokens_token_hash", "`token_hash`", "token_hash")
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
        if recruit_seats_added:
            conn.execute(text("UPDATE rides SET recruit_seats = GREATEST(total_seats - 1, 1)"))
        else:
            conn.execute(text("UPDATE rides SET recruit_seats = GREATEST(total_seats - 1, 1) WHERE recruit_seats IS NULL OR recruit_seats <= 0"))
        conn.execute(text("UPDATE orders SET status = 'paid' WHERE status IS NULL OR status = ''"))
        conn.execute(text("UPDATE orders SET payment_status = status WHERE payment_status IS NULL OR payment_status = ''"))
        conn.execute(text("UPDATE orders SET payment_provider = 'mock' WHERE payment_provider IS NULL OR payment_provider = ''"))
        conn.execute(text("UPDATE orders SET paid_at = created_at WHERE status = 'paid' AND paid_at IS NULL"))
        conn.execute(text("UPDATE orders SET contact_unlocked_at = COALESCE(paid_at, created_at) WHERE status = 'paid' AND contact_unlocked_at IS NULL"))
    logger.info("Lightweight database migrations completed")


# Synchronously ensure the database exists and create all tables
def init_db():
    logger.info("init_db started for database %s", settings.database_name)
    if _is_mysql_database():
        database_name = settings.database_name
        if not database_name:
            raise RuntimeError("MySQL DATABASE_URL must include a database name")

        # Connect without database name first to create it.
        root_url = make_url(settings.root_sync_database_url)
        logger.info(
            "Connecting to MySQL root URL host=%s port=%s driver=%s to ensure database exists",
            root_url.host,
            root_url.port,
            root_url.drivername,
        )
        temp_engine = create_engine(settings.root_sync_database_url, echo=False, pool_pre_ping=True)
        with temp_engine.connect() as conn:
            logger.info("Ensuring MySQL database exists: %s", database_name)
            conn.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS {_quote_identifier(database_name)} "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
            conn.commit()
        temp_engine.dispose()
        logger.info("Database existence check completed: %s", database_name)

    # Import models here to ensure they are registered on Base
    logger.info("Importing SQLAlchemy models")
    from app.models.user import User
    from app.models.ride import Ride
    from app.models.product import Product
    from app.models.order import Order
    from app.models.ride_member import RideMember
    from app.models.activation_token import ActivationToken

    # Create tables
    _repair_datetime_columns_before_create_all()
    logger.info("Creating missing tables with SQLAlchemy metadata")
    Base.metadata.create_all(bind=sync_engine)
    logger.info("Table creation step completed")
    _run_lightweight_migrations()

    # Seed/update initial product data
    logger.info("Syncing product defaults")
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
                "color": "#8b5cf6",
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
        logger.info("Successfully synced product types")
    except Exception as e:
        db.rollback()
        logger.exception("Error seeding database")
        raise RuntimeError(f"Error seeding database: {e}") from e
    finally:
        db.close()
        logger.info("init_db finished")
