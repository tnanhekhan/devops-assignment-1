from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://mongo:27017")
db = client["students_db"]
student_collection = db["students"]

def add(student=None):
    existing_student = student_collection.find_one({"first_name": student.first_name, "last_name": student.last_name})
    if existing_student:
        return 'already exists', 409
    student_dict = student.to_dict()
    result = student_collection.insert_one(student_dict)
    student.student_id = str(result.inserted_id)
    return student.student_id

def get_by_id(student_id=None, subject=None):
    student_id = ObjectId(student_id)
    student = student_collection.find_one({"_id": student_id})
    if not student:
        return 'not found', 404
    student['student_id'] = str(student['_id'])
    del student['_id']
    return student

def delete(student_id=None):
    student_id = ObjectId(student_id)
    student = student_collection.find_one({"_id": student_id})
    if not student:
        return 'not found', 404
    student_collection.delete_one({"_id": student_id})
    return student_id
