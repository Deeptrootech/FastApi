from fastapi import FastAPI

from api import organization

app = FastAPI()

# Include routers
app.include_router(organization.router)
    