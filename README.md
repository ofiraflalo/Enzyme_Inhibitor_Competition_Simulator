# Enzyme Inhibitor Competition Simulator

## Overview

Enzyme Inhibitor Competition Simulator is a Python-based biochemical simulation tool designed to model competition between two enzymes or proteins for the same inhibitor.

In many biological and biochemical systems, inhibitors bind to enzymes and reduce their activity. However, when more than one protein can bind the same inhibitor, competition can occur. This means that a second protein may bind part of the inhibitor and reduce the amount of inhibitor available to bind the main enzyme of interest.

This tool simulates how the activity of a main enzyme changes when a competing enzyme or protein is added to the system.

The program calculates the distribution of inhibitor between free inhibitor, inhibitor bound to enzyme 1, and inhibitor bound to enzyme 2. It then estimates the remaining activity of enzyme 1 and generates plots showing how enzyme 1 activity changes as the concentration of enzyme 2 increases.

## Biological Motivation

Enzymes are proteins that help chemical reactions occur faster in biological systems. Inhibitors are molecules that can bind to enzymes and reduce their activity.

In a simple inhibition model, one enzyme binds one inhibitor. However, real biological systems can be more complex. Different proteins may bind the same molecule and therefore compete with each other.

In this project, enzyme 1, called `E1`, is the main enzyme of interest. When the inhibitor binds to `E1`, the activity of `E1` decreases.

A second enzyme or protein, called `E2`, can also bind the same inhibitor. If `E2` binds part of the inhibitor, less inhibitor may remain available to bind `E1`. As a result, adding `E2` may increase the remaining activity of `E1`.

This type of simulation can help visualize biochemical competition and understand how changes in concentration and binding strength affect enzyme activity.

## Project Goal

The purpose of this project is to create a simple computational tool that simulates competition between two enzymes or proteins for the same inhibitor.

The software receives concentrations and binding constants from the user, solves the equilibrium binding model, and calculates the predicted activity of enzyme 1.

The program also generates graphs that allow the user to compare different binding strengths of enzyme 2 and understand how strongly enzyme 2 must bind the inhibitor in order to affect enzyme 1 activity.

Initially, the project focuses on a simple two-enzyme model, but it can later be expanded to include more proteins, experimental data fitting, or additional inhibition models.

## Model Description

The model includes two enzymes or proteins, `E1` and `E2`, and one inhibitor, `I`.

The binding reactions are:

```text
E1 + I ⇌ E1I
E2 + I ⇌ E2I
```
Where:

E1 = main enzyme of interest

E2 = competing enzyme or protein

I = free inhibitor

E1I = enzyme 1 bound to inhibitor

E2I = enzyme 2 bound to inhibitor

The binding strength is described by dissociation constants:

K1 = dissociation constant for E1 and the inhibitor

K2 = dissociation constant for E2 and the inhibitor

A lower dissociation constant means stronger binding.
The dissociation constants are:

```text
K1 = [E1][I] / [E1I]
K2 = [E2][I] / [E2I]
```
For each value of total E2 concentration, the program solves the inhibitor mass-balance equation:

```text
I_total = I_free + E1_bound + E2_bound
```
where:

```text
E1_bound = E1_total * I_free / (K1 + I_free)
E2_bound = E2_total * I_free / (K2 + I_free)
```
The activity of enzyme 1 is calculated as the fraction of E1 that is not bound to inhibitor:

```text
Activity (%) = 100 * (1 - E1_bound / E1_total)
```
For each concentration of E2, the program calculates how much inhibitor is free and how much inhibitor is bound to each enzyme.

## Input

The program expects numerical input from the user.  
All concentrations should be given in the same units, for example nM.

The required input values are:

- `K1`: dissociation constant between enzyme 1 and the inhibitor
- `E1_total`: total concentration of enzyme 1
- `Inhibitor_total`: total concentration of inhibitor
- `E2_min`: minimum concentration of enzyme 2 to test
- `E2_max`: maximum concentration of enzyme 2 to test
- `K2_values`: one or more dissociation constants between enzyme 2 and the inhibitor

Optional input:

- `Target_activity`: selected activity percentage, for example 80%

Example input:

```text
K1 = 10 nM
E1_total = 100 nM
Inhibitor_total = 80 nM
E2 concentration range = 0-500 nM
K2 values = 5, 10, 50, 100 nM
Target activity = 80%
```

## Output

The tool generates calculated values and a graph.

For each tested `E2` concentration, the program calculates:

- `I_free`: free inhibitor concentration
- `E1_bound`: amount of inhibitor bound to enzyme 1
- `E2_bound`: amount of inhibitor bound to enzyme 2
- `E1_activity_percent`: predicted remaining activity of enzyme 1

Example output table:

| E2_total | K2 | I_free | E1_bound | E2_bound | E1_activity_percent |
|---------:|---:|-------:|---------:|---------:|--------------------:|
| 0        | 10 | 5.2    | 34.2     | 0        | 65.8                |
| 50       | 10 | 4.1    | 29.1     | 14.5     | 70.9                |
| 100      | 10 | 3.3    | 24.8     | 24.8     | 75.2                |
The program also generates a plot of enzyme 1 activity as a function of enzyme 2 concentration.

In the graph:

- The x-axis shows the total concentration of `E2`
- The y-axis shows the predicted activity of `E1` in percent

If several `K2` values are entered, the program plots several curves on the same graph. Each curve represents a different binding strength of enzyme 2 to the inhibitor.

The program can also mark the concentration of `E2` needed to reach a selected target activity, such as 80%.

## Limitations

This project uses a simplified biochemical model.

The model assumes that:

- Both enzymes bind the same inhibitor
- Binding reaches equilibrium
- The inhibitor binds independently to each enzyme
- Enzyme 1 activity depends only on whether enzyme 1 is bound to inhibitor
- All concentrations are given in the same units

The model does not include more complex biological effects such as cooperativity, irreversible inhibition, enzyme degradation, or full enzyme kinetics.

Therefore, this project is intended as a simple simulation and visualization tool, not as a complete description of a real biological system.

## Installation

Clone the repository:

```bash
git clone <repository-link>
cd EnzymeInhibitorCompetitionSimulator
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Program

Run the main script:

```bash
python main.py
```

The program will ask the user to enter the required parameters.

Example:

```text
Enter K1 in nM: 10
Enter total E1 concentration in nM: 100
Enter total inhibitor concentration in nM: 80
Enter minimum E2 concentration in nM: 0
Enter maximum E2 concentration in nM: 500
Enter K2 values separated by commas: 5,10,50,100
Enter target activity percentage: 80
```

After running, the program will calculate the results and generate the output graph.

## Running Tests

Run:

```bash
pytest
```

The tests will check that:

- The calculated activity is between 0 and 100 percent
- Negative concentrations are not accepted
- The inhibitor mass balance is reasonable
- Multiple `K2` values can be processed
- Increasing `E2` affects the amount of inhibitor bound to `E1`

## Course Information

This project was developed as part of a Python programming course project:

https://github.com/Code-Maven/wis-python-course-2026-03

The project combines biochemical modeling and Python-based simulation to investigate how competition for an inhibitor can affect enzyme activity.
