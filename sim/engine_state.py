from enum import Enum

class EngineState(Enum):
    OFF = 0
    CRANKING = 1
    IDLE = 2
    RUNNING = 3
    REV = 4