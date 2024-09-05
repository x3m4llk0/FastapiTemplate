from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TestDTO(BaseModel):
    test_id: UUID
    info: Optional[str] = None