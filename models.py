from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from pydantic import BaseModel

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)


class UpdateUser(BaseModel):
    name: str
    age: int
