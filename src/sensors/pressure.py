import random
import time
from engine_state import EngineState

_current_pressure = 0.0  # Base pressure in PSI

def get_data(curr_time, eng_status, rpm, temp):
    global _current_pressure

    max_limit = 80
    ramp = 0.2
    noise = random.uniform(-0.5, 0.5)  # Simulate small pressure fluctuations

    if eng_status == EngineState.OFF:
        target_pressure = 0.0  # No pressure when engine is off
        ramp =  0.6
    
    else:
        target_pressure = 10 + (rpm * 0.01)
        
        if temp < 60:
            target_pressure *= 1.05

    target_pressure = min(target_pressure, max_limit)

    _current_pressure += (target_pressure-_current_pressure) * ramp + noise # Smooth transition to target pressure
    
    if _current_pressure < 0:
        _current_pressure = 0

    if abs(_current_pressure) < 0.5:
        _current_pressure = 0

    return {
        'timestamp': curr_time,
        'value': round(_current_pressure, 1)  # Round pressure to 1 decimal place
    }