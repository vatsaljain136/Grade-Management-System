from app.calculations.grade_points import calculate_grade_point


# ---------------------------------------------------------
# Grade Point Tests
# ---------------------------------------------------------

def test_grade_point_a():
    result = calculate_grade_point(90)
    assert result == 10


def test_grade_point_b():
    result = calculate_grade_point(80)
    assert result == 9


def test_grade_point_c():
    result = calculate_grade_point(70)
    assert result == 8


def test_grade_point_d():
    result = calculate_grade_point(60)
    assert result == 7


def test_grade_point_e():
    result = calculate_grade_point(50)
    assert result == 6


def test_grade_point_f():
    result = calculate_grade_point(40)
    assert result == 5


def test_grade_point_fail():
    result = calculate_grade_point(30)
    assert result == 0


def test_grade_point_zero():
    result = calculate_grade_point(0)
    assert result == 0


def test_grade_point_full_marks():
    result = calculate_grade_point(100)
    assert result == 10