import pytest

from app.calculations.percentile import calculate_percentile


def test_percentile_high_score():
    result = calculate_percentile(
        student_gpa=95,
        eligible_gpas=[50, 60, 70, 80, 90, 95, 100],
    )

    assert result == pytest.approx(71.4285714286)


def test_percentile_low_score():
    result = calculate_percentile(
        student_gpa=50,
        eligible_gpas=[50, 60, 70, 80, 90, 100],
    )

    assert result == 0


def test_percentile_middle_score():
    result = calculate_percentile(
        student_gpa=70,
        eligible_gpas=[50, 60, 70, 80, 90],
    )

    assert result == 40


def test_percentile_highest_score():
    result = calculate_percentile(
        student_gpa=100,
        eligible_gpas=[50, 60, 70, 80, 90, 100],
    )

    assert result == pytest.approx(83.3333333333)


def test_percentile_lowest_score():
    result = calculate_percentile(
        student_gpa=50,
        eligible_gpas=[50, 60, 70, 80, 90, 100],
    )

    assert result == 0


def test_percentile_single_score():
    result = calculate_percentile(
        student_gpa=80,
        eligible_gpas=[80],
    )

    assert result is None


def test_percentile_empty_scores():
    result = calculate_percentile(
        student_gpa=80,
        eligible_gpas=[],
    )

    assert result is None