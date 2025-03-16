from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Text, text
import uuid

from .repository import Base, uuid_pk, str_uniq, str_null_true, uuid_not_pk


class User(Base):
    id: Mapped[uuid_pk] = mapped_column(primary_key=True)
    name: Mapped[str_null_true]
    email: Mapped[str_uniq]
    password: Mapped[str_uniq]

    historys: Mapped[list["History"]] = relationship("History", back_populates="user")
    is_user: Mapped[bool] = mapped_column(
        default=True, server_default=text("true"), nullable=False
    )
    is_admin: Mapped[bool] = mapped_column(
        default=False, server_default=text("false"), nullable=False
    )
    is_super_admin: Mapped[bool] = mapped_column(
        default=False, server_default=text("false"), nullable=False
    )

    extend_existing = True

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, email={self.email!r})"

    def __repr__(self):
        return str(self)


class Disease(Base):

    id: Mapped[uuid_pk] = mapped_column(primary_key=True)
    name: Mapped[str_uniq]
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    recommendations: Mapped[str] = mapped_column(Text, nullable=True)

    historys: Mapped[list["History"]] = relationship(
        "History", back_populates="disease"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)


class History(Base):

    id: Mapped[uuid_pk] = mapped_column(primary_key=True)
    user_id: Mapped[uuid_not_pk] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        primary_key=False,
    )
    disease_id: Mapped[uuid_not_pk] = mapped_column(
        ForeignKey("diseases.id"),
        nullable=False,
        primary_key=False,
    )
    image_path: Mapped[str_uniq] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="historys")
    disease: Mapped["Disease"] = relationship("Disease", back_populates="historys")
