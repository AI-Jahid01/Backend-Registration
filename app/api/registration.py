
# # backend/app/api/registration.py
# from fastapi import APIRouter, HTTPException
# from datetime import datetime
# import numpy as np

# from app.schemas.registration import StudentRegistration
# from app.db.mongo import students_col
# from app.core.face_embedding import generate_face_embedding
# from app.utils.validators import validate_min_images

# router = APIRouter()

# SIM_THRESHOLD = 0.6


# def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
#     return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# @router.post("/register", tags=["Registration"])
# def register_student(student: StudentRegistration):
#     """
#     Student Self Registration Endpoint
#     """

#     # ==========================
#     # VALIDATION
#     # ==========================
#     try:
#         validate_min_images(student.face_images)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

#     # ==========================
#     # STUDENT ID CHECK
#     # ==========================
#     existing_student = students_col.find_one(
#         {"student_id": student.student_id}
#     )

#     if existing_student:
#         duplicate_subjects = set(existing_student.get("subjects", [])) & set(student.subjects)
#         if duplicate_subjects:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Already registered for: {', '.join(duplicate_subjects)}"
#             )

#     # ==========================
#     # FACE EMBEDDING GENERATION
#     # ==========================
#     embeddings = []

#     for img in student.face_images:
#         embedding = generate_face_embedding(img)

#         if embedding is None:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Face not detected in one or more images"
#             )

#         embeddings.append(embedding)

#     avg_embedding = np.mean(np.array(embeddings), axis=0)

#     # ==========================
#     # FACE DUPLICATE CHECK
#     # ==========================
#     for record in students_col.find({}, {"student_id": 1, "face_embedding": 1}):
#         existing_embedding = np.array(record["face_embedding"])
#         similarity = cosine_similarity(existing_embedding, avg_embedding)

#         if similarity > SIM_THRESHOLD:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Face already registered (Student ID: {record['student_id']})"
#             )

#     # ==========================
#     # INSERT / UPDATE
#     # ==========================
#     if existing_student:
#         updated_subjects = list(
#             set(existing_student["subjects"]) | set(student.subjects)
#         )

#         students_col.update_one(
#             {"student_id": student.student_id},
#             {
#                 "$set": {
#                     "subjects": updated_subjects,
#                     "face_embedding": avg_embedding.tolist()
#                 }
#             }
#         )
#     else:
#         students_col.insert_one({
#             "student_id": student.student_id,
#             "full_name": student.full_name,
#             "faculty": student.faculty,
#             "subjects": student.subjects,
#             "face_embedding": avg_embedding.tolist(),
#             "registered_at": datetime.utcnow()
#         })

#     return {"message": "Registration successful"}



# new logic add below if exixting students want to register for new subjects
# # backend/app/api/registration.py
from fastapi import APIRouter, HTTPException
from datetime import datetime
import numpy as np

from app.schemas.registration import StudentRegistration
from app.db.mongo import students_col
from app.core.face_embedding import generate_face_embedding
from app.utils.validators import validate_min_images

router = APIRouter()

SIM_THRESHOLD = 0.6


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@router.post("/register", tags=["Registration"])
def register_student(student: StudentRegistration):
    """
    Student Self Registration Endpoint
    """

    # ==========================
    # STUDENT ID CHECK
    # ==========================
    existing_student = students_col.find_one({"student_id": student.student_id})

    if existing_student:
        # Check which subjects are already registered
        duplicate_subjects = set(existing_student.get("subjects", [])) & set(student.subjects)
        new_subjects = set(student.subjects) - set(existing_student.get("subjects", []))

        if not new_subjects:
            # No new subjects to register
            raise HTTPException(
                status_code=400,
                detail=f"Already registered for all subjects: {', '.join(duplicate_subjects)}"
            )

        # If new subjects exist, we allow adding without face images
        updated_subjects = list(set(existing_student["subjects"]) | set(student.subjects))
        students_col.update_one(
            {"student_id": student.student_id},
            {"$set": {"subjects": updated_subjects}}
        )
        return {"message": f"Subjects updated successfully: {', '.join(new_subjects)}"}

    # ==========================
    # NEW STUDENT → VALIDATE FACE IMAGES
    # ==========================
    try:
        validate_min_images(student.face_images)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ==========================
    # FACE EMBEDDING GENERATION
    # ==========================
    # embeddings = []

    # for img in student.face_images:
    #     embedding = generate_face_embedding(img)

    #     if embedding is None:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Face not detected in one or more images"
    #         )
    #     embeddings.append(embedding)

    # avg_embedding = np.mean(np.array(embeddings), axis=0)

    embeddings = []

    for img in student.face_images:
        embedding = generate_face_embedding(img)
        if embedding is not None:
            embeddings.append(embedding)

    if len(embeddings) < 4:
        raise HTTPException(
            status_code=400,
            detail="At least 4 clear face images are required"
        )

    avg_embedding = np.mean(np.array(embeddings), axis=0)

    # ==========================
    # FACE DUPLICATE CHECK
    # ==========================
    for record in students_col.find({}, {"student_id": 1, "face_embedding": 1}):
        existing_embedding = np.array(record["face_embedding"])
        similarity = cosine_similarity(existing_embedding, avg_embedding)

        if similarity > SIM_THRESHOLD:
            raise HTTPException(
                status_code=400,
                detail=f"Face already registered (Student ID: {record['student_id']})"
            )

    # ==========================
    # INSERT NEW STUDENT
    # ==========================
    students_col.insert_one({
        "student_id": student.student_id,
        "full_name": student.full_name,
        "faculty": student.faculty,
        "subjects": student.subjects,
        "face_embedding": avg_embedding.tolist(),
        "registered_at": datetime.utcnow()
    })

    return {"message": "Registration successful"}

