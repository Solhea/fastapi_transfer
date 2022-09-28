from fastapi import FastAPI

from core import models
from core.database import SessionLocal, engine
from core.routers import user_router, authentication_router


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(user_router.router, prefix="/api", tags=["users"])
app.include_router(authentication_router.router, prefix="/api", tags=["auth"])