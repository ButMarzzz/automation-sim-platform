from faults.fault_types import FaultType
import random

def update_faults(time):
    if 10 < time < 20:
        return [FaultType.OVERHEATING]
    if random.random() < 0.30:
        return [FaultType.LOW_OIL_PRESSURE]
    if random.random() < 0.20:
        return [FaultType.VOLTAGE_DROP]

    return []


def apply_faults(sensor_data, faults):
    if FaultType.OVERHEATING in faults:
        sensor_data["temp"] += 30

    if FaultType.LOW_OIL_PRESSURE in faults:
        sensor_data["pressure"] -= 20

    if FaultType.VOLTAGE_DROP in faults:
        sensor_data["voltage"] -= 2

    if FaultType.SENSOR_FAILURE in faults:
        sensor_data["temp"] = None

    if FaultType.VOLTAGE_ZERO in faults:
        sensor_data["voltage"] = 0

    return sensor_data