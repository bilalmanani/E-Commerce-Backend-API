from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.product import Product


class Wishlist(Base, TimestampMixin):
    __tablename__ = "wishlist"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="unique_user_product_wishlist"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="wishlist_items")
    product: Mapped["Product"] = relationship("Product", back_populates="wishlist_items")
