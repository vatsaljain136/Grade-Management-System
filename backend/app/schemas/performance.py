from pydantic import BaseModel


#this file will evolve as i have just made a basic structure for my understanding as of now.
#this not completed in the least and will need some more thought and discussion
class CoursePerformance(BaseModel):
    course_id: int
    course_name: str
    credits: float
    percentage: float | None
    grade_point: float | None
    complete: bool                   #might add or remove fields later 


class SemesterPerformance(BaseModel):
    semester_id: int
    semester_name: str
    sequence: int
    gpa: float | None
    complete: bool
    courses: list[CoursePerformance]


class GPAHistoryItem(BaseModel):
    semester_name: str
    sequence: int
    gpa: float


class PerformanceResponse(BaseModel):
    student_id: int
    student_name: str

    semesters: list[SemesterPerformance]

    cgpa: float | None
    percentile: float | None

    gpa_history: list[GPAHistoryItem]

    projected_gpa: float | None
    projection_available: bool