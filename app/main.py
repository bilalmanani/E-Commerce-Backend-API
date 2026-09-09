from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.database.session import get_db, engine
from app.models import Base
from seed_demo_data import seed_data
from app.middleware.logging import LoggingMiddleware
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    global_unhandled_exception_handler,
)
from app.routers import (
    auth, user, category, product, cart, wishlist, address, order, review, coupon, admin
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI startup and shutdown.
    Ensures database tables are created and demo data is seeded automatically.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await seed_data()
        print("✅ Lifespan: Database initialized and seeded successfully.")
    except Exception as e:
        print(f"⚠️ Lifespan DB setup notice: {e}")
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="A production-ready E-Commerce Backend API built with FastAPI, SQLAlchemy 2.0, PostgreSQL, and Pydantic v2.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# 1. Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Add Custom Logging Middleware
app.add_middleware(LoggingMiddleware)

# 3. Register Custom Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_unhandled_exception_handler)

# 4. Mount Static Directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# 5. Register API Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(address.router)
app.include_router(order.router)
app.include_router(review.router)
app.include_router(coupon.router)
app.include_router(admin.router)


@app.get("/", tags=["Storefront"])
async def root():
    """Serves the interactive frontend web application."""
    return FileResponse("static/index.html")


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}


@app.get("/db-check", tags=["Health Check"])
async def db_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    value = result.scalar()
    return {"status": "connected", "query_result": value}
