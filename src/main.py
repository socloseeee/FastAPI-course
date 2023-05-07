from fastapi import FastAPI
from src.auth.schemas import UserRead, UserCreate

from auth.base_config import auth_backend, fastapi_users

from operations.router import router as router_operation

# entry point to our web-app
app = FastAPI(
    title="Trading App"  # title
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
