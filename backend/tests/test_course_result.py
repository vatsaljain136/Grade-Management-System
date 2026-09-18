import pytest

from app.calculations.course_result import calculate_course_result


def test_course_result_pass():
    result = calculate_course_result(
        [
            (80, 100, 100),
        ]
    )

    assert result == 80


def test_course_result_zero_marks():
    result = calculate_course_result(
        [
            (0, 100, 100),
        ]
    )

    assert result == 0


def test_course_result_full_marks():
    result = calculate_course_result(
        [
            (100, 100, 100),
        ]
    )

    assert result == 100


def test_course_result_fractional_marks():
    result = calculate_course_result(
        [
            (75, 80, 100),
        ]
    )

    assert result == pytest.approx(93.75)


def test_course_result_invalid_maximum_marks():
    result = calculate_course_result(
        [
            (50, 0, 100),
        ]
    )

    assert result is None