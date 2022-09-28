from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.schemas.user import UserCreate, UserUpdate
from core.models import User as UserTable
from core.utils.helpers import update_optional_fields


def get_user(db: Session, user_id: int):
    return db.query(UserTable).filter(UserTable.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(UserTable).filter(UserTable.username == username).first()


def get_all_users(db: Session):
    return db.query(UserTable).all()


def create_user(db: Session, user: UserCreate):
    db_user = UserTable(username=user.username, password=user.password,
                        first_name=user.firstName, last_name=user.lastName)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on username")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_user


def update_user(db: Session, user: UserUpdate, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user = update_optional_fields(db_user, user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate entry on username")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong")
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
