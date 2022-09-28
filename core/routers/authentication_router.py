from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.utils.helpers import get_db
from core.middleware import create_access_token, verify_password
from core.cruds.user_crud import get_user_by_username


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, form_data.username)
    if db_user is None or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=404, detail="Please check your credentials")

    access_token = create_access_token(
        data={"username": db_user.username}
    )
    return {"data": {"access_token": access_token, "token_type": "bearer"}}
