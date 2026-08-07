def diagnose(status, sensor_data):
    issues = []

    temp = status["temp"]
    pressure = status["pressure"]
    voltage = status["voltage"]
    rpm = status["rpm"]

    missing_sensors = [
    name
    for name, value in status.items()
    if value == "INVALID"
    ]

    # Example rules

    if temp == "HIGH" and pressure == "LOW":
        issues.append("Possible head gasket failure")

    if voltage == "LOW" and rpm != "LOW":
        issues.append("Alternator not charging")

    if temp == "HIGH" and pressure == "NORMAL":
        issues.append("Cooling system issue")

    if pressure == "LOW" and rpm == "HIGH":
        issues.append("Oil starvation under load")
    
    if missing_sensors:
        issues.append(
            f"Sensor error: Not Reading ({', '.join(missing_sensors)})"
        )
    if not issues:
        issues.append("No faults detected")

    return issues