def diagnose(status, sensor_data):
    issues = []

    temp = status["temp"]
    pressure = status["pressure"]
    voltage = status["voltage"]
    rpm = status["rpm"]

    # Example rules

    if temp == "HIGH" and pressure == "LOW":
        issues.append("Possible head gasket failure")

    if voltage == "LOW" and rpm != "LOW":
        issues.append("Alternator not charging")

    if temp == "HIGH" and pressure == "NORMAL":
        issues.append("Cooling system issue")

    if pressure == "LOW" and rpm == "HIGH":
        issues.append("Oil starvation under load")
    
    issues.append("test your chicken")
    

    return issues