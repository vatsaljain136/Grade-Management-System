import pytest

from app.calculations.projection import calculate_projected_gpa


def test_projected_gpa_increasing_trend():
    result = calculate_projected_gpa(
        [6.0, 7.0, 8.0]
    )

    assert result == pytest.approx(9.0)


def test_projected_gpa_decreasing_trend():
    result = calculate_projected_gpa(
        [9.0, 8.0, 7.0]
    )

    assert result == pytest.approx(6.0)


def test_projected_gpa_constant_values():
    result = calculate_projected_gpa(
        [8.0, 8.0, 8.0]
    )

    assert result == pytest.approx(8.0)


def test_projected_gpa_fewer_than_three_semesters():
    result = calculate_projected_gpa(
        [8.0, 9.0]
    )

    assert result is None


def test_projected_gpa_clamped_to_maximum():
    result = calculate_projected_gpa(
        [8.0, 10.0, 10.0]
    )

    assert result == pytest.approx(10.0)


def test_projected_gpa_clamped_to_minimum():
    result = calculate_projected_gpa(
        [2.0, 1.0, 0.0]
    )

    assert result == pytest.approx(0.0)