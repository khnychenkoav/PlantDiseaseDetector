from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Text, ForeignKey

from ..repository import Base, uuid_pk, str_null_true, str_uniq


class User(Base):
    id: Mapped[uuid_pk]
    name: Mapped[str_null_true]
    email: Mapped[str_uniq]
    password: Mapped[str_uniq]

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, " f"email={self.email!r}"

    def __repr__(self):
        return str(self)
