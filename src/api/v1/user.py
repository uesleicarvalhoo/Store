from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlmodel import Session
from starlette.status import HTTP_201_CREATED

from src.core.controller import user
from src.core.helpers.database import make_session
from src.core.models import Context, CreateUser, QueryUser, User
from src.utils.dependencies import api_context_manager

router = APIRouter()


@router.get("/", response_model=List[User], response_model_exclude={"password_hash": ...})
async def get(
    query: QueryUser = Depends(),
    session: Session = Depends(make_session),
    context: Context = Depends(api_context_manager),
):
    return user.get_all(session, query, context=api_context_manager)


@router.get("/{user_id}", response_model=User, response_model_exclude={"password_hash": ...})
async def get_by_id(
    user_id: UUID, session: Session = Depends(make_session), context: Context = Depends(api_context_manager)
):
    return user.get_by_id(session, user_id, context=api_context_manager)


@router.post("/", response_model=User, status_code=HTTP_201_CREATED)
async def create(schema: CreateUser, session: Session = Depends(make_session)):

    return user.create(session, schema, context=api_context_manager)
