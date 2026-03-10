import random
import time
from engine_state import EngineState


_current_voltage = 12.6  # Base voltage for normal operation

def get_data(init_time, curr_time, eng_status):
    global _current_voltage

    noise = random.uniform(-0.01, 0.05)  # Simulate small voltage fluctuations

    if eng_status == EngineState.OFF:
        target_voltage = 12.6  # Normal voltage when engine is off
        _current_voltage += (target_voltage - _current_voltage) * 0.3  # Smooth transition to target voltage

    elif eng_status == EngineState.CRANKING:
        target_voltage = 10.0  # Lower voltage when engine is cranking
        _current_voltage += (target_voltage - _current_voltage) * 0.5  # Smooth transition to target voltage
        
    else:
        target_voltage = 14.3  # Higher voltage when engine is running
        _current_voltage += (target_voltage-_current_voltage) * 0.2  # Smooth transition to target voltage

    return {
        'timestamp': curr_time,
        'voltage': round(_current_voltage + noise, 2)  # Round voltage to 2 decimal places
    }