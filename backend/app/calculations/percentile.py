# Calculate Percentile

def calculate_percentile(
    student_gpa: float,
    eligible_gpas: list[float],
) -> float | None:
    """
    Calculate percentile for a student's semester GPA.

    Percentile =
        (# of eligible students with lower GPA
         / total eligible students) × 100

    Students with the same GPA receive the same percentile.

    Returns None when fewer than 2 students are eligible.
    """

    if len(eligible_gpas) < 2:
        return None

    lower_count = sum(                      #Count how many students have a GPA lower than this student's GPA.
        1
        for gpa in eligible_gpas
        if gpa < student_gpa
    )

    return (lower_count / len(eligible_gpas)) * 100