from asyncio.windows_events import NULL
import random
import time
from engine_state import EngineState

_current_temp = 20.0  # Base temperature in Celsius
AMBIENT_TEMP = 20.0
CRANK_TEMP = 30.0
OPERATING_TEMP = 90.0

OFF = 0.05
CRANKING = 0.1
RUNNING = 0.02
REVING = 0.05

_last_time = 0

def get_data(curr_time, eng_status):
    global _current_temp
    global _last_time
    
    noise = random.uniform(-0.1, 0.3)  # Simulate small temperature fluctuations

    if _last_time == 0:
        dt = 0
    else:
        dt = curr_time - _last_time

    _last_time = curr_time

    if eng_status == EngineState.OFF:
        target = AMBIENT_TEMP
        rate = OFF

    elif eng_status == EngineState.CRANKING:
        target = CRANK_TEMP
        rate = CRANKING

    elif eng_status in (EngineState.IDLE, EngineState.RUNNING):
        target = OPERATING_TEMP
        rate = RUNNING
    
    elif eng_status == EngineState.REV:
        target = OPERATING_TEMP + 10  # Revving causes extra heat
        rate = REVING

    _current_temp += (target - _current_temp) * rate * max(dt, 1)

    return {
        'timestamp': curr_time,
        'value': round(_current_temp + noise, 1)  # Round temperature to 1 decimal place
    }