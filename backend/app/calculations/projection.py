
#this is basically manual implementation of linear regression, might change it to scikit-learn in future after consulting with puru sir.


def calculate_projected_gpa(
    gpas: list[float],
) -> float | None:
    """
    Project the next semester GPA using a straight-line trend.

    Projection is available only when there are at least
    3 completed semester GPAs.

    The projected GPA is clamped to the valid GPA range:
        0 <= GPA <= 10

    Returns None when fewer than 3 completed semesters exist.
    """

    if len(gpas) < 3:
        return None

    n = len(gpas)

    x_values = list(range(1, n + 1))

    x_mean = sum(x_values) / n
    y_mean = sum(gpas) / n

    numerator = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(x_values, gpas)
    )

    denominator = sum(
        (x - x_mean) ** 2
        for x in x_values
    )

    if denominator == 0:
        return None

    slope = numerator / denominator

    intercept = y_mean - slope * x_mean

    next_x = n + 1

    projected_gpa = intercept + slope * next_x

    # GPA must remain within 0-10.
    projected_gpa = max(
        0.0,
        min(10.0, projected_gpa),
    )

    return projected_gpa