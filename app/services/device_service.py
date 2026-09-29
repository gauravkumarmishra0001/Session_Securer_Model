from user_agents import parse


def get_device_info(user_agent_string):
    if not user_agent_string:
        return {
            "device_type": "Unknown",
            "browser": "Unknown",
            "operating_system": "Unknown"
        }

    user_agent = parse(user_agent_string)

    if user_agent.is_mobile:
        device_type = "Mobile"
    elif user_agent.is_tablet:
        device_type = "Tablet"
    elif user_agent.is_pc:
        device_type = "Desktop"
    else:
        device_type = "Other"

    browser = (
        user_agent.browser.family
        or "Unknown"
    )

    operating_system = (
        user_agent.os.family
        or "Unknown"
    )

    return {
        "device_type": device_type,
        "browser": browser,
        "operating_system": operating_system
    }
