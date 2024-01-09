from pydantic import BaseModel
from typing import Optional

class DefaultReponseDoc(BaseModel):
    error: bool
    message: str

class PaginationDoc(BaseModel):
    pages_count: int
    itens_count: int
    itens_per_page: int
    prev: Optional[int]
    next: Optional[int]
    current: int