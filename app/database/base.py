import uuid
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        type_=UUID(as_uuid=True),
        unique=True,
        nullable=False,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        index=True,
        onupdate=func.now(),
        server_default=func.now(),
    )

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()
