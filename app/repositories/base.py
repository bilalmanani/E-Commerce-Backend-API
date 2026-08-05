from typing import Generic, TypeVar, Type, Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic Base Repository handling common async CRUD database operations.
    """

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: Any) -> ModelType | None:
        """Fetch a single record by primary key."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """Fetch multiple records with offset pagination."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj_in: dict[str, Any]) -> ModelType:
        """Create and persist a new record."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in: dict[str, Any]) -> ModelType:
        """Update fields on an existing record."""
        for field, value in obj_in.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any) -> bool:
        """Delete a record by primary key."""
        db_obj = await self.get_by_id(id)
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False
