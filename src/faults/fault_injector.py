from faults.fault_types import FaultType
from engine_state import EngineState
import random

def update_faults(time, active_faults, engine_status):
    if random.random() < 0.80 and FaultType.OVERHEATING not in active_faults:
        active_faults[FaultType.OVERHEATING] = {
            "start_time": time,
            "endtime": time + 20.0
        }

    if random.random() < 0.30 and FaultType.LOW_OIL_PRESSURE not in active_faults:
        active_faults[FaultType.LOW_OIL_PRESSURE] = {
            "start_time": time,
            "endtime": time + 20.0
        }

    if random.random() < 0.20 and FaultType.VOLTAGE_DROP not in active_faults:
        active_faults[FaultType.VOLTAGE_DROP] = {
            "start_time": time,
            "endtime": time + 20.0
        }

    if random.random() < 0.25 and FaultType.RPM_DROP not in active_faults and engine_status != "EngineState.OFF":
        active_faults[FaultType.STALL] = {
            "start_time": time,
            "endtime": time + 20.0
        }
    
    for fault, info in list(active_faults.items()):
        if time > info["endtime"]:
            del active_faults[fault]



def apply_faults(sensor_data, faults):
    if FaultType.OVERHEATING in faults:
        sensor_data["temp"] += 30

    if FaultType.LOW_OIL_PRESSURE in faults:
        sensor_data["pressure"] -= 20
        sensor_data["pressure"] = max(0, sensor_data["pressure"])

    if FaultType.VOLTAGE_DROP in faults:
        sensor_data["voltage"] -= 2
        sensor_data["voltage"] = max(0, sensor_data["voltage"])

    if FaultType.RPM_DROP in faults:
        sensor_data["rpm"] -= 2000
        sensor_data["rpm"] = max(0, sensor_data["rpm"])

    if FaultType.TEMP_SENSOR_FAILURE in faults:
        sensor_data["temp"] = None
    
    if FaultType.RPM_SENSOR_FAILURE in faults:
        sensor_data["rpm"] = None
    
    if FaultType.VOLTAGE_SENSOR_FAILURE in faults:
        sensor_data["voltage"] = None

    if FaultType.PRESSURE_SENSOR_FAILURE in faults:
        sensor_data["pressure"] = None

    if FaultType.VOLTAGE_ZERO in faults:
        sensor_data["voltage"] = 0
    
    if FaultType.PRESSURE_ZERO in faults:
        sensor_data["pressure"] = 0
    
    if FaultType.RPM_ZERO in faults:
        sensor_data["rpm"] = 0
    
    if FaultType.TEMP_ZERO in faults:
        sensor_data["temp"] = 0

    return sensor_data