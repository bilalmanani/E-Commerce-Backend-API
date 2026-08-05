from decimal import Decimal
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.cart import CartItem
    from app.models.order import OrderItem
    from app.models.review import Review
    from app.models.wishlist import Wishlist


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    discount_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    wishlist_items: Mapped[List["Wishlist"]] = relationship("Wishlist", back_populates="product", cascade="all, delete-orphan")
