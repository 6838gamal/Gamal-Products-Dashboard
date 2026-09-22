"""اتصال قاعدة بيانات الأراضي والعقارات (مستقلة)."""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# ضع رابط القاعدة المنفصلة في settings أو هنا مباشرة
LANDS_DB_URL = settings.LANDS_DB_URL  # مثال: "postgresql+asyncpg://user:pass@host:5432/lands_db"

lands_engine = create_async_engine(LANDS_DB_URL, echo=False, pool_pre_ping=True)
LandsSessionLocal = async_sessionmaker(lands_engine, class_=AsyncSession, expire_on_commit=False)

async def get_lands_db():
    async with LandsSessionLocal() as session:
        yield session
