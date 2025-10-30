from database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


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
