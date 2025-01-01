from fastapi import Depends, FastAPI

from .dependencies import get_current_user
from .internal import admin
from .routers import auth, posts, users

app = FastAPI()  # dependencies=[Depends(get_query_token)]

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, dependencies=[Depends(get_current_user)])  # protected api
app.include_router(posts.router, dependencies=[Depends(get_current_user)])  # protected api
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_current_user)],
    responses={418: {"description": "I'm a teapot"}},
)  # Not protected api


@app.get("/")  # Not protected api
async def root():
    return {"message": "Hello Bigger Applications!"}
