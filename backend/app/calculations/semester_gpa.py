def calculate_semester_gpa(
    courses: list[tuple[float | None, float]],          #tuple contains (grade_point, credits)
) -> float | None:
    """
    Calculate Semester GPA using:

        GPA = Σ(grade_point × credits) / Σ(credits)

    Each tuple contains:
        grade_point
        credits

    Returns None if any enrolled course is incomplete.
    """

    if not courses:
        return None

    # A missing grade point means the course is incomplete. in that case, the semester GPA is None
    if any(grade_point is None for grade_point, _ in courses):
        return None

    total_credits = sum(
        credits for _, credits in courses
    )

    if total_credits <= 0:
        return None

    total_weighted_points = sum(
        grade_point * credits
        for grade_point, credits in courses
    )

    return total_weighted_points / total_credits