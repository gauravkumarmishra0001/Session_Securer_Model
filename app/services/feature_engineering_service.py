from collections import Counter


ML_FEATURE_NAMES = [
    "historical_event_count",
    "ip_known",
    "device_known",
    "browser_known",
    "operating_system_known",
    "new_ip",
    "new_device",
    "new_browser",
    "new_operating_system",
    "unique_ip_count",
    "unique_device_count",
    "unique_browser_count",
    "unique_operating_system_count",
    "ip_diversity",
    "device_diversity",
    "browser_diversity",
    "operating_system_diversity",
    "current_ip_frequency",
    "current_device_frequency",
    "current_browser_frequency",
    "current_operating_system_frequency",
    "login_hour",
    "login_day_of_week",
    "seconds_since_last_event"
]


def _safe_divide(value, total):
    if total == 0:
        return 0.0

    return float(value) / float(total)


def build_feature_vector(session, historical_events):
    event_count = len(historical_events)

    ips = [
        event.ip_address
        for event in historical_events
        if event.ip_address
    ]

    devices = [
        event.device_type
        for event in historical_events
        if event.device_type
    ]

    browsers = [
        event.browser
        for event in historical_events
        if event.browser
    ]

    operating_systems = [
        event.operating_system
        for event in historical_events
        if event.operating_system
    ]

    ip_counts = Counter(ips)
    device_counts = Counter(devices)
    browser_counts = Counter(browsers)
    os_counts = Counter(operating_systems)

    current_ip = session.ip_address
    current_device = session.device_type
    current_browser = session.browser
    current_os = session.operating_system

    ip_known = int(current_ip in ip_counts)
    device_known = int(current_device in device_counts)
    browser_known = int(current_browser in browser_counts)
    operating_system_known = int(current_os in os_counts)

    new_ip = int(not ip_known)
    new_device = int(not device_known)
    new_browser = int(not browser_known)
    new_operating_system = int(
        not operating_system_known
    )

    unique_ip_count = len(set(ips))
    unique_device_count = len(set(devices))
    unique_browser_count = len(set(browsers))
    unique_operating_system_count = len(
        set(operating_systems)
    )

    login_time = session.created_at

    if login_time is not None:
        login_hour = login_time.hour
        login_day_of_week = login_time.weekday()
    else:
        login_hour = 0
        login_day_of_week = 0

    event_times = [
        event.created_at
        for event in historical_events
        if event.created_at is not None
    ]

    if login_time is not None and event_times:
        last_event_time = max(event_times)

        seconds_since_last_event = max(
            0.0,
            (
                login_time - last_event_time
            ).total_seconds()
        )
    else:
        seconds_since_last_event = 0.0

    features = {
        "historical_event_count": event_count,

        "ip_known": ip_known,
        "device_known": device_known,
        "browser_known": browser_known,
        "operating_system_known": operating_system_known,

        "new_ip": new_ip,
        "new_device": new_device,
        "new_browser": new_browser,
        "new_operating_system": new_operating_system,

        "unique_ip_count": unique_ip_count,
        "unique_device_count": unique_device_count,
        "unique_browser_count": unique_browser_count,
        "unique_operating_system_count":
            unique_operating_system_count,

        "ip_diversity": _safe_divide(
            unique_ip_count,
            event_count
        ),

        "device_diversity": _safe_divide(
            unique_device_count,
            event_count
        ),

        "browser_diversity": _safe_divide(
            unique_browser_count,
            event_count
        ),

        "operating_system_diversity": _safe_divide(
            unique_operating_system_count,
            event_count
        ),

        "current_ip_frequency": ip_counts.get(
            current_ip,
            0
        ),

        "current_device_frequency": device_counts.get(
            current_device,
            0
        ),

        "current_browser_frequency": browser_counts.get(
            current_browser,
            0
        ),

        "current_operating_system_frequency":
            os_counts.get(current_os, 0),

        "login_hour": login_hour,
        "login_day_of_week": login_day_of_week,

        "seconds_since_last_event":
            seconds_since_last_event
    }

    return features
