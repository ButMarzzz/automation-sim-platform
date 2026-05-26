TEMP_LOW = 15.0
TEMP_HIGH = 100.0

VOLT_LOW = 11.0
VOLT_HIGH = 15.0

RPM_LOW = 500
RPM_HIGH = 4000

PRESS_LOW = 20.0
PRESS_HIGH = 80.0

def check_range(value, low_limit, high_limit):
    if value < low_limit:
        return 'LOW'
    elif value > high_limit:
        return 'HIGH'
    else:
        return 'NORMAL'
    
def check_zero(value):
    if value == 0:
        return 'ZERO'
    else:
        return 'NON-ZERO'

def check_temp(temp_data):
    temp_value = temp_data['value']
    return check_range(temp_value, TEMP_LOW, TEMP_HIGH)

def check_voltage(voltage_data):
    voltage_value = voltage_data['value']
    return check_range(voltage_value, VOLT_LOW, VOLT_HIGH)

def check_rpm(rpm_data):
    rpm_value = rpm_data['value']
    return check_range(rpm_value, RPM_LOW, RPM_HIGH)

def check_pressure(pressure_data):
    pressure_value = pressure_data['value']
    return check_range(pressure_value, PRESS_LOW, PRESS_HIGH)

def print_status(sensor, status, message=None):
    if status == 'LOW':
        print(f"{sensor} is too low!" + (message if message else ""))
    elif status == 'HIGH':
        print(f"{sensor} is too high!" + (message if message else ""))
    else:
        print(f"{sensor} is normal.")

def print_temp(status):
    message = ""
    if status == 'LOW':
        message = " Possible cooling system issue."
    elif status == 'HIGH':
        message = " Possible overheating."

    print_status("Temperature", status, message)

def print_voltage(status):
    message = ""
    if status == 'LOW':
        message = " Possible battery or alternator issue."
    elif status == 'HIGH':
        message = " Possible overvoltage."

    print_status("Voltage", status, message)

def print_rpm(status):
    message = ""
    if status == 'LOW':
        message = " Possible mechanical issue."
    elif status == 'HIGH':
        message = " Possible overspeed."

    print_status("RPM", status, message)

def print_pressure(status):
    message = ""
    if status == 'LOW':
        message = " Possible low pressure issue."
    elif status == 'HIGH':
        message = " Possible high pressure issue."
        
    print_status("Pressure", status, message)