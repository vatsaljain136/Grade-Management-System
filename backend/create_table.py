from app.database.base import Base
from app.database.connection import engine

# Import all models so SQLAlchemy knows about them
from app.models import (
    Student,
    Course,
    Semester,
    Enrollment,
    Assessment,
    Grade,
)


Base.metadata.create_all(bind=engine)

print("All tables created successfully!")