"""
Main program for the Enzyme Inhibitor Competition Simulator.

The program asks the user for biochemical parameters, runs the simulation,
saves the calculated results as a CSV file, and generates a plot.
"""

import csv
import os

from enzyme_competition import run_simulation, find_target_activity
from plot_results import plot_activity


def parse_k2_values(user_input):
    """
    Convert a comma-separated string of K2 values into a list of floats.
    """
    try:
        values = [float(value.strip()) for value in user_input.split(",")]
    except ValueError as error:
        raise ValueError("K2 values must be numbers separated by commas.") from error

    if not values:
        raise ValueError("At least one K2 value is required.")

    return values


def save_results_to_csv(results, output_path):
    """
    Save simulation results to a CSV file.
    """
    fieldnames = [
        "E2_total",
        "K2",
        "I_free",
        "E1_bound",
        "E2_bound",
        "E1_activity_percent",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def main():
    """
    Run the simulator.
    """
    print("Enzyme Inhibitor Competition Simulator")
    print("--------------------------------------")

    try:
        K1 = float(input("Enter K1 in nM: "))
        E1_total = float(input("Enter total E1 concentration in nM: "))
        inhibitor_total = float(input("Enter total inhibitor concentration in nM: "))
        E2_min = float(input("Enter minimum E2 concentration in nM: "))
        E2_max = float(input("Enter maximum E2 concentration in nM: "))
        K2_values = parse_k2_values(input("Enter K2 values separated by commas: "))
        target_activity_input = input(
            "Enter target activity percentage, or press Enter to skip: "
        )

        target_activity = None
        if target_activity_input.strip():
            target_activity = float(target_activity_input)

        results = run_simulation(
            E1_total=E1_total,
            inhibitor_total=inhibitor_total,
            K1=K1,
            E2_min=E2_min,
            E2_max=E2_max,
            K2_values=K2_values,
            number_of_points=100,
        )

        os.makedirs("output", exist_ok=True)

        csv_path = os.path.join("output", "simulation_results.csv")
        plot_path = os.path.join("output", "activity_plot.png")

        save_results_to_csv(results, csv_path)
        plot_activity(results, plot_path, target_activity=target_activity)

        print("\nSimulation completed successfully.")
        print(f"Results saved to: {csv_path}")
        print(f"Plot saved to: {plot_path}")

        if target_activity is not None:
            target_points = find_target_activity(results, target_activity)

            print(f"\nE2 concentration needed to reach {target_activity}% activity:")
            for K2, E2_value in target_points.items():
                if E2_value is None:
                    print(f"K2 = {K2}: target activity was not reached")
                else:
                    print(f"K2 = {K2}: E2 ≈ {E2_value:.2f} nM")

    except ValueError as error:
        print(f"\nInput error: {error}")


if __name__ == "__main__":
    main()
