
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_ml_feature_count():

    from app.services.feature_engineering_service import (
        ML_FEATURE_NAMES
    )

    assert len(ML_FEATURE_NAMES) == 24


def test_training_data_exists():

    assert (
        PROJECT_ROOT /
        "data" /
        "ml_training_data.csv"
    ).exists()


def test_model_exists():

    assert (
        PROJECT_ROOT /
        "models" /
        "isolation_forest.joblib"
    ).exists()


def test_isolation_forest_functions():

    from app.services.isolation_forest_service import (
        train_isolation_forest,
        load_isolation_forest,
        predict_isolation_forest
    )

    assert callable(train_isolation_forest)
    assert callable(load_isolation_forest)
    assert callable(predict_isolation_forest)


def test_risk_functions():

    from app.services.risk_service import (
        calculate_ml_risk,
        classify_ml_risk
    )

    metadata = {
        "score_p05": -0.10,
        "score_max": 0.20
    }

    risk = calculate_ml_risk(
        0.20,
        metadata
    )

    assert 0.0 <= risk <= 1.0
    assert classify_ml_risk(risk) == "NORMAL"


def test_detection_import():

    from app.services.detection_service import (
        analyze_session
    )

    assert callable(analyze_session)
