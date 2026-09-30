
import numpy as np


def calculate_ml_risk(
    decision_score,
    metadata
):
    normal_floor = metadata["score_p05"]
    normal_ceiling = metadata["score_max"]

    denominator = (
        normal_ceiling -
        normal_floor
    )

    if denominator <= 0:
        risk = 0.0
    else:
        risk = (
            normal_ceiling -
            decision_score
        ) / denominator

    risk = float(
        np.clip(
            risk,
            0.0,
            1.0
        )
    )

    return round(risk, 4)


def classify_ml_risk(risk_score):

    if risk_score < 0.40:
        return "NORMAL"

    if risk_score < 0.70:
        return "UNUSUAL"

    return "HIGH_RISK"
