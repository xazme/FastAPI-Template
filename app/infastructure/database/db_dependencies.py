from typing import Annotated, AsyncGenerator
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .db_helper import DataBaseHelper


def get_db_helper(request: Request) -> DataBaseHelper:
    return request.app.state.db_helper


DataBaseHelperDep = Annotated[DataBaseHelper, Depends(get_db_helper)]


async def get_session(
    db_helper: DataBaseHelperDep,
) -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.get_session():
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
