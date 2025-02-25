from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Text, ForeignKey

from ..repository import Base, uuid_pk


class History(Base):
    id: Mapped[uuid_pk]
    user_id: Mapped[uuid_pk] = mapped_column(ForeignKey("users.id"), nullable=False)
    diseases_id: Mapped[uuid_pk] = mapped_column(
        ForeignKey("diseases.id"), nullable=False
    )
