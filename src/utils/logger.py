import csv
import os
from pathlib import Path


def init_logger(filename="engine_data.csv"):
    
    BASE_DIR = Path(__file__).resolve().parent      # utils/
    SRC_DIR = BASE_DIR.parent                      # src/
    PROJECT_ROOT = SRC_DIR.parent                 # automation-sim-platform/

    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_DIR.mkdir(exist_ok=True)

    filepath = LOG_DIR / "engine_data.csv"

    file = open(filepath, mode="w", newline="")
    writer = csv.writer(file)

    writer.writerow(["time", "state", "rpm", "voltage", "temp", "pressure", "issues"])

    print("FILE:", __file__)
    print("BASE_DIR:", BASE_DIR)
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("LOG_DIR:", LOG_DIR)
    print("CWD:", os.getcwd())
    return file, writer


def log_data(writer, curr_time, state, sensor_data, issues):
    issues_str = " | ".join(issues) if issues else "None"

    temp = sensor_data["temp"]
    temp = round(temp, 2) if temp is not None else "FAIL"

    writer.writerow([
        round(curr_time, 2),
        state.name,
        int(sensor_data["rpm"]),
        round(sensor_data["voltage"], 2),
        round(sensor_data["temp"], 2),
        round(sensor_data["pressure"], 2),
        issues_str
    ])