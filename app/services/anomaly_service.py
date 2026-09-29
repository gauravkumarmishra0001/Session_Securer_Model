def calculate_anomaly_score(features):
    """
    Calculate a simple explainable anomaly score.

    Maximum score = 1.0
    """

    score = 0.0

    if features.get("new_ip", False):
        score += 0.25

    if features.get("new_device", False):
        score += 0.30

    if features.get("new_browser", False):
        score += 0.15

    if features.get("new_operating_system", False):
        score += 0.30

    return round(min(score, 1.0), 2)


def classify_anomaly(score):
    """
    Convert anomaly score into a human-readable class.
    """

    if score < 0.30:
        return "NORMAL"

    if score < 0.60:
        return "UNUSUAL"

    return "HIGH_ANOMALY"
