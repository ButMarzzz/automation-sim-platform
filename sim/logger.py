import csv

def init_logger(filename="engine_data.csv"):
    file = open(filename, mode="w", newline="")
    writer = csv.writer(file)

    # header
    writer.writerow(["time", "state", "rpm", "voltage", "temp","pressure"])

    return file, writer


def log_data(writer, curr_time, state, rpm, voltage, temp, pressure):
    writer.writerow([
        round(curr_time, 2),
        state.name,   # because using Enum
        int(rpm),
        round(voltage, 2),
        round(temp, 2),
        round(pressure,2)
    ])