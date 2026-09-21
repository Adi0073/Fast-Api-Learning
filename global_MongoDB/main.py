from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from bson.errors import InvalidId
from database import student_collection
from validation import Student_create, Student_update, Student_out


app = FastAPI(title="Learning FastAPI")


def student_helper(student: dict) -> dict:
    """Convert a raw Mongo document into the shape Student_out expects."""
    student["_id"] = str(student["_id"])
    return student


def to_object_id(student_id: str) -> ObjectId:
    try:
        return ObjectId(student_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid student id format")

@app.get("/")
def home():
    return {"message": "Welcome to Adi's Student Api Project"}


@app.get("/students", response_model=list[Student_out])
async def get_students():
    students = await student_collection.find().to_list(length=None)
    return [student_helper(s) for s in students]


@app.get("/students/{student_id}", response_model=Student_out)
async def get_student(student_id: str):
    oid = to_object_id(student_id)
    student = await student_collection.find_one({"_id": oid})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_helper(student)



@app.post("/students", status_code=status.HTTP_201_CREATED, response_model=Student_out)
async def add_student(student: Student_create):
    result = await student_collection.insert_one(student.model_dump())
    new_student = await student_collection.find_one({"_id": result.inserted_id})
    return student_helper(new_student)



@app.put("/students/{student_id}", response_model=Student_out)
async def update_student(student_id: str, student: Student_update):
    oid = to_object_id(student_id)
    # Only update fields the client actually sent
    update_data = {k: v for k, v in student.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    result = await student_collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    updated = await student_collection.find_one({"_id": oid})
    return student_helper(updated)


@app.delete("/students/{student_id}")
async def delete_student(student_id: str):
    oid = to_object_id(student_id)
    result = await student_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}
