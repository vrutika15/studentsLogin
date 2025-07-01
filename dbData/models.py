from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class StudentLogin(Base):
    __tablename__ = 'student_login'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Assuming hashed password here

    # Relationship to student data
    student_data = relationship("StudentData", back_populates="student_login")


class StudentData(Base):
    __tablename__ = 'student_data'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(String)

    student_id = Column(Integer, ForeignKey('student_login.id'))

    student_login = relationship("StudentLogin", back_populates="student_data")
