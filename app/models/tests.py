from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from app.database.postgres import Base


class TestModel(Base):
    __tablename__ = "test-models"
    test_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    info: Mapped[str]

    def __str__(self):
        return f"Test: {self.test_id}"