# backend/app/schemas/registration.py
from pydantic import BaseModel, Field
from typing import List


class StudentRegistration(BaseModel):
    student_id: str = Field(..., example="STU2026001")
    full_name: str
    faculty: str
    subjects: List[str]
    face_images: List[str]  # Base64 encoded images
