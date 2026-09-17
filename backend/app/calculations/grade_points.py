

#to convert percentage into grade point, we use the following scale:

def calculate_grade_point(
    percentage: float | None,
) -> float | None:
    """
    Convert a course percentage into a grade point.

    Grade scale:
        90 - 100  -> 10
        80 - <90  -> 9
        70 - <80  -> 8
        60 - <70  -> 7
        50 - <60  -> 6
        40 - <50  -> 5
        <40       -> 0

    None means the course result is incomplete.
    """

    if percentage is None:
        return None

    if percentage < 0 or percentage > 100:
        raise ValueError(
            "Percentage must be between 0 and 100."
        )

    if percentage >= 90:
        return 10.0
    elif percentage >= 80:
        return 9.0
    elif percentage >= 70:
        return 8.0
    elif percentage >= 60:
        return 7.0
    elif percentage >= 50:
        return 6.0
    elif percentage >= 40:
        return 5.0
    else:
        return 0.0