from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from app.api.user import User


class Token(Base, CreatedAtMixin, UpdatedAtMixin):
    user_id: Mapped[UUID] = mapped_column(
<<<<<<< HEAD
        ForeignKey(column="user.id"),
=======
        ForeignKey(column="users.id"),
>>>>>>> dev
        unique=True,
    )

    refresh_token: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="token",
    )
