import random
import time
from engine_state import EngineState

_current_pressure = 0.0  # Base pressure in PSI

def get_data(curr_time, eng_status, rpm, temp):
    global _current_pressure

    noise = random.uniform(-0.5, 0.5)  # Simulate small pressure fluctuations

    if eng_status == EngineState.OFF:
        target_pressure = 0.0  # No pressure when engine is off

    if _current_pressure < 0:
        _current_pressure = 0
    
    target_pressure = 10 + (rpm * 0.01)

    _current_pressure += (target_pressure-_current_pressure) * 0.2  # Smooth transition to target pressure

    if temp < 60:
        _current_pressure += 10

    return {
        'timestamp': curr_time,
        'value': round(_current_pressure + noise, 1)  # Round pressure to 1 decimal place
    }