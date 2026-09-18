from collections.abc import Iterable


def calculate_course_result(
    grades: Iterable[tuple[float | None, float, float]],      #each tuple contains (marks, maximum_marks, weight)
) -> float | None:
    """
    Calculate the weighted course percentage.

    Each tuple contains:
        marks
        maximum_marks
        weight
    """
    if any(maximum_marks <= 0 for _, maximum_marks, _ in grades):  #added after failing test(zero division err in case of maximum_marks=0)
        return None

    grades = list(grades)

    # No assessments
    if not grades:
        return None

    # Course result is incomplete if any mark is missing
    if any(marks is None for marks, _, _ in grades):
        return None

    # Course result is incomplete until weights total 100%
    total_weight = sum(weight for _, _, weight in grades)

    if total_weight != 100:
        return None

    result = sum(
        (marks / maximum_marks) * weight
        for marks, maximum_marks, weight in grades
    )

    return result