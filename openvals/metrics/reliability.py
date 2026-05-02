def reliability(output):
    if not output:
        return 0.0
    
    if "ERROR" in str(output):
        return 0.0

    return 1.0