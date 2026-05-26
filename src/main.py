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
    eng_status = EngineState.OFF
    time_in_state = 0
    previous_status = eng_status
    just_started = False

    print("Starting simulation...")
    
    while True:
        curr_time = time.time() - init_time

        eng_status = update_engine_state(time_in_state, eng_status, curr_time)


        if eng_status != previous_status:
            time_in_state = 0

            just_started = (
            previous_status == EngineState.CRANKING and eng_status != EngineState.OFF
            )

            print(f"\n--- Engine status changed to: {eng_status} ---\n")

        if just_started == True and time_in_state >= 0.5:
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
        faults = update_faults(curr_time)
        sensor_data = apply_faults(sensor_data, faults)

        # 3. Evaluate status
        status = evaluate_all(sensor_data)

        # 4. Diagnose
        issues = diagnose(status, sensor_data)

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
        temp_checked = fault_check.check_temp(temp_data)
        rpm_checked  = fault_check.check_rpm(rpm_data)
        voltage_checked = fault_check.check_voltage(voltage_data)
        pressure_checked = fault_check.check_pressure(pressure_data)

        # 3. print results
        fault_check.print_temp(temp_checked)
        fault_check.print_rpm(rpm_checked)
        fault_check.print_voltage(voltage_checked)
        fault_check.print_pressure(pressure_checked)
 
        previous_status = eng_status
        time_in_state += 0.50  # Increment time_in_state by 0.5 seconds (the sleep interval)
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
