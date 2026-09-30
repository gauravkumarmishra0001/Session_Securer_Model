import numpy as np
import pandas as pd

from app.services.feature_engineering_service import (
    ML_FEATURE_NAMES
)


def generate_normal_training_data(
    samples=1000,
    random_state=42
):
    rng = np.random.default_rng(random_state)

    rows = []

    for _ in range(samples):

        historical_event_count = int(
            rng.integers(5, 100)
        )

        unique_ip_count = int(
            rng.integers(1, 4)
        )

        unique_device_count = int(
            rng.integers(1, 3)
        )

        unique_browser_count = int(
            rng.integers(1, 3)
        )

        unique_os_count = int(
            rng.integers(1, 3)
        )

        ip_known = 1
        device_known = 1
        browser_known = 1
        operating_system_known = 1

        new_ip = 0
        new_device = 0
        new_browser = 0
        new_operating_system = 0

        current_ip_frequency = int(
            rng.integers(
                1,
                max(
                    2,
                    historical_event_count // 2 + 1
                )
            )
        )

        current_device_frequency = int(
            rng.integers(
                1,
                historical_event_count + 1
            )
        )

        current_browser_frequency = int(
            rng.integers(
                1,
                historical_event_count + 1
            )
        )

        current_operating_system_frequency = int(
            rng.integers(
                1,
                historical_event_count + 1
            )
        )

        login_hour = int(
            rng.integers(7, 23)
        )

        login_day_of_week = int(
            rng.integers(0, 7)
        )

        seconds_since_last_event = float(
            rng.integers(
                60,
                604800
            )
        )

        row = {
            "historical_event_count":
                historical_event_count,

            "ip_known":
                ip_known,

            "device_known":
                device_known,

            "browser_known":
                browser_known,

            "operating_system_known":
                operating_system_known,

            "new_ip":
                new_ip,

            "new_device":
                new_device,

            "new_browser":
                new_browser,

            "new_operating_system":
                new_operating_system,

            "unique_ip_count":
                unique_ip_count,

            "unique_device_count":
                unique_device_count,

            "unique_browser_count":
                unique_browser_count,

            "unique_operating_system_count":
                unique_os_count,

            "ip_diversity":
                unique_ip_count /
                historical_event_count,

            "device_diversity":
                unique_device_count /
                historical_event_count,

            "browser_diversity":
                unique_browser_count /
                historical_event_count,

            "operating_system_diversity":
                unique_os_count /
                historical_event_count,

            "current_ip_frequency":
                current_ip_frequency,

            "current_device_frequency":
                current_device_frequency,

            "current_browser_frequency":
                current_browser_frequency,

            "current_operating_system_frequency":
                current_operating_system_frequency,

            "login_hour":
                login_hour,

            "login_day_of_week":
                login_day_of_week,

            "seconds_since_last_event":
                seconds_since_last_event
        }

        rows.append(row)

    return pd.DataFrame(
        rows,
        columns=ML_FEATURE_NAMES
    )
