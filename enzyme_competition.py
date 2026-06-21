"""
Core calculations for the Enzyme Inhibitor Competition Simulator.

This module contains the biochemical binding model used to calculate how an
inhibitor is distributed between two enzymes and how much activity remains for
enzyme 1.
"""


def validate_inputs(E1_total, inhibitor_total, K1, E2_total, K2):
    """
    Validate input values for one simulation point.

    Concentrations must be non-negative.
    Dissociation constants must be positive.
    E1_total must be positive because activity is calculated relative to E1.
    """
    if E1_total <= 0:
        raise ValueError("E1_total must be greater than zero.")

    if inhibitor_total < 0:
        raise ValueError("Inhibitor_total cannot be negative.")

    if E2_total < 0:
        raise ValueError("E2_total cannot be negative.")

    if K1 <= 0:
        raise ValueError("K1 must be greater than zero.")

    if K2 <= 0:
        raise ValueError("K2 must be greater than zero.")


def bound_enzyme(enzyme_total, free_inhibitor, dissociation_constant):
    """
    Calculate how much inhibitor is bound to an enzyme.

    Formula:
    bound = enzyme_total * free_inhibitor / (K + free_inhibitor)
    """
    return enzyme_total * free_inhibitor / (dissociation_constant + free_inhibitor)


def mass_balance_error(free_inhibitor, E1_total, inhibitor_total, K1, E2_total, K2):
    """
    Calculate the mass-balance error for a given free inhibitor concentration.

    The correct free inhibitor concentration satisfies:

    inhibitor_total = free_inhibitor + E1_bound + E2_bound
    """
    E1_bound = bound_enzyme(E1_total, free_inhibitor, K1)
    E2_bound = bound_enzyme(E2_total, free_inhibitor, K2)

    return free_inhibitor + E1_bound + E2_bound - inhibitor_total


def solve_free_inhibitor(E1_total, inhibitor_total, K1, E2_total, K2):
    """
    Solve for the free inhibitor concentration using the bisection method.

    The value must be between 0 and inhibitor_total.
    """
    validate_inputs(E1_total, inhibitor_total, K1, E2_total, K2)

    if inhibitor_total == 0:
        return 0.0

    low = 0.0
    high = inhibitor_total

    for _ in range(100):
        mid = (low + high) / 2
        error = mass_balance_error(mid, E1_total, inhibitor_total, K1, E2_total, K2)

        if error > 0:
            high = mid
        else:
            low = mid

    return (low + high) / 2


def calculate_activity(E1_total, inhibitor_total, K1, E2_total, K2):
    """
    Calculate one simulation point.

    Returns a dictionary containing:
    - E2_total
    - K2
    - I_free
    - E1_bound
    - E2_bound
    - E1_activity_percent
    """
    free_inhibitor = solve_free_inhibitor(
        E1_total=E1_total,
        inhibitor_total=inhibitor_total,
        K1=K1,
        E2_total=E2_total,
        K2=K2,
    )

    E1_bound = bound_enzyme(E1_total, free_inhibitor, K1)
    E2_bound = bound_enzyme(E2_total, free_inhibitor, K2)

    activity_percent = 100 * (1 - E1_bound / E1_total)

    return {
        "E2_total": E2_total,
        "K2": K2,
        "I_free": free_inhibitor,
        "E1_bound": E1_bound,
        "E2_bound": E2_bound,
        "E1_activity_percent": activity_percent,
    }


def generate_e2_values(E2_min, E2_max, number_of_points):
    """
    Generate evenly spaced E2 concentration values.
    """
    if E2_min < 0 or E2_max < 0:
        raise ValueError("E2 concentrations cannot be negative.")

    if E2_max < E2_min:
        raise ValueError("E2_max must be greater than or equal to E2_min.")

    if number_of_points < 2:
        raise ValueError("number_of_points must be at least 2.")

    step = (E2_max - E2_min) / (number_of_points - 1)
    return [E2_min + i * step for i in range(number_of_points)]


def run_simulation(
    E1_total,
    inhibitor_total,
    K1,
    E2_min,
    E2_max,
    K2_values,
    number_of_points=100,
):
    """
    Run the simulation for several E2 concentrations and several K2 values.

    Returns a list of dictionaries.
    """
    if not K2_values:
        raise ValueError("At least one K2 value is required.")

    E2_values = generate_e2_values(E2_min, E2_max, number_of_points)

    results = []

    for K2 in K2_values:
        for E2_total in E2_values:
            result = calculate_activity(
                E1_total=E1_total,
                inhibitor_total=inhibitor_total,
                K1=K1,
                E2_total=E2_total,
                K2=K2,
            )
            results.append(result)

    return results


def find_target_activity(results, target_activity):
    """
    Find the first E2 concentration that reaches the target activity for each K2.

    Returns a dictionary:
    K2 -> E2 concentration or None if the target was not reached.
    """
    if target_activity < 0 or target_activity > 100:
        raise ValueError("Target activity must be between 0 and 100.")

    target_points = {}
    k2_values = sorted(set(row["K2"] for row in results))

    for K2 in k2_values:
        rows = [row for row in results if row["K2"] == K2]
        rows = sorted(rows, key=lambda row: row["E2_total"])

        target_points[K2] = None

        for row in rows:
            if row["E1_activity_percent"] >= target_activity:
                target_points[K2] = row["E2_total"]
                break

    return target_points
