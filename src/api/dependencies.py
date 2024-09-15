from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[
        int | None,
        Query(
            default=1,
            description="Страницы",
            ge=1,
        ),
    ]
    per_page: Annotated[
        int | None, Query(default=None, description="Количество запросов", ge=1, lt=5)
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token") or None
    if not access_token:
        raise HTTPException(status_code=403, detail="Отсутствует токен доступа")
    access_token_bytes = access_token.encode("utf-8")
    return access_token_bytes


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]
