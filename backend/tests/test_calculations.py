from app.calculations.course_result import calculate_course_result
from app.calculations.grade_points import calculate_grade_point
from app.calculations.semester_gpa import calculate_semester_gpa
from app.calculations.cgpa import calculate_cgpa
from app.calculations.percentile import calculate_percentile
from app.calculations.projection import calculate_projected_gpa


# ---------------------------------------------------------
# Course Result Tests
# ---------------------------------------------------------

def test_course_result():
    grades = [
        (80, 100, 50),
        (90, 100, 50),
    ]

    result = calculate_course_result(grades)

    assert result == 85.0


def test_course_result_with_missing_marks():
    grades = [
        (80, 100, 50),
        (None, 100, 50),
    ]

    result = calculate_course_result(grades)

    assert result is None


def test_course_result_requires_100_percent_weight():
    grades = [
        (80, 100, 40),
        (90, 100, 40),
    ]

    result = calculate_course_result(grades)

    assert result is None


# ---------------------------------------------------------
# Grade Point Tests
# ---------------------------------------------------------

def test_grade_point_boundaries():
    assert calculate_grade_point(90) == 10.0
    assert calculate_grade_point(80) == 9.0
    assert calculate_grade_point(70) == 8.0
    assert calculate_grade_point(60) == 7.0
    assert calculate_grade_point(50) == 6.0
    assert calculate_grade_point(40) == 5.0
    assert calculate_grade_point(39.99) == 0.0


def test_grade_point_for_missing_percentage():
    assert calculate_grade_point(None) is None


# ---------------------------------------------------------
# Semester GPA Tests
# ---------------------------------------------------------

def test_semester_gpa():
    courses = [
        (9.0, 3),
        (8.0, 1),
    ]

    gpa = calculate_semester_gpa(courses)

    assert gpa == 8.75


def test_semester_gpa_incomplete():
    courses = [
        (9.0, 3),
        (None, 1),
    ]

    gpa = calculate_semester_gpa(courses)

    assert gpa is None


# ---------------------------------------------------------
# CGPA Tests
# ---------------------------------------------------------

def test_cgpa():
    semesters = [
        (8.75, 4),
        (7.50, 4),
    ]

    cgpa = calculate_cgpa(semesters)

    assert cgpa == 8.125


def test_cgpa_excludes_incomplete_semester():
    semesters = [
        (8.75, 4),
        (None, 4),
    ]

    cgpa = calculate_cgpa(semesters)

    assert cgpa == 8.75


# ---------------------------------------------------------
# Percentile Tests
# ---------------------------------------------------------

def test_percentile():
    eligible_gpas = [7.0, 8.75, 8.75, 9.5]

    percentile = calculate_percentile(
        student_gpa=8.75,
        eligible_gpas=eligible_gpas,
    )

    assert percentile == 25.0


def test_equal_gpas_have_same_percentile():
    eligible_gpas = [7.0, 8.75, 8.75, 9.5]

    first = calculate_percentile(8.75, eligible_gpas)
    second = calculate_percentile(8.75, eligible_gpas)

    assert first == second


def test_percentile_requires_two_students():
    percentile = calculate_percentile(
        student_gpa=8.0,
        eligible_gpas=[8.0],
    )

    assert percentile is None


# ---------------------------------------------------------
# GPA Projection Tests
# ---------------------------------------------------------

def test_projection_requires_three_semesters():
    projected = calculate_projected_gpa([7.0, 8.0])

    assert projected is None


def test_projection_with_three_semesters():
    projected = calculate_projected_gpa(
        [7.0, 8.0, 9.0]
    )

    assert projected == 10.0


def test_projection_is_clamped_to_valid_range():
    projected = calculate_projected_gpa(
        [8.0, 9.0, 10.0]
    )

    assert 0.0 <= projected <= 10.0