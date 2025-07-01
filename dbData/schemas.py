from pydantic import BaseModel

class StudentLoginCreate(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes  = True  # Required to use SQLAlchemy models with Pydantic

class StudentDataCreate(BaseModel):
    name: str
    age: int
    grade: str

class StudentDataResponse(BaseModel):
    id: int
    name: str
    age: int
    grade: str

    class Config:
        from_attributes = True  # Enable ORM compatibility for SQLAlchemy models

class Token(BaseModel):
    access_token: str
    token_type: str

class Item(BaseModel):
    name: str
    price: float
