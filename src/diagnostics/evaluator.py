from diagnostics import thresholds

SENSOR_LIMITS = {
    "temp": (thresholds.TEMP_LOW, thresholds.TEMP_HIGH),
    "voltage": (thresholds.VOLT_LOW, thresholds.VOLT_HIGH),
    "rpm": (thresholds.RPM_LOW, thresholds.RPM_HIGH),
    "pressure": (thresholds.PRESS_LOW, thresholds.PRESS_HIGH),
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
    sensor_status = {}

    for name, value in sensor_data.items():
        sensor_status[name] = evaluate_sensor(name, value)

    return sensor_status