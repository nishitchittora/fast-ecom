from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {
        "name": "heelo"
    }
}


class Student(BaseModel):
    name: str
    year: str
    age: int


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    year: Optional[str] = None
    age: Optional[int] = None


@app.get("/")
def index():
    return {"name": "hello"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="ID of student", gt=0, lt=4)):
    return students[student_id]


@app.get("/get-by-name/{student_id}")
def get_student_name(student_id: int, test: int, name: Optional[str] = None):
    pass
