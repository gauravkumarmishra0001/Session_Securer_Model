
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    Response
)

from app.services.session_service import (
    get_session_from_token
)

from app.services.dashboard_service import (
    get_dashboard_data
)


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


def current_session():
    token = request.cookies.get(
        current_app.config[
            "SESSION_COOKIE_NAME"
        ]
    )

    if not token:
        return None

    return get_session_from_token(token)


@dashboard_bp.route(
    "/api/dashboard/summary",
    methods=["GET"]
)
def summary():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    return jsonify(
        get_dashboard_data(
            session.user_id
        )
    ), 200


@dashboard_bp.route(
    "/api/dashboard/active-sessions",
    methods=["GET"]
)
def active_sessions():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "sessions":
            data["active_sessions"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/login-history",
    methods=["GET"]
)
def login_history():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "history":
            data["login_history"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/risk-scores",
    methods=["GET"]
)
def risk_scores():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "risk_scores":
            data["risk_scores"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/blocked-attempts",
    methods=["GET"]
)
def blocked_attempts():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "blocked_attempts":
            data["blocked_attempts"]
    }), 200


@dashboard_bp.route(
    "/api/dashboard/security-alerts",
    methods=["GET"]
)
def security_alerts():

    session = current_session()

    if session is None:
        return jsonify({
            "error":
                "authentication required"
        }), 401

    data = get_dashboard_data(
        session.user_id
    )

    return jsonify({
        "alerts":
            data["security_alerts"]
    }), 200


@dashboard_bp.route(
    "/dashboard",
    methods=["GET"]
)
def dashboard_page():

    session = current_session()

    if session is None:
        return Response(
            "<h2>Authentication required</h2>"
            "<p>Please login first.</p>",
            status=401,
            mimetype="text/html"
        )

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Session Securer Dashboard</title>

<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background: #f4f6f8;
    color: #222;
}

header {
    background: #111827;
    color: white;
    padding: 22px;
}

header h1 {
    margin: 0;
}

.container {
    padding: 25px;
    max-width: 1400px;
    margin: auto;
}

.cards {
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow:
        0 2px 8px rgba(0,0,0,0.08);
}

.card h3 {
    margin-top: 0;
}

.number {
    font-size: 30px;
    font-weight: bold;
}

.section {
    background: white;
    margin-bottom: 25px;
    padding: 20px;
    border-radius: 10px;
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
    white-space: nowrap;
}

th {
    background: #f1f5f9;
}

</style>
</head>

<body>

<header>
<h1>Session Securer Security Dashboard</h1>
<p>Authentication and session security monitoring</p>
</header>

<div class="container">

<div class="cards">

<div class="card">
<h3>Active Sessions</h3>
<div id="activeCount" class="number">-</div>
</div>

<div class="card">
<h3>Login History</h3>
<div id="loginCount" class="number">-</div>
</div>

<div class="card">
<h3>Risk Assessments</h3>
<div id="riskCount" class="number">-</div>
</div>

<div class="card">
<h3>Blocked Attempts</h3>
<div id="blockedCount" class="number">-</div>
</div>

<div class="card">
<h3>Security Alerts</h3>
<div id="alertCount" class="number">-</div>
</div>

</div>

<div class="section">
<h2>Active Sessions</h2>

<table>
<thead>
<tr>
<th>ID</th>
<th>IP</th>
<th>Location</th>
<th>Device</th>
<th>Browser</th>
<th>OS</th>
<th>Created</th>
<th>Last Seen</th>
</tr>
</thead>

<tbody id="sessionsTable"></tbody>
</table>
</div>


<div class="section">
<h2>Login History</h2>

<table>
<thead>
<tr>
<th>Time</th>
<th>Event</th>
<th>IP</th>
<th>Location</th>
<th>Device</th>
<th>Browser</th>
<th>OS</th>
</tr>
</thead>

<tbody id="historyTable"></tbody>
</table>
</div>


<div class="section">
<h2>Risk Scores</h2>

<table>
<thead>
<tr>
<th>Time</th>
<th>Risk Score</th>
<th>Classification</th>
<th>ML Classification</th>
<th>Action</th>
</tr>
</thead>

<tbody id="riskTable"></tbody>
</table>
</div>


<div class="section">
<h2>Blocked Attempts</h2>

<table>
<thead>
<tr>
<th>Time</th>
<th>Severity</th>
<th>Action</th>
<th>Message</th>
</tr>
</thead>

<tbody id="blockedTable"></tbody>
</table>
</div>


<div class="section">
<h2>Security Alerts</h2>

<table>
<thead>
<tr>
<th>Time</th>
<th>Severity</th>
<th>Title</th>
<th>Action</th>
<th>Message</th>
</tr>
</thead>

<tbody id="alertsTable"></tbody>
</table>
</div>

</div>


<script>

function safe(value) {
    if (value === null ||
        value === undefined) {
        return "-";
    }

    return value;
}


async function loadDashboard() {

    const response =
        await fetch(
            "/api/dashboard/summary"
        );

    if (!response.ok) {
        document.body.innerHTML =
            "<h2>Authentication required</h2>";
        return;
    }

    const data =
        await response.json();


    document.getElementById(
        "activeCount"
    ).textContent =
        data.counts.active_sessions;


    document.getElementById(
        "loginCount"
    ).textContent =
        data.counts.login_history;


    document.getElementById(
        "riskCount"
    ).textContent =
        data.counts.risk_scores;


    document.getElementById(
        "blockedCount"
    ).textContent =
        data.counts.blocked_attempts;


    document.getElementById(
        "alertCount"
    ).textContent =
        data.counts.security_alerts;


    document.getElementById(
        "sessionsTable"
    ).innerHTML =
        data.active_sessions.map(
            function(s) {
                return `
<tr>
<td>${safe(s.id)}</td>
<td>${safe(s.ip_address)}</td>
<td>${safe(s.location)}</td>
<td>${safe(s.device_type)}</td>
<td>${safe(s.browser)}</td>
<td>${safe(s.operating_system)}</td>
<td>${safe(s.created_at)}</td>
<td>${safe(s.last_seen_at)}</td>
</tr>`;
            }
        ).join("");


    document.getElementById(
        "historyTable"
    ).innerHTML =
        data.login_history.map(
            function(e) {
                return `
<tr>
<td>${safe(e.created_at)}</td>
<td>${safe(e.event_type)}</td>
<td>${safe(e.ip_address)}</td>
<td>${safe(e.location)}</td>
<td>${safe(e.device_type)}</td>
<td>${safe(e.browser)}</td>
<td>${safe(e.operating_system)}</td>
</tr>`;
            }
        ).join("");


    document.getElementById(
        "riskTable"
    ).innerHTML =
        data.risk_scores.map(
            function(r) {
                return `
<tr>
<td>${safe(r.created_at)}</td>
<td>${safe(r.risk_score)}</td>
<td>${safe(r.classification)}</td>
<td>${safe(r.ml_classification)}</td>
<td>${safe(r.action)}</td>
</tr>`;
            }
        ).join("");


    document.getElementById(
        "blockedTable"
    ).innerHTML =
        data.blocked_attempts.map(
            function(a) {
                return `
<tr>
<td>${safe(a.created_at)}</td>
<td>${safe(a.severity)}</td>
<td>${safe(a.action)}</td>
<td>${safe(a.message)}</td>
</tr>`;
            }
        ).join("");


    document.getElementById(
        "alertsTable"
    ).innerHTML =
        data.security_alerts.map(
            function(a) {
                return `
<tr>
<td>${safe(a.created_at)}</td>
<td>${safe(a.severity)}</td>
<td>${safe(a.title)}</td>
<td>${safe(a.action)}</td>
<td>${safe(a.message)}</td>
</tr>`;
            }
        ).join("");
}


loadDashboard();

</script>

</body>
</html>
"""

    return Response(
        html,
        status=200,
        mimetype="text/html"
    )
