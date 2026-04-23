import random
import time
from engine_state import EngineState


_current_rpm = 0

def get_data(curr_time, eng_status, just_started):

    global _current_rpm

    ramp = 0.2  # How quickly RPM approaches target (0.0 to 1.0) - higher is faster

    # target RPM depending on engine state
    if eng_status == EngineState.OFF:
        _current_rpm = 0
        target = 0

    elif eng_status == EngineState.CRANKING:
        target = random.uniform(250, 400)

    elif eng_status == EngineState.IDLE:
        target = random.uniform(700, 900)

    elif eng_status == EngineState.RUNNING:
        target = random.uniform(1800, 3200)

    elif eng_status == EngineState.REV:
        target = random.uniform(4000, 6000)
        ramp = 0.5  # Revving is more aggressive, so we use a faster ramp

    else:
        target = 0

    if just_started:
        _current_rpm += random.uniform(300, 600)

    # smooth ramp (no instant jump)
    _current_rpm += (target - _current_rpm) * ramp

    # small vibration noise
    _current_rpm += random.uniform(-20, 20)

    if _current_rpm < 0:
        _current_rpm = 0

    return {
        'timestamp': curr_time,
        'value': _current_rpm 
    }