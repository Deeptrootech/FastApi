from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from admin.setup import setup_admin
from dependencies import get_current_user
from routers import auth, posts, users, roles

app = FastAPI()  # dependencies=[Depends(get_query_token)]
setup_admin(app)  # sqladmin panel integration

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router)  # unprotected api
app.include_router(roles.router)
app.include_router(posts.router, dependencies=[Depends(get_current_user)])  # protected api

# Mount the "static" directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
