# Automotive Engine Simulation & Telemetry Platform

## Overview

This project is an automotive engine simulation that models an engine moving through different states of operation. During the simulation, it generates and records telemetry data representing key engine parameters and simulated faults. Python and Pandas are then used to analyze the generated data and extract useful metrics and diagnostic information. An interactive Streamlit dashboard is used to visualize the telemetry, engine states, faults, and analysis results.

## Features

* Simulates an automotive engine through multiple operating states and generates telemetry data.
* Records engine parameters including RPM, temperature, voltage, and oil pressure.
* Simulates and tracks engine faults and fault occurrences.
* Uses Pandas to analyze engine states, fault frequency, durations, and sensor behavior.
* Provides an interactive Streamlit dashboard for exploring telemetry data.
* Includes interactive sensor, state, fault, and time-range filtering.
* Visualizes engine states, sensor data, fault frequency, and fault timelines.

## Technologies

* Python
* Pandas
* Streamlit
* Plotly
* Matplotlib
* Git / GitHub

## Project Structure

├───dashboard → contains the presentation/interface for generated analysis data
│       app.py
│
├───logs → contains generated telemetry data (sensor data, engine states, faults)
│       engine_data.csv
│
├───outputs → contains visualization output (charts and graphs)
│   └───graphs
│           graph.png
│
├───scripts → contains scripts for analysis/processing data and plots
│       analyze_data.py
│       plot_results.py
│
├───src → contains core application/simulation logic that runs the sim (fault rules, sensor logic, logging)
│   │   engine_state.py
│   │   main.py
│   ├───diagnostics
│   │   │   evaluator.py
│   │   │   rules.py
│   │   │   thresholds.py
├───faults
│   │   │   fault_check.py
│   │   │   fault_injector.py
│   │   │   fault_types.py
├───sensors
│   │   │   pressure.py
│   │   │   RPM.py
│   │   │   temp.py
│   │   │   voltage.py
  ├───utils
│   │   │   logger.py

## Dashboard

* Overview
In the overview section you will be shown basic information about each state. Amount of passes, average values, max and mins. Allowing the user to see statistical averages and how the data changes over time.
* Engine State Analysis
Shows duration of each state, which state lasted the longest, how many state changes, etc It allows the user to understand how the engine's operating time was distributed across states.
* Fault Analysis
Shows count of each issue, most common issue, fault frequency chart, a fault timeline. Then a dropdown of fault avg values compared to normal avg values. This section can be used to see how common issues were, the values that changed and cause these issues.
* Interactive Analysis
In this portion you can select a sensor for a sensor vs time chart. You can choose a fault to see metrics on average values and a full timeline for the fault. You will also get a timeline for the selected state. Then you also have a time-range filter for the state selected for RPM. This allows the issue to pick and choose data for specificied moments and faults.

## Data Analysis

* Summarizes sensor data using averages, minimums, and maximums.
* Filters fault-related data and tracks when issues occur.
* Filters unusually high or extreme sensor values to identify potentially abnormal conditions.
* Detects engine state changes and calculates the duration of individual states.
* Uses time-based analysis to determine when significant events occur, such as high RPM or cooling system issues.
* Groups telemetry data by engine state to compare sensor behavior across different operating conditions.

## How to Run

How to Run

1. Install Dependencies

Make sure Python is installed, then install the project's required packages:

pip install -r requirements.txt

2. Run the Engine Simulation

From the project root directory:

python src/main.py

This generates the engine telemetry data used by the analysis and dashboard.

3. Run the Data Analysis
python scripts/analyze_data.py

This analyzes the generated telemetry data and outputs statistical and diagnostic information.

4. Launch the Dashboard
streamlit run dashboard/app.py

This launches the interactive Streamlit dashboard in your browser.

## Example Insights

Analysis of the simulated telemetry produced several notable observations:

* More than 50% of recorded telemetry contained a simulated fault condition.
* Cooling system issues were the most frequently recorded fault.
REV was the longest-lasting engine operating state.
* Cooling system issues were frequently associated with longer REV periods, providing an example of how telemetry can be used to identify relationships between engine states and fault conditions.

## Future Improvements

* Expand the engine simulation to model more realistic engine behavior and operating conditions.
* Add additional sensors and fault types to increase the variety and complexity of the simulated telemetry.
* Implement automated testing for simulation logic, sensor behavior, fault detection, and data processing.