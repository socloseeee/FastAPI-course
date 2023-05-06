from datetime import datetime

from enum import Enum
from typing import List, Optional
from typing import Annotated

from fastapi import FastAPI, Request, status, Depends
import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manage import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError

from pydantic.fields import Field
from pydantic.main import BaseModel

# entry point to our web-app
app = FastAPI(
    title="Trading App"  # title
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

current_user = fastapi_users.current_user()

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonim"



