from flask import Blueprint, jsonify

from app.services.social_simulation_service import (
    get_recent_events,
    simulate_high_risk_login,
    simulate_new_device,
    simulate_normal_login,
)


social_bp = Blueprint(
    "social",
    __name__,
    url_prefix="/api/social"
)


@social_bp.get("/events")
def events():

    return jsonify({
        "events": get_recent_events()
    }), 200


@social_bp.post("/simulate/normal")
def simulate_normal():

    event = simulate_normal_login()

    if event is None:

        return jsonify({
            "error": "No demo user available"
        }), 503

    return jsonify(
        event.to_dict()
    ), 201


@social_bp.post("/simulate/new-device")
def simulate_new_device_route():

    event = simulate_new_device()

    if event is None:

        return jsonify({
            "error": "No demo user available"
        }), 503

    return jsonify(
        event.to_dict()
    ), 201


@social_bp.post("/simulate/high-risk")
def simulate_high_risk():

    event = simulate_high_risk_login()

    if event is None:

        return jsonify({
            "error": "No demo user available"
        }), 503

    return jsonify(
        event.to_dict()
    ), 201
