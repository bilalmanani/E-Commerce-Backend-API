import asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.database.session import get_db
from app.models.base import Base
from app.models.user import User, UserRole
from app.auth.security import hash_password
from app.auth.jwt import create_access_token

# 1. In-memory SQLite Test Database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create Test Engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Test Session Maker
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session-scoped async fixtures."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def prepare_database():
    """Create all database tables before test runs and drop them after test completes."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide isolated test database session per test."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Override get_db dependency with test database session and provide httpx AsyncClient.
    """
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create customer test user in test DB."""
    user = User(
        email="testuser@example.com",
        first_name="Test",
        last_name="Customer",
        hashed_password=hash_password("testpassword123"),
        role=UserRole.CUSTOMER
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_admin(db_session: AsyncSession) -> User:
    """Create admin test user in test DB."""
    admin = User(
        email="adminuser@example.com",
        first_name="Admin",
        last_name="Tester",
        hashed_password=hash_password("adminpassword123"),
        role=UserRole.ADMIN
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    """Generate authorization Bearer header for customer test user."""
    token = create_access_token({"sub": str(test_user.id), "email": test_user.email, "role": test_user.role})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_headers(test_admin: User) -> dict:
    """Generate authorization Bearer header for admin test user."""
    token = create_access_token({"sub": str(test_admin.id), "email": test_admin.email, "role": test_admin.role})
    return {"Authorization": f"Bearer {token}"}
