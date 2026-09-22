"""اتصال قاعدة بيانات الأراضي والعقارات (مستقلة) — متوافق مع Neon و PostgreSQL."""
import re
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings


def _normalize_async_url(url: str) -> str:
    """
    يحوّل أي رابط PostgreSQL إلى سائق asyncpg.
    
    يدعم:
      - postgres://...
      - postgresql://...
      - postgresql+psycopg2://...
      - postgresql+asyncpg://...  (يبقى كما هو)
    """
    if not url:
        raise ValueError("LANDS_DB_URL غير مُعرّف في الإعدادات أو متغيرات البيئة")
    return re.sub(r"^postgres(ql)?(\+\w+)?://", "postgresql+asyncpg://", url)


LANDS_DB_URL = _normalize_async_url(settings.LANDS_DB_URL)


# ── تجهيز connect_args حسب نوع القاعدة ──
_connect_args: dict = {}

if LANDS_DB_URL.startswith("postgresql+asyncpg://"):
    # PostgreSQL: فعّل SSL حسب إعداد المشروع (Neon يتطلب SSL)
    if getattr(settings, "DB_USE_SSL", False):
        _connect_args = {"ssl": "require"}
    # المهلة (بالثواني) لتجنب تعليق الاتصال
    _connect_args.setdefault("timeout", 30)
    # لـ Neon: تعطيل prepared statements عند استخدام pooler (pgbouncer)
    _connect_args.setdefault("statement_cache_size", 0)


lands_engine = create_async_engine(
    LANDS_DB_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800,           # إعادة تدوير الاتصالات كل 30 دقيقة
    connect_args=_connect_args,
)

LandsSessionLocal = async_sessionmaker(
    lands_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_lands_db():
    """FastAPI dependency لجلسة قاعدة بيانات الأراضي."""
    async with LandsSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
