"""
Unit tests for the Enzyme Inhibitor Competition Simulator.
"""

import pytest

from enzyme_competition import (
    bound_enzyme,
    calculate_activity,
    generate_e2_values,
    run_simulation,
    find_target_activity,
)


def test_bound_enzyme_returns_positive_value():
    result = bound_enzyme(
        enzyme_total=100,
        free_inhibitor=10,
        dissociation_constant=5,
    )

    assert result > 0
    assert result < 100


def test_activity_is_between_zero_and_one_hundred():
    result = calculate_activity(
        E1_total=100,
        inhibitor_total=80,
        K1=10,
        E2_total=50,
        K2=10,
    )

    assert 0 <= result["E1_activity_percent"] <= 100


def test_negative_concentration_is_rejected():
    with pytest.raises(ValueError):
        calculate_activity(
            E1_total=100,
            inhibitor_total=80,
            K1=10,
            E2_total=-5,
            K2=10,
        )


def test_generate_e2_values_has_correct_length():
    values = generate_e2_values(
        E2_min=0,
        E2_max=100,
        number_of_points=11,
    )

    assert len(values) == 11
    assert values[0] == 0
    assert values[-1] == 100


def test_run_simulation_handles_multiple_k2_values():
    results = run_simulation(
        E1_total=100,
        inhibitor_total=80,
        K1=10,
        E2_min=0,
        E2_max=100,
        K2_values=[5, 10],
        number_of_points=5,
    )

    assert len(results) == 10


def test_adding_e2_can_increase_e1_activity():
    without_e2 = calculate_activity(
        E1_total=100,
        inhibitor_total=80,
        K1=10,
        E2_total=0,
        K2=10,
    )

    with_e2 = calculate_activity(
        E1_total=100,
        inhibitor_total=80,
        K1=10,
        E2_total=200,
        K2=10,
    )

    assert with_e2["E1_activity_percent"] > without_e2["E1_activity_percent"]


def test_find_target_activity_returns_dictionary():
    results = run_simulation(
        E1_total=100,
        inhibitor_total=80,
        K1=10,
        E2_min=0,
        E2_max=500,
        K2_values=[10],
        number_of_points=20,
    )

    target_points = find_target_activity(results, target_activity=70)

    assert isinstance(target_points, dict)
    assert 10 in target_points
