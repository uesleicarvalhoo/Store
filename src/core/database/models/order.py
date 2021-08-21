from typing import List, Union

from sqlalchemy import Column, ForeignKey, Integer, exists
from sqlalchemy.orm import Query, Session, relationship
from sqlalchemy.sql.sqltypes import DateTime

from src.core.schemas import CreateOrder, GetOrder

from .base import BaseModel


class Order(BaseModel):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True)
    client_id = Column("client_id", Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    date = Column("date", DateTime)

    client = relationship(
        "Client", back_populates="orders", cascade="all,delete", lazy="selectin", passive_deletes=True
    )

    details = relationship(
        "OrderDetail", back_populates="order", cascade="all,delete", lazy="selectin", passive_deletes=True
    )

    @classmethod
    def query(cls, session: Session, schema: GetOrder) -> Query:
        query = session.query(cls)

        if schema.client_id:
            return query.filter(cls.client_id == schema.client_id)

        return query

    @classmethod
    def create(cls, session: Session, schema: CreateOrder) -> "Order":
        data = schema.dict(exclude={"details"})
        obj = Order(**data)
        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj

    @classmethod
    def get(cls, session: Session, order_id: int) -> Union[None, "Order"]:
        return session.query(cls).filter(cls.id == order_id).first()

    @classmethod
    def get_by_hash(cls, session: Session, hash: str) -> Union[None, "Order"]:
        return session.query(cls).filter(cls.hash == hash).first()

    @classmethod
    def get_all(cls, session: Session, schema: GetOrder) -> List["Order"]:
        return super().get_all(session, schema)

    @classmethod
    def delete_by_id(cls, session: Session, order_id: int) -> Union[None, "Order"]:
        return super().delete_by_id(session, order_id)

    @classmethod
    def exists(cls, session: Session, order_id: int) -> bool:
        return session.query(exists().where(cls.order_id == order_id)).scalar()
