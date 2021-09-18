from typing import List, Union
from uuid import uuid4

from sqlalchemy import Boolean, Column, String, exists
from sqlalchemy.orm import Query, Session

from ...schemas import CreateUser, GetUser
from ...security import get_password_hash
from ..types import GUID
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    __dict_exclude_fields__ = ["password_hash"]

    id = Column("id", GUID(), default=uuid4(), primary_key=True)
    email = Column("email", String, unique=True, nullable=False)
    password_hash = Column("password_hash", String, nullable=False)
    name = Column("name", String, nullable=False)
    admin = Column("admin", Boolean, default=False)

    @classmethod
    def query(cls, session: Session, schema: GetUser) -> Query:
        query = session.query(cls)

        if schema.id:
            return query.filter(cls.id == schema.id)

        if schema.name:
            return query.filter(cls.name == schema.name)

        if schema.email:
            return query.filter(cls.email == schema.email)

        return query

    @classmethod
    def create(cls, session: Session, schema: CreateUser) -> "User":
        data = schema.dict(exclude={"confirm_password"})
        data["password_hash"] = get_password_hash(data.pop("password"))

        user = cls(**data)
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @classmethod
    def get(cls, session: Session, user_id: int) -> Union[None, "User"]:
        return super().get(session, user_id)

    @classmethod
    def get_all(cls, session: Session, schema: GetUser) -> List["User"]:
        return super().get_all(session, schema)

    @classmethod
    def get_by_email(cls, session: Session, email: str) -> "User":
        return session.query(cls).filter(cls.email == cls.email).first()

    @classmethod
    def delete_by_id(cls, session: Session, user_id: int) -> Union[None, "User"]:
        return super().delete_by_id(session, user_id)

    @classmethod
    def exists(cls, session: Session, email: str) -> bool:
        return bool(session.query(exists().where(cls.email == email)).scalar())

    @property
    def is_super_user(self) -> bool:
        return self.admin