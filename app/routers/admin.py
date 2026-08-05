from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.admin import DashboardStatsResponse
from app.dependencies.auth import get_current_admin_user
from app.services.admin import AdminService

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    admin_user: Annotated[User, Depends(get_current_admin_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Get aggregated platform analytics and revenue stats (Admin only).
    """
    service = AdminService(db)
    return await service.get_dashboard_stats()
