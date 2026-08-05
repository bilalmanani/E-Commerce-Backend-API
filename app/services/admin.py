from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.schemas.admin import DashboardStatsResponse


class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_stats(self) -> DashboardStatsResponse:
        """
        Executes high-performance SQL aggregation queries for admin analytics.
        """
        # 1. Total Users Count
        users_stmt = select(func.count(User.id))
        users_res = await self.db.execute(users_stmt)
        total_users = users_res.scalar_one()

        # 2. Total Products Count
        products_stmt = select(func.count(Product.id))
        products_res = await self.db.execute(products_stmt)
        total_products = products_res.scalar_one()

        # 3. Total Orders Count
        orders_stmt = select(func.count(Order.id))
        orders_res = await self.db.execute(orders_stmt)
        total_orders = orders_res.scalar_one()

        # 4. Total Revenue (Excluding CANCELLED orders, COALESCE handles NULL -> 0.00)
        revenue_stmt = select(
            func.coalesce(func.sum(Order.total_amount), Decimal("0.00"))
        ).where(Order.status != OrderStatus.CANCELLED)
        revenue_res = await self.db.execute(revenue_stmt)
        total_revenue = revenue_res.scalar_one()

        # 5. Orders Count Grouped by Status
        status_stmt = select(Order.status, func.count(Order.id)).group_by(Order.status)
        status_res = await self.db.execute(status_stmt)
        orders_by_status = {status.value: count for status, count in status_res.all()}

        # Fill missing statuses with 0
        for status_enum in OrderStatus:
            if status_enum.value not in orders_by_status:
                orders_by_status[status_enum.value] = 0

        return DashboardStatsResponse(
            total_users=total_users,
            total_products=total_products,
            total_orders=total_orders,
            total_revenue=total_revenue,
            orders_by_status=orders_by_status
        )
