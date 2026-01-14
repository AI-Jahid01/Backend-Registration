# from fastapi import FastAPI
# from app.api.registration import router as registration_router

# app = FastAPI(
#     title="Smart Face Attendance - Registration API",
#     version="1.0.0"
# )

# app.include_router(registration_router)

# @app.get("/")
# def root():
#     return {"status": "Student Registration Service Running"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# # below code is using face_recognition library for local testing
# # backend/app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.registration import router as registration_router

# app = FastAPI(
#     title="Smart Face Attendance - Registration API",
#     version="1.0.0"
# )

# # ==========================
# # CORS CONFIGURATION
# # ==========================
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",   # Vite frontend
#         "http://127.0.0.1:5173"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],          # IMPORTANT → enables OPTIONS
#     allow_headers=["*"],
# )

# # ==========================
# # ROUTERS
# # ==========================
# # app.include_router(registration_router, prefix="/api")
# app.include_router(registration_router, prefix="/api")  # ✅ keep this
# # app.include_router(registration_router)  # no prefix
# # app.include_router(registration_router, prefix="/api")

# # ==========================
# # HEALTH CHECK
# # ==========================
# @app.get("/")
# def root():
#     return {"status": "Student Registration Service Running"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


# below code is using face_recognition library for deployment

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.registration import router as registration_router
from app.db.mongo import students_col
from pymongo.errors import PyMongoError

app = FastAPI(
    title="Smart Face Attendance - Registration API",
    version="1.0.0"
)

@app.on_event("startup")
def startup_db():
    try:
        students_col.create_index("student_id", unique=True)
        print("✅ MongoDB index ensured")
    except PyMongoError as e:
        print("❌ MongoDB connection failed:", e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(registration_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Student Registration Service Running"}
