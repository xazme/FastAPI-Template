from datetime import datetime
from uuid import UUID


class CreatedAtResponseMixin:
    created_at: datetime


class UpdatedAtResponseMixin:
    updated_at: datetime


class BaseResponseMixin(CreatedAtResponseMixin, UpdatedAtResponseMixin):
    id: UUID
