def classify_zone(distance):
    if distance < 0.5:
        return "DANGER"
    elif distance < 1.5:
        return "WARNING"
    else:
        return "SAFE"
