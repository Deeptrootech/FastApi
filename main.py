from fastapi import FastAPI
from routes import auth, projects, issue, comments

app = FastAPI()

# Include the auth routes
app.include_router(auth.router, tags=["auth"])
app.include_router(projects.router, tags=["projects"])
app.include_router(issue.router, tags=["issue"])
app.include_router(comments.router, tags=["comments"])
