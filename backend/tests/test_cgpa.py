from app.calculations.cgpa import calculate_cgpa


# ---------------------------------------------------------
# CGPA Tests
# ---------------------------------------------------------

def test_cgpa_single_semester():
    result = calculate_cgpa(
        [
            (8.0, 20),
        ]
    )

    assert result == 8.0


def test_cgpa_multiple_semesters():
    result = calculate_cgpa(
        [
            (8.0, 20),
            (9.0, 20),
        ]
    )

    expected = ((8.0 * 20) + (9.0 * 20)) / (20 + 20)

    assert result == expected


def test_cgpa_different_credits():
    result = calculate_cgpa(
        [
            (8.0, 20),
            (9.0, 30),
        ]
    )

    expected = ((8.0 * 20) + (9.0 * 30)) / (20 + 30)

    assert result == expected


def test_cgpa_equal_semester_gpa():
    result = calculate_cgpa(
        [
            (8.5, 20),
            (8.5, 30),
            (8.5, 25),
        ]
    )

    assert result == 8.5


def test_cgpa_zero():
    result = calculate_cgpa(
        [
            (0.0, 20),
            (0.0, 30),
        ]
    )

    assert result == 0.0


def test_cgpa_empty_semesters():
    result = calculate_cgpa([])

    assert result is None