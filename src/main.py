import time
from sensors import RPM as rpm_sensor
#from faults import fault_check
from sensors import temp
from sensors import voltage
from engine_state import EngineState
from faults import fault_check
from sensors import pressure
from utils import logger
from faults.fault_injector import update_faults, apply_faults
from diagnostics.evaluator import evaluate_all
from diagnostics.rules import diagnose

def main():

    log_file, writer = logger.init_logger()

    init_time = time.time()
    time_in_state_init = init_time
    time_in_state = 0

    faults = dict()

    eng_status = EngineState.OFF
    previous_status = eng_status
    just_started = False

    print("Starting simulation...")
    
    while True:
        curr_time = time.time() - init_time

        eng_status = update_engine_state(time_in_state, eng_status, curr_time)

        state_changed = eng_status != previous_status

        if state_changed:
            time_in_state_init = time.time()

            just_started = (
            previous_status == EngineState.CRANKING and eng_status != EngineState.OFF
            )

            print(f"\n--- Engine status changed to: {eng_status} ---\n")

        if just_started and time_in_state >= 0.5:
            just_started = False 


        if eng_status == EngineState.OFF and curr_time > 8:
            break
       
        # 1. read sensors
        voltage_data = voltage.get_data(curr_time, eng_status, previous_status, time_in_state)
        rpm_data  = rpm_sensor.get_data(curr_time, eng_status, just_started)
        temp_data = temp.get_data(curr_time, eng_status)
        pressure_data = pressure.get_data(curr_time, eng_status, rpm_data['value'], temp_data['value'])

        sensor_data = {
            "temp": temp_data["value"],
            "pressure": pressure_data["value"],
            "voltage": voltage_data["value"],
            "rpm": rpm_data["value"]
        }

        # 2. Inject faults
        update_faults(curr_time, faults)
        sensor_data = apply_faults(sensor_data, faults)

        # 3. Evaluate status
        status = evaluate_all(sensor_data)

        for sensor in status:
             print(sensor, ":" ,status[sensor])

        # 4. Diagnose
        issues = diagnose(status, sensor_data)

        simulation_state = {
            "engine_state": eng_status,
            "time_in_state": time_in_state,
            "sensors": sensor_data,
            "faults": faults,
            "issues": issues
        }
        # log data
        logger.log_data(
            writer,
            curr_time,
            eng_status,
            sensor_data,
            issues
        )
        print(issues)

        # 2. check faults
        # if eng_status != EngineState.OFF and just_started != True:
        #     temp_checked = fault_check.check_temp(sensor_data["temp"])
        #     rpm_checked  = fault_check.check_rpm(sensor_data["rpm"])
        #     voltage_checked = fault_check.check_voltage(sensor_data["voltage"])
        #     pressure_checked = fault_check.check_pressure(sensor_data["pressure"])

        #     # 3. print results
        #     fault_check.print_temp(temp_checked)
        #     fault_check.print_rpm(rpm_checked)
        #     fault_check.print_voltage(voltage_checked)
        #     fault_check.print_pressure(pressure_checked)
        
 
        previous_status = eng_status
        time_in_state = time.time() - time_in_state_init  # Increment time_in_state by 0.5 seconds (the sleep interval)
        print(time_in_state)

        print(curr_time)
        time.sleep(0.50)

    log_file.close()


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
