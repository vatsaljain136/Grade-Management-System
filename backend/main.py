from fastapi import FastAPI

from app.api.students import router as students_router
from app.api.assessments import router as assessments_router
from app.api.grades import router as grades_router
from app.api.uploads import router as uploads_router
from app.api.performance import router as performance_router
from app.api.enrollments import router as enrollments_router
from app.api.courses import router as courses_router
from app.api.semesters import router as semesters_router

app = FastAPI(
title="Grade Management System",
description="Backend API for managing students, assessments, grades, and performance.",
version="1.0.0",
)

app.include_router(students_router)
app.include_router(assessments_router)
app.include_router(grades_router)
app.include_router(uploads_router)
app.include_router(performance_router)
app.include_router(enrollments_router)
app.include_router(courses_router)
app.include_router(semesters_router)

@app.get("/")
def root():
    return {
    "message": "Grade Management System API is running."
    }
