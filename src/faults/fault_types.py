from enum import Enum

class FaultType(Enum):
    NONE = 0
    OVERHEATING = 1
    LOW_OIL_PRESSURE = 2
    VOLTAGE_DROP = 3
    TEMP_SENSOR_FAILURE = 4
    VOLTAGE_ZERO = 5
    TEMP_ZERO = 6
    PRESSURE_ZERO = 7
    RPM_ZERO = 8