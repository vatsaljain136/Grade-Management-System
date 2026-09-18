from sqlalchemy import select

from app.database.session import SessionLocal

from app.models import (
    Assessment,
    Course,
    Enrollment,
    Grade,
    Semester,
    Student,
)


def seed_data():

    db = SessionLocal()

    try:

        # ---------------------------------------------------------
        # 1. Students
        # ---------------------------------------------------------

        students_data = [

            {
                "student_code": "STU001",
                "name": "Asha Sharma",
                "email": "asha@example.com",
                "batch": "2026",
            },

            {
                "student_code": "STU002",
                "name": "Rohan Verma",
                "email": "rohan@example.com",
                "batch": "2026",
            },

            {
                "student_code": "STU003",
                "name": "Priya Singh",
                "email": "priya@example.com",
                "batch": "2026",
            },

            {
                "student_code": "STU004",
                "name": "Arjun Mehta",
                "email": "arjun@example.com",
                "batch": "2026",
            },

        ]

        students = {}

        for data in students_data:

            student = db.scalar(
                select(Student).where(
                    Student.student_code == data["student_code"]
                )
            )

            if student is None:

                student = Student(**data)

                db.add(student)

                db.flush()

            students[data["student_code"]] = student


        # ---------------------------------------------------------
        # 2. Courses
        # ---------------------------------------------------------

        courses_data = [

            {
                "code": "PY101",
                "name": "Python Programming",
                "credits": 3,
            },

            {
                "code": "DB101",
                "name": "Database Systems",
                "credits": 1,
            },

        ]

        courses = {}

        for data in courses_data:

            course = db.scalar(
                select(Course).where(
                    Course.code == data["code"]
                )
            )

            if course is None:

                course = Course(**data)

                db.add(course)

                db.flush()

            courses[data["code"]] = course


        # ---------------------------------------------------------
        # 3. Semesters
        # ---------------------------------------------------------

        semesters_data = [

            {
                "name": "Semester 1",
                "sequence": 1,
            },

            {
                "name": "Semester 2",
                "sequence": 2,
            },

            {
                "name": "Semester 3",
                "sequence": 3,
            },

        ]

        semesters = {}

        for data in semesters_data:

            semester = db.scalar(
                select(Semester).where(
                    Semester.sequence == data["sequence"]
                )
            )

            if semester is None:

                semester = Semester(**data)

                db.add(semester)

                db.flush()

            semesters[data["sequence"]] = semester


        # ---------------------------------------------------------
        # 4. Enrollments
        # ---------------------------------------------------------

        for student in students.values():

            for semester in semesters.values():

                for course in courses.values():

                    enrollment = db.scalar(
                        select(Enrollment).where(
                            Enrollment.student_id == student.id,
                            Enrollment.course_id == course.id,
                            Enrollment.semester_id == semester.id,
                        )
                    )

                    if enrollment is None:

                        db.add(
                            Enrollment(
                                student_id=student.id,
                                course_id=course.id,
                                semester_id=semester.id,
                            )
                        )

        db.flush()


        # ---------------------------------------------------------
        # 5. Assessments
        # ---------------------------------------------------------

        assessments_data = []

        for semester in semesters.values():

            for course in courses.values():

                assessments_data.extend(
                    [

                        {
                            "course_id": course.id,
                            "semester_id": semester.id,
                            "title": "Internal Assessment",
                            "type": "assignment",
                            "maximum_marks": 100,
                            "weight": 50,
                        },

                        {
                            "course_id": course.id,
                            "semester_id": semester.id,
                            "title": "Final Assessment",
                            "type": "exam",
                            "maximum_marks": 100,
                            "weight": 50,
                        },

                    ]
                )

        assessments = {}

        for data in assessments_data:

            assessment = db.scalar(
                select(Assessment).where(
                    Assessment.course_id == data["course_id"],
                    Assessment.semester_id == data["semester_id"],
                    Assessment.title == data["title"],
                )
            )

            if assessment is None:

                assessment = Assessment(**data)

                db.add(assessment)

                db.flush()

            key = (
                data["course_id"],
                data["semester_id"],
                data["title"],
            )

            assessments[key] = assessment


        # ---------------------------------------------------------
        # 6. Grades
        # ---------------------------------------------------------

        grade_values = {

            "STU001": {

                1: {
                    "PY101": (80, 90),
                    "DB101": (70, 80),
                },

                2: {
                    "PY101": (85, 88),
                    "DB101": (75, 82),
                },

                3: {
                    "PY101": (90, 92),
                    "DB101": (85, 90),
                },

            },

            "STU002": {

                1: {
                    "PY101": (75, 80),
                    "DB101": (65, 70),
                },

                2: {
                    "PY101": (78, 82),
                    "DB101": (72, 75),
                },

                3: {
                    "PY101": (85, 88),
                    "DB101": (80, 84),
                },

            },

            "STU003": {

                1: {
                    "PY101": (90, 95),
                    "DB101": (85, 90),
                },

                2: {
                    "PY101": (88, 92),
                    "DB101": (82, 86),
                },

                3: {
                    "PY101": (92, 94),
                    "DB101": (90, 93),
                },

            },

            "STU004": {

                1: {
                    "PY101": (60, 70),
                    "DB101": (55, 65),
                },

                2: {
                    "PY101": (68, 72),
                    "DB101": (60, 70),
                },

                3: {
                    "PY101": (75, 78),
                    "DB101": (70, 74),
                },

            },

        }

        for student_code, semester_data in grade_values.items():

            student = students[student_code]

            for sequence, course_data in semester_data.items():

                semester = semesters[sequence]

                for course_code, marks_pair in course_data.items():

                    course = courses[course_code]

                    assessment_1 = assessments[
                        (
                            course.id,
                            semester.id,
                            "Internal Assessment",
                        )
                    ]

                    assessment_2 = assessments[
                        (
                            course.id,
                            semester.id,
                            "Final Assessment",
                        )
                    ]

                    marks_1, marks_2 = marks_pair

                    for assessment, marks in [
                        (assessment_1, marks_1),
                        (assessment_2, marks_2),
                    ]:

                        existing_grade = db.scalar(
                            select(Grade).where(
                                Grade.student_id == student.id,
                                Grade.assessment_id == assessment.id,
                            )
                        )

                        if existing_grade is None:

                            db.add(
                                Grade(
                                    student_id=student.id,
                                    assessment_id=assessment.id,
                                    marks=marks,
                                )
                            )

        db.commit()

        print("Seed data inserted successfully.")

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


if __name__ == "__main__":

    seed_data()