from fastapi import APIRouter, Depends, Request

from src.core.models import Context
from src.core.models.user import User

from ..dependencies import context_manager, get_current_user
from ..utils import templates

router = APIRouter()


@router.get("/")
async def index(
    request: Request, current_user: User = Depends(get_current_user), context: Context = Depends(context_manager)
):
    return templates.TemplateResponse("index.html", {"request": request, "context": context})
