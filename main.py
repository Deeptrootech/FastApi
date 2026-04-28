from fastapi import FastAPI, Depends

from dependency import is_authenticated
from routes import auth, projects, issue, comments

app = FastAPI()

# Include the auth routes
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(issue.router)
app.include_router(comments.router)
