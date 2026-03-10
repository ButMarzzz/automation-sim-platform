import time
from sensors import RPM as rpm_sensor
#from faults import fault_check
from sensors import temp
from sensors import voltage
from engine_state import EngineState


def main():
    
    init_time = time.time()
    eng_status = EngineState.OFF
    time_in_state = 0
    previous_status = eng_status
    just_started = False

    print("Starting simulation...")
    
    while True:
        curr_time = time.time() - init_time
        
        eng_status = update_engine_state(time_in_state, eng_status, curr_time)

        
        if eng_status != previous_status:
            just_started = (
            previous_status == EngineState.CRANKING and eng_status != EngineState.OFF and time_in_state < 1.0
            )

            print(f"\n--- Engine status changed to: {eng_status} ---\n")
            previous_status = eng_status 
            time_in_state = 0

        if eng_status == EngineState.OFF and curr_time > 8:
            break
        
        time_in_state += 0.5  # Increment time_in_state by 0.5 seconds (the sleep interval)
        
        # 1. read sensors
        #temp_data = temp.get_data(init_time, curr_time, eng_status)
        voltage_data = voltage.get_data(init_time, curr_time, eng_status)
        rpm_data  = rpm_sensor.get_data(init_time, curr_time, eng_status, just_started)
        
        # 2. check faults
        '''temp_checked = fault_check.check_temp(temp_data)
        rpm_checked  = fault_check.check_rpm(rpm_data)
        voltage_checked = fault_check.check_voltage(voltage_data)

        # 3. print results
        fault_check.print_temp(temp_checked)
        fault_check.print_rpm(rpm_checked)
        fault_check.print_voltage(voltage_checked)'''

        time.sleep(0.5)


def update_engine_state(time_in_state, current_state, total_time):
    # determine next engine state based on elapsed time and current state
    new_state = current_state
    if time_in_state > 5 and current_state == EngineState.OFF:
        new_state = EngineState.CRANKING
    elif time_in_state > 2 and current_state == EngineState.CRANKING:
        new_state = EngineState.IDLE
    elif time_in_state > 9 and current_state == EngineState.IDLE and total_time < 20:
        new_state = EngineState.RUNNING
    elif time_in_state > 10 and current_state == EngineState.RUNNING:
        new_state = EngineState.REV
    elif time_in_state > 20 and current_state == EngineState.REV:
        new_state = EngineState.RUNNING
    elif time_in_state > 9 and current_state == EngineState.RUNNING and total_time > 40:
        new_state = EngineState.IDLE
    elif time_in_state > 10 and current_state == EngineState.IDLE :
        new_state = EngineState.OFF

    return new_state

if __name__ == "__main__":
    main()
