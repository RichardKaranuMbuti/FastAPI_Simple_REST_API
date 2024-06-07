# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from pydantic import BaseModel

models.Base.metadata.create_all(bind=models.engine)

app = FastAPI()

class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/", response_model=StudentCreate)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(name=student.name, age=student.age, grade=student.grade)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student
