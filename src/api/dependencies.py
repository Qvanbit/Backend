from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Страницы", ge=1,)]
    per_page: Annotated[int | None, Query(default=None, description="Количество запросов", ge=1, lt=5)]
    
    
PaginationDep = Annotated[PaginationParams, Depends()]