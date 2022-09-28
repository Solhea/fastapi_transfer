from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from core.utils.helpers import get_db
from core.schemas.user import UserCreate, UserUpdate
from core.cruds.user_crud import get_user, get_all_users, create_user, update_user, delete_user
from core.middleware import hash_password, get_current_user


router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getUser/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    del db_user.password

    return {"data": db_user}


@router.get("/getUsers")
def read_users(db: Session = Depends(get_db)):
    db_users = get_all_users(db)
    if db_users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")

    for user in db_users:
        del user.password

    return {"data": db_users}


@router.post("/createUser")
def create_user_route(user: UserCreate = Body(embed=False), db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    db_user = create_user(db, user)
    if db_user:
        del db_user.password
        return {"data": db_user}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User not created",
    )


@router.put("/updateUser/{user_id}")
def update_user_route(user_id: int, user: UserUpdate = Body(embed=False), db: Session = Depends(get_db)):
    if user.password:
        user.password = hash_password(user.password)
    db_user = update_user(db, user, user_id)
    if db_user:
        del db_user.password
        return {"data": db_user}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User not updated",
    )


@router.delete("/deleteUser/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if db_user:
        del db_user.password
        return {"data": db_user}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User not deleted",
    )
