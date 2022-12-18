from core.database import SessionLocal
from humps import camelize


def update_optional_fields(object, data):
    for key, value in data:
        if value is not None:
            setattr(object, key, value)
    return object


def update_specific_optional_fields(object, data, fields):
    for key in data:
        value = data[key]
        if value is not None and key in fields:
            setattr(object, key, value)
    return object


def update_required_fields(object, data):
    for key, value in data:
        setattr(object, key, value)
    return object


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def to_camel(string):
    return camelize(string)
