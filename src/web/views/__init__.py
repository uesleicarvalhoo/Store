from fastapi import APIRouter
from fastapi.params import Depends

from ..dependencies import login_required
from . import access, clients, fiscal_notes, index, items, order

endpoints = APIRouter()
endpoints.include_router(access.router)
endpoints.include_router(index.router, dependencies=[Depends(login_required)])
endpoints.include_router(clients.router, prefix="/clientes", dependencies=[Depends(login_required)])
endpoints.include_router(fiscal_notes.router, prefix="/notas_fiscais", dependencies=[Depends(login_required)])
endpoints.include_router(items.router, prefix="/produtos", dependencies=[Depends(login_required)])
endpoints.include_router(order.router, prefix="/vendas", dependencies=[Depends(login_required)])