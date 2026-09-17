# Calculate Cumulative Grade Point Average (CGPA)

def calculate_cgpa(
    semesters: list[tuple[float | None, float]],
) -> float | None:
    """
    Calculate CGPA across completed semesters.

    Each tuple contains:
        semester_gpa
        total_credits

    Incomplete semesters (GPA is None) are excluded.

    CGPA =
        Σ(semester_gpa × semester_credits)
        / Σ(semester_credits)
    """

    if not semesters:
        return None

    completed_semesters = [
        (gpa, credits)
        for gpa, credits in semesters
        if gpa is not None
    ]

    if not completed_semesters:
        return None

    total_credits = sum(
        credits
        for _, credits in completed_semesters
    )

    if total_credits <= 0:
        return None

    total_weighted_gpa = sum(
        gpa * credits
        for gpa, credits in completed_semesters
    )

    return total_weighted_gpa / total_credits