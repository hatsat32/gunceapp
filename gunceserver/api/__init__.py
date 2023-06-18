from fastapi import APIRouter, Depends

from lib.oauth2 import get_current_active_user

from .home import r as public_router
from .auth import r as auth_router

from .user import r as user_router
from .entry import r as entry_router

api_routes = APIRouter(prefix="/api", dependencies=[Depends(get_current_active_user)])

api_routes.include_router(user_router)
api_routes.include_router(entry_router)
