"""
Plotting functions for the Enzyme Inhibitor Competition Simulator.
"""

import matplotlib.pyplot as plt


def plot_activity(results, output_path, target_activity=None):
    """
    Plot E1 activity as a function of E2 concentration.

    Each K2 value is plotted as a separate curve.
    """
    if not results:
        raise ValueError("No results to plot.")

    k2_values = sorted(set(row["K2"] for row in results))

    plt.figure(figsize=(8, 6))

    for K2 in k2_values:
        rows = [row for row in results if row["K2"] == K2]
        rows = sorted(rows, key=lambda row: row["E2_total"])

        e2_values = [row["E2_total"] for row in rows]
        activity_values = [row["E1_activity_percent"] for row in rows]

        plt.plot(e2_values, activity_values, marker="o", markersize=3, label=f"K2 = {K2}")

    if target_activity is not None:
        plt.axhline(
            y=target_activity,
            linestyle="--",
            label=f"Target activity = {target_activity}%",
        )

    plt.xlabel("E2 total concentration")
    plt.ylabel("E1 activity (%)")
    plt.title("Effect of E2 Concentration on E1 Activity")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
