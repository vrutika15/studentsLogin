from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import uvicorn
import schemas
import models
import db
from sqlalchemy.orm import Session
import auth

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

get_db = db.get_db

@app.get('/')
def home():
    return {'data': 'home'}

@app.post('/register', response_model=schemas.StudentDataResponse)
def register_student(student_login: schemas.StudentLoginCreate, student_data: schemas.StudentDataCreate, db: Session = Depends(get_db)):
    db_student_login = auth.create_student_login(db, email=student_login.email, password=student_login.password)

    db_student_data = auth.create_student_data(
        db,
        student_id=db_student_login.id,
        name=student_data.name,
        age=student_data.age,
        grade=student_data.grade
    )
    return db_student_data

@app.post('/login', response_model=schemas.Token)
def login(credentials: schemas.StudentLoginCreate, db: Session = Depends(get_db)):
    student = auth.get_student_by_email(db, credentials.email)
    if student is None or not auth.verify_password(credentials.password, student.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!", headers={"WWW-Authenticate": "Bearer"})
    
    token_data = {"sub": student.email}
    access_token = auth.create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/students/me", response_model=schemas.StudentDataResponse)
async def get_student(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Decode and verify the token
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    email = payload.get("sub")
    student = auth.get_student_by_email(db, email=email)
    
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_data = db.query(models.StudentData).filter(models.StudentData.student_id == student.id).first()

    if student_data is None:
        raise HTTPException(status_code=404, detail="Student data not found")

    # Return the Pydantic model of StudentData
    return schemas.StudentDataResponse.from_orm(student_data)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
