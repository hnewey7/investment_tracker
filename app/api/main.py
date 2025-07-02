from fastapi import APIRouter

from app.api.routes import login, users, instruments

# - - - - - - - - - - - - - - - - - - -

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(instruments.router)