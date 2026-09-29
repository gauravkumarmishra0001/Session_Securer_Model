from collections import Counter


def build_user_profile(events):
    """
    Build a behavioral profile from historical login events.
    """

    if not events:
        return {
            "total_events": 0,
            "known_ips": [],
            "known_devices": [],
            "known_browsers": [],
            "known_operating_systems": []
        }

    ips = Counter(
        event.ip_address
        for event in events
        if event.ip_address
    )

    devices = Counter(
        event.device_type
        for event in events
        if event.device_type
    )

    browsers = Counter(
        event.browser
        for event in events
        if event.browser
    )

    operating_systems = Counter(
        event.operating_system
        for event in events
        if event.operating_system
    )

    return {
        "total_events": len(events),
        "known_ips": list(ips.keys()),
        "known_devices": list(devices.keys()),
        "known_browsers": list(browsers.keys()),
        "known_operating_systems": list(
            operating_systems.keys()
        )
    }


def extract_session_features(session, profile):
    """
    Convert a session into behavioral features.
    """

    ip_known = (
        session.ip_address in profile["known_ips"]
    )

    device_known = (
        session.device_type in profile["known_devices"]
    )

    browser_known = (
        session.browser in profile["known_browsers"]
    )

    operating_system_known = (
        session.operating_system
        in profile["known_operating_systems"]
    )

    return {
        "ip_known": ip_known,
        "device_known": device_known,
        "browser_known": browser_known,
        "operating_system_known": operating_system_known,

        "new_ip": not ip_known,
        "new_device": not device_known,
        "new_browser": not browser_known,
        "new_operating_system": not operating_system_known
    }
