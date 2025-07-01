from datetime import datetime, timedelta
from jose import JWTError
import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext  
import schemas
import models

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create JWT token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify JWT token
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Get student by email from DB
def get_student_by_email(db: Session, email: str):
    student = db.query(models.StudentLogin).filter(models.StudentLogin.email == email).first()
    if student:
        return student     #schemas.StudentLoginCreate(email=student.email, password=student.password)
    return None

# Get student data by email
def get_student_data_by_email(db: Session, email: str):
    student = get_student_by_email(db, email)
    if student:
        return schemas.StudentDataResponse(
            name=student.student_data.name,
            age=student.student_data.age,
            grade=student.student_data.grade
        )
    return None

# Create student login (with hashed password)
def create_student_login(db: Session, email: str, password: str):
    hashed_password = hash_password(password)
    db_student = models.StudentLogin(email=email, password=hashed_password)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Create student data
def create_student_data(db: Session, student_id: int, name: str, age: int, grade: str):
    db_student_data = models.StudentData(student_id=student_id, name=name, age=age, grade=grade)
    db.add(db_student_data)
    db.commit()
    db.refresh(db_student_data)
    return db_student_data
