from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy.orm import DeclarativeBase # type: ignore

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)