from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    """
    A mixin class that adds a `created_at` timestamp field to SQLAlchemy models.

    This mixin automatically records the creation time of a record using the database server's
    current time (UTC-aware) via `func.now()`. The field is indexed and non-nullable, making it
    efficient for querying and sorting by creation time.

    Usage:
        Inherit this mixin in any SQLAlchemy model to include a standardized `created_at` field.

    Example:
        >>> class User(Base, CreatedAtMixin):
        ...     id: Mapped[int] = mapped_column(primary_key=True)
        ...     name: Mapped[str] = mapped_column(String)

        The `created_at` field will be set automatically when the record is first inserted.

    Attributes:
        created_at (Mapped[datetime]): An auto-populated, indexed timestamp indicating
            when the record was created. Stored with timezone information and defaults
            to the database server's current time.
    """

    created_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
    )


class UpdatedAtMixin:
    """
    A mixin class that adds an `updated_at` timestamp field to SQLAlchemy models.

    This mixin automatically tracks the last modification time of a record. The `updated_at`
    field is updated with the database server's current time (UTC-aware) whenever the record
    is modified, thanks to the `onupdate` parameter. It also defaults to the current time
    upon record creation.

    The field is indexed and non-nullable, making it efficient for queries that filter or
    sort by update time.

    Usage:
        Inherit this mixin in any SQLAlchemy model to include a standardized `updated_at` field.

    Example:
        >>> class User(Base, UpdatedAtMixin):
        ...     id: Mapped[int] = mapped_column(primary_key=True)
        ...     name: Mapped[str] = mapped_column(String)

        Each time the user record is updated, `updated_at` will be automatically refreshed.

    Attributes:
        updated_at (Mapped[datetime]): A timestamp indicating when the record was last updated.
            Stored with timezone information, automatically set on insert and updated on any change.
            Indexed for faster queries.
    """

    updated_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        index=True,
        onupdate=func.now(),
        server_default=func.now(),
    )
