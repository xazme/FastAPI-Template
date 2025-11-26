from uuid import UUID
from datetime import datetime


class CreatedAtMixin:
    created_at: datetime


class UpdatedAtMixin:
    updated_at: datetime


class BaseResponseMixin(CreatedAtMixin, UpdatedAtMixin):
    id: UUID
