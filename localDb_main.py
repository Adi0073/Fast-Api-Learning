from pathlib import Path
import json
from pydantic import BaseModel
from fastapi import FastAPI,HTTPException

db=Path('students.json')
class Student(BaseModel):
    id:int
    name:str
    course:str
      


app=FastAPI()
texts=[]
def check_db():
    if not db.exists():
        db.write_text('[]')

    else:
        with open(db,'r') as file:
            return json.load(file)

def save_students(data):
    with open(db,'w') as f:
        json.dump(data,f,indent=4)


@app.get('/')

def home():
    return {1:"Welcome to the start"}


@app.get("/students")

def load_db():
    return check_db()

@app.get("/students/{student_id}")
def get_student(student_id:int):

    s=load_db()

    for student in s:
        if student['id']==student_id:
            return student

    raise HTTPException(404,"Student Id Not Found")


@app.post("/students",status_code=201)

def add_students(student:Student):
    students=load_db()

    for s in students:
        if s['id']==student.id:
            raise HTTPException(400,"Id already exists")

    students.append(student.model_dump())

    save_students(students)
    return {"messege":"data added successfully"}


@app.put("/students/{student_id}")

def update_student(student_id:int,student:Student):

    students=load_db()

    for i,s in enumerate(students):
        if s['id']==student_id:
            students[i]=student.model_dump()
            save_students(students)
            return {"messege":"Student data updated sucessfully"}

    raise HTTPException(404,"Student not found")


@app.delete("/students/{student_id}")
def delete_student(student_id:int):
    students=load_db()

    new=[s for s in students if s['id']!=student_id]
    if len(new)==len(students):
        raise HTTPException(404,"Student Id not found")
    save_students(new)
    return{"Messege":"Studnet has been sucessfully deleted"}

        

        


        
    

