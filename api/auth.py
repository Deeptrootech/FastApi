from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependency.authorization import authorized_role
from dependency.database import get_global_db
from schemas.auth import AdminLogin

app = APIRouter()


# 3rd point
# depends: only admin role,
@app.post("/admin/login", Depends(authorized_role(["admin"])))
def admin_login(data: AdminLogin, db: Session = Depends(get_global_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_jwt_access_token({"sub": db_user.username})
    logger.info("Login Successfull..!!")
    return {"access_token": access_token, "token_type": "bearer"}
