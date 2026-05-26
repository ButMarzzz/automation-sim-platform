import random
import time
from engine_state import EngineState


_current_voltage = 12.6  # Base voltage for normal operation

def get_data(curr_time, eng_status, prev_status, time_in_state):
    global _current_voltage
    
    ramp = 0.1  # How quickly voltage approaches target (0.0 to 1.0) - higher is faster

    noise = random.uniform(-0.01, 0.05)  # Simulate small voltage fluctuations

    if eng_status == EngineState.OFF:
        if prev_status == EngineState.RUNNING and time_in_state < 0.5:
            _current_voltage += random.uniform(-1.1, -0.6)  # Voltage drops immediately when engine is turned off
            ramp = 0.7  # Faster ramp when transitioning from running to off
            target_voltage = 12.6  # Normal voltage when engine is off
        else:
            target_voltage = 12.6  # Normal voltage when engine is off
            ramp = 0.2  # Slow ramp when engine is off

    elif eng_status == EngineState.CRANKING:
        ramp = 0.8  # Faster ramp during cranking
        _current_voltage += random.uniform(-0.3, 0.8)  # Simulate voltage drop during cranking

        if prev_status == EngineState.OFF and time_in_state < 0.5:
            _current_voltage += random.uniform(-3.1, -1.6)  # Voltage drops immediately when cranking starts
            ramp = 0.8
            target_voltage = 10.5  # Initial voltage drop when cranking starts  
        elif time_in_state < 1.2:
            target_voltage = 10.0     # sustained crank
        else:
            target_voltage = 11.5     # engine catching
        
    elif eng_status in (EngineState.IDLE, EngineState.RUNNING):

        if prev_status == EngineState.CRANKING and time_in_state < 0.5:
            _current_voltage += random.uniform(1.4, 3.2) # Voltage recovers quickly after cranking
            ramp = 0.7  # Faster ramp when transitioning from cranking to running
            target_voltage = 14.3
        else:
            target_voltage = 14.3  # Higher voltage when engine is running
            ramp = 0.25  # Jumps quickly to target when running
    
    elif eng_status == EngineState.REV:
        target_voltage = 14.4  # Slightly higher voltage when revving
        ramp = 0.5  # Very fast ramp during revving
        

    _current_voltage += (target_voltage - _current_voltage) * ramp

    return {
        'timestamp': curr_time,
        'value': round(_current_voltage + noise, 2)  # Round voltage to 2 decimal places
    }