from datetime import datetime

import sqlalchemy as sa # type: ignore
from src.models.base import db
from sqlalchemy.orm import Mapped, mapped_column # type: ignore

class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=True)
    body: Mapped[str] = mapped_column(sa.String, nullable= True)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})" 