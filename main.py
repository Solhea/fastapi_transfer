from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from core import models
from core.database import SessionLocal, engine
from core.routers import user_router, authentication_router, employee_router, driver_router, operation_router


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(user_router.router, prefix="/api", tags=["users"])
app.include_router(authentication_router.router, prefix="/api", tags=["auth"])
app.include_router(employee_router.router, prefix="/api", tags=["employees"])
app.include_router(driver_router.router, prefix="/api", tags=["drivers"])
app.include_router(operation_router.router, prefix="/api", tags=["operations"])
