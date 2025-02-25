from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Text

from ..repository import Base, uuid_pk, str_null_true, str_uniq


class Disease(Base):
    id: Mapped[uuid_pk]
    name: Mapped[str_uniq]
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    recommendations: Mapped[str] = mapped_column(Text, nullable=True)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, " f"name={self.name!r}"

    def __repr__(self):
        return str(self)
