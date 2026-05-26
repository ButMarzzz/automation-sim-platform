from diagnostics.thresholds import *

SENSOR_LIMITS = {
    "temp": (TEMP_LOW, TEMP_HIGH),
    "voltage": (VOLT_LOW, VOLT_HIGH),
    "rpm": (RPM_LOW, RPM_HIGH),
    "pressure": (PRESS_LOW, PRESS_HIGH),
}

def check_range(value, low, high):
    if value is None:
        return "INVALID"
    if value < low:
        return "LOW"
    elif value > high:
        return "HIGH"
    return "NORMAL"


def evaluate_sensor(name, value):
    low, high = SENSOR_LIMITS[name]
    return check_range(value, low, high)


def evaluate_all(sensor_data):
    status = {}

    for name, value in sensor_data.items():
        status[name] = evaluate_sensor(name, value)

    return status