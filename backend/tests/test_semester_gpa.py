import pytest

from app.calculations.semester_gpa import calculate_semester_gpa


def test_semester_gpa_single_course():
    result = calculate_semester_gpa(
        [
            (8.0, 3),
        ]
    )

    assert result == 8.0


def test_semester_gpa_multiple_courses():
    result = calculate_semester_gpa(
        [
            (8.0, 3),
            (9.0, 4),
            (7.0, 3),
        ]
    )

    expected = (
        (8.0 * 3)
        + (9.0 * 4)
        + (7.0 * 3)
    ) / (3 + 4 + 3)

    assert result == pytest.approx(expected)


def test_semester_gpa_with_different_credits():
    result = calculate_semester_gpa(
        [
            (10.0, 1),
            (5.0, 5),
        ]
    )

    expected = (
        (10.0 * 1)
        + (5.0 * 5)
    ) / 6

    assert result == pytest.approx(expected)


def test_semester_gpa_incomplete_course():
    result = calculate_semester_gpa(
        [
            (8.0, 3),
            (None, 4),
        ]
    )

    assert result is None


def test_semester_gpa_zero_credits():
    result = calculate_semester_gpa(
        [
            (8.0, 0),
        ]
    )

    assert result is None


def test_semester_gpa_empty_courses():
    result = calculate_semester_gpa([])

    assert result is None