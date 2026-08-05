from decimal import Decimal
from typing import Dict
from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    total_users: int
    total_products: int
    total_orders: int
    total_revenue: Decimal
    orders_by_status: Dict[str, int]
