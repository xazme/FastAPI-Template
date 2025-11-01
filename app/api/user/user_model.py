from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    name: Mapped[str] = mapped_column(
        type_=String,
        unique=False,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        type_=String,
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        type_=String,
        unique=False,
        nullable=False,
    )
