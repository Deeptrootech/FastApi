from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from authentication.jwt_auth import decode_and_verify_jwt_token
from database.global_config import GlobalDBSession
from database.tenant_config import get_db_session
from models.global_models import Organizations


# Global DB Dependency
def get_global_db():
    db = GlobalDBSession()
    try:
        yield db
    finally:
        db.close()


# Tenant DB Dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_tenant_db(token: str = Depends(oauth2_scheme)):
    payload = decode_and_verify_jwt_token(token)
    org_name = payload.get("org")  # Organization name to connect Tenant DB

    if not org_name or not org_name.startswith("org_"):
        raise HTTPException(status_code=400, detail="Invalid organization")

    # verify org exists in global DB
    global_db = GlobalDBSession()
    org = global_db.query(Organizations).filter_by(name=org_name).first()
    global_db.close()

    if not org:
        raise HTTPException(status_code=404, detail="Organization not registered.")

    # connect tenant DB
    db = get_db_session(f"{org_name}_db")()

    try:
        yield db
    finally:
        db.close()
