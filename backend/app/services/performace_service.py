from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.grade import Grade
from app.models.semester import Semester
from app.models.student import Student

from app.calculations.course_result import calculate_course_result
from app.calculations.grade_points import calculate_grade_point
from app.calculations.semester_gpa import calculate_semester_gpa
from app.calculations.cgpa import calculate_cgpa
from app.calculations.percentile import calculate_percentile
from app.calculations.projection import calculate_projected_gpa

from app.schemas.performance import (
    CoursePerformance,
    SemesterPerformance,
    GPAHistoryItem,
    PerformanceResponse,
)

#this is the main orchestrator of the calculation system.


def get_student_performance(
    db: Session,
    student_id: int,
) -> PerformanceResponse | None:

    student = db.scalar(
        select(Student).where(
            Student.id == student_id
        )
    )

    if student is None:
        return None

    # Get all semesters in sequence order.
    semesters = list(
        db.scalars(
            select(Semester).order_by(
                Semester.sequence
            )
        ).all()
    )

    semester_results: list[SemesterPerformance] = []

    for semester in semesters:

        # Get courses in which this student is enrolled
        # for this semester.
        enrollments = list(
            db.scalars(
                select(Enrollment).where(
                    Enrollment.student_id == student_id,
                    Enrollment.semester_id == semester.id,
                )
            ).all()
        )

        course_results: list[CoursePerformance] = []
        semester_calculation_data: list[
            tuple[float | None, float]
        ] = []

        for enrollment in enrollments:

            course = db.scalar(
                select(Course).where(
                    Course.id == enrollment.course_id
                )
            )

            if course is None:
                continue

            assessments = list(
                db.scalars(
                    select(Assessment).where(
                        Assessment.course_id
                        == course.id,
                        Assessment.semester_id
                        == semester.id,
                    )
                ).all()
            )

            grade_data: list[
                tuple[float | None, float, float]
            ] = []

            for assessment in assessments:

                grade = db.scalar(
                    select(Grade).where(
                        Grade.student_id == student_id,
                        Grade.assessment_id
                        == assessment.id,
                    )
                )

                marks = (
                    float(grade.marks)
                    if grade is not None
                    and grade.marks is not None
                    else None
                )

                grade_data.append(
                    (
                        marks,
                        float(assessment.maximum_marks),
                        float(assessment.weight),
                    )
                )

            percentage = calculate_course_result(
                grade_data
            )

            grade_point = calculate_grade_point(
                percentage
            )

            complete = (
                percentage is not None
                and grade_point is not None
            )

            course_results.append(
                CoursePerformance(
                    course_id=course.id,
                    course_name=course.name,
                    credits=float(course.credits),
                    percentage=percentage,
                    grade_point=grade_point,
                    complete=complete,
                )
            )

            semester_calculation_data.append(
                (
                    grade_point,
                    float(course.credits),
                )
            )

        semester_gpa = calculate_semester_gpa(
            semester_calculation_data
        )

        semester_complete = semester_gpa is not None

        semester_results.append(
            SemesterPerformance(
                semester_id=semester.id,
                semester_name=semester.name,
                sequence=semester.sequence,
                gpa=semester_gpa,
                complete=semester_complete,
                courses=course_results,
            )
        )

    # Only completed semesters are used for CGPA.
    completed_semesters = [
        (
            semester.gpa,
            sum(
                course.credits
                for course in semester.courses
            ),
        )
        for semester in semester_results
        if semester.complete
    ]

    cgpa = calculate_cgpa(
        completed_semesters
    )

    # GPA history contains completed semesters only.
    gpa_history = [
        GPAHistoryItem(
            semester_name=semester.semester_name,
            sequence=semester.sequence,
            gpa=semester.gpa,
        )
        for semester in semester_results
        if semester.complete
    ]

    # Projection requires at least 3 completed semesters.
    completed_gpas = [
        semester.gpa
        for semester in semester_results
        if semester.complete
    ]

    projected_gpa = calculate_projected_gpa(
        completed_gpas
    )

    # Percentile requires the student's latest
    # completed semester and comparison with students
    # from the same batch and semester.
    percentile = None

    if semester_results:
        completed_student_semesters = [
            semester
            for semester in semester_results
            if semester.complete
        ]

        if completed_student_semesters:
            latest_semester = completed_student_semesters[-1]

            percentile = calculate_student_percentile(
                db=db,
                student=student,
                semester_id=latest_semester.semester_id,
                student_gpa=latest_semester.gpa,
            )

    return PerformanceResponse(
        student_id=student.id,
        student_name=student.name,
        semesters=semester_results,
        cgpa=cgpa,
        percentile=percentile,
        gpa_history=gpa_history,
        projected_gpa=projected_gpa,
        projection_available=projected_gpa is not None,
    )


def calculate_student_percentile(
    db: Session,
    student: Student,
    semester_id: int,
    student_gpa: float,
) -> float | None:

    student_ids = list(
        db.scalars(
            select(Student.id).where(
                Student.batch == student.batch
            )
        ).all()
    )

    eligible_gpas: list[float] = []

    for student_id in student_ids:

        if student_id == student.id:
            eligible_gpas.append(student_gpa)
            continue

        performance = get_student_semester_gpa(
            db=db,
            student_id=student_id,
            semester_id=semester_id,
        )

        if performance is not None:
            eligible_gpas.append(performance)

    return calculate_percentile(
        student_gpa=student_gpa,
        eligible_gpas=eligible_gpas,
    )


def get_student_semester_gpa(
    db: Session,
    student_id: int,
    semester_id: int,
) -> float | None:

    enrollments = list(
        db.scalars(
            select(Enrollment).where(
                Enrollment.student_id == student_id,
                Enrollment.semester_id == semester_id,
            )
        ).all()
    )

    if not enrollments:
        return None

    course_data: list[
        tuple[float | None, float]
    ] = []

    for enrollment in enrollments:

        course = db.scalar(
            select(Course).where(
                Course.id == enrollment.course_id
            )
        )

        if course is None:
            return None

        assessments = list(
            db.scalars(
                select(Assessment).where(
                    Assessment.course_id
                    == course.id,
                    Assessment.semester_id
                    == semester_id,
                )
            ).all()
        )

        grade_data: list[
            tuple[float | None, float, float]
        ] = []

        for assessment in assessments:

            grade = db.scalar(
                select(Grade).where(
                    Grade.student_id == student_id,
                    Grade.assessment_id == assessment.id,
                )
            )

            marks = (
                float(grade.marks)
                if grade is not None
                and grade.marks is not None
                else None
            )

            grade_data.append(
                (
                    marks,
                    float(assessment.maximum_marks),
                    float(assessment.weight),
                )
            )

        percentage = calculate_course_result(
            grade_data
        )

        grade_point = calculate_grade_point(
            percentage
        )

        course_data.append(
            (
                grade_point,
                float(course.credits),
            )
        )

    return calculate_semester_gpa(course_data)