from flask import Blueprint, Response


web_bp = Blueprint(
    "web",
    __name__
)


HOME_PAGE = r"""
<!doctype html>
<html lang="en">

<head>

<meta charset="utf-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>Session Securer</title>

<style>

body {
    margin: 0;
    background: #0b1014;
    color: #e5edf1;
    font-family: Arial, Helvetica, sans-serif;
}

header {
    border-bottom: 1px solid #26343d;
    background: #0d1419;
}

nav {
    max-width: 1100px;
    margin: auto;
    padding: 20px 24px;

    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-weight: bold;
    letter-spacing: .12em;
}

.links {
    display: flex;
    gap: 20px;
}

a {
    color: #55c7d9;
    text-decoration: none;
}

main {
    max-width: 1100px;
    margin: auto;
    padding: 80px 24px;
}

.eyebrow {
    color: #55c7d9;
    font-size: 13px;
    letter-spacing: .15em;
    text-transform: uppercase;
}

h1 {
    font-size: 64px;
    line-height: 1;
    max-width: 850px;
}

p {
    color: #8b9aa4;
    line-height: 1.7;
    max-width: 760px;
}

.actions {
    margin-top: 30px;
}

button {
    background: #131c22;
    color: #e5edf1;
    border: 1px solid #26343d;
    padding: 13px 18px;
    margin-right: 8px;
    cursor: pointer;
}

button:hover {
    border-color: #55c7d9;
    color: #55c7d9;
}

.panel {
    margin-top: 70px;
    border: 1px solid #26343d;
    background: #11181e;
    padding: 28px;
}

footer {
    border-top: 1px solid #26343d;
    padding: 30px 24px;
    color: #8b9aa4;
}

footer div {
    max-width: 1100px;
    margin: auto;
}

</style>

</head>

<body>

<header>

<nav>

<div class="logo">
SESSION SECURER
</div>

<div class="links">

<a href="/">
Home
</a>

<a href="/social">
Social Lab
</a>

<a href="/dashboard">
Dashboard
</a>

</div>

</nav>

</header>


<main>

<div class="eyebrow">
Defensive Authentication Platform
</div>

<h1>
Session security with detection and response.
</h1>

<p>
Session Securer combines authentication, session telemetry,
behavior analysis, risk scoring and prevention controls
into one defensive security platform.
</p>

<div class="actions">

<a href="/social">
<button>
Open Social Security Lab
</button>
</a>

<a href="/dashboard">
<button>
Open Security Dashboard
</button>
</a>

</div>


<div class="panel">

<h2>
Security Pipeline
</h2>

<p>
Authentication → Session Events → Detection →
Risk Analysis → Prevention → Monitoring
</p>

<p>
Phase 6 provides a controlled simulated social platform
for security testing without requiring private telemetry
from external social networks.
</p>

</div>

</main>


<footer>

<div>

<a href="/terms">
Terms of Service
</a>

&nbsp; | &nbsp;

<a href="/privacy">
Privacy Policy
</a>

<p>
This project uses defense-in-depth security principles.
No software system can honestly guarantee absolute security.
</p>

</div>

</footer>

</body>

</html>
"""


SOCIAL_PAGE = r"""
<!doctype html>

<html lang="en">

<head>

<meta charset="utf-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>Social Security Lab</title>

<style>

body {
    margin: 0;
    background: #0b1014;
    color: #e5edf1;
    font-family: Arial, Helvetica, sans-serif;
}

main {
    max-width: 1050px;
    margin: auto;
    padding: 50px 24px;
}

a {
    color: #55c7d9;
    text-decoration: none;
}

.panel {
    border: 1px solid #26343d;
    background: #11181e;
    padding: 25px;
    margin-top: 25px;
}

button {
    background: #151e25;
    color: #e5edf1;
    border: 1px solid #26343d;
    padding: 13px 18px;
    margin: 5px;
    cursor: pointer;
}

button:hover {
    border-color: #55c7d9;
    color: #55c7d9;
}

.event {
    border-top: 1px solid #26343d;
    padding: 18px 0;
}

.normal {
    color: #75c99b;
}

.unusual {
    color: #d6bd6d;
}

.highrisk {
    color: #df7777;
}

#loading {
    display: none;
    color: #8b9aa4;
}

</style>

</head>


<body>

<main>

<a href="/">
← Home
</a>

<h1>
Social Security Lab
</h1>

<p>
Run controlled security scenarios and observe the resulting
security telemetry.
</p>


<div class="panel">

<h2>
Security Scenarios
</h2>

<button onclick="runScenario('/api/social/simulate/normal')">
Normal Login
</button>

<button onclick="runScenario('/api/social/simulate/new-device')">
New Device
</button>

<button onclick="runScenario('/api/social/simulate/high-risk')">
High Risk
</button>

</div>


<div class="panel">

<h2>
Security Events
</h2>

<div id="loading">
Loading security telemetry...
</div>

<div id="events">
</div>

</div>

</main>


<script>

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


async function runScenario(endpoint) {

    document.getElementById(
        "loading"
    ).style.display = "block";

    try {

        const response = await fetch(
            endpoint,
            {
                method: "POST"
            }
        );

        await response.json();

        await loadEvents();

    } catch (error) {

        document.getElementById(
            "events"
        ).innerHTML =
            "<p>Unable to execute scenario.</p>";
    }

    document.getElementById(
        "loading"
    ).style.display = "none";
}


async function loadEvents() {

    const box =
        document.getElementById("events");

    box.innerHTML =
        "<div class='event'>Loading...</div>";

    try {

        const response =
            await fetch(
                "/api/social/events"
            );

        const data =
            await response.json();

        if (
            !data.events ||
            data.events.length === 0
        ) {

            box.innerHTML =
                "<p>No events recorded yet.</p>";

            return;
        }


        box.innerHTML =
            data.events.map(
                function(event) {

                    let classification =
                        String(
                            event.classification || ""
                        );

                    let className =
                        classification === "NORMAL"
                        ? "normal"
                        : classification === "UNUSUAL"
                        ? "unusual"
                        : "highrisk";

                    let score =
                        event.risk_score === null
                        ? "N/A"
                        : Number(
                            event.risk_score
                          ).toFixed(2);

                    return `
                        <div class="event">

                            <strong>
                                ${escapeHtml(
                                    event.event_type
                                )}
                            </strong>

                            <p>
                                Classification:
                                <span class="${className}">
                                    ${escapeHtml(
                                        classification
                                    )}
                                </span>
                            </p>

                            <p>
                                Risk Score: ${score}
                            </p>

                            <p>
                                Action:
                                ${escapeHtml(
                                    event.action
                                )}
                            </p>

                            <p>
                                Device:
                                ${escapeHtml(
                                    event.device_type ||
                                    "Unknown"
                                )}
                            </p>

                            <p>
                                Location:
                                ${escapeHtml(
                                    event.location ||
                                    "Unknown"
                                )}
                            </p>

                        </div>
                    `;
                }
            ).join("");

    } catch (error) {

        box.innerHTML =
            "<p>Unable to load events.</p>";
    }
}


loadEvents();

</script>

</body>

</html>
"""


TERMS_PAGE = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Terms of Service</title>

<style>

body {
    background:#0b1014;
    color:#e5edf1;
    font-family:Arial,Helvetica,sans-serif;
    max-width:900px;
    margin:auto;
    padding:50px 24px;
    line-height:1.7;
}

a {
    color:#55c7d9;
}

</style>

</head>

<body>

<a href="/">
← Home
</a>

<h1>
Terms of Service
</h1>

<h2>
Authorized Use
</h2>

<p>
Session Securer is a defensive security research and
demonstration platform. Users must only test systems,
accounts and infrastructure that they own or are
authorized to assess.
</p>

<h2>
Security
</h2>

<p>
The project uses defense-in-depth controls. No software
system can guarantee absolute protection against every
possible vulnerability or attack.
</p>

</body>
</html>
"""


PRIVACY_PAGE = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Privacy Policy</title>

<style>

body {
    background:#0b1014;
    color:#e5edf1;
    font-family:Arial,Helvetica,sans-serif;
    max-width:900px;
    margin:auto;
    padding:50px 24px;
    line-height:1.7;
}

a {
    color:#55c7d9;
}

</style>

</head>

<body>

<a href="/">
← Home
</a>

<h1>
Privacy Policy
</h1>

<h2>
Security Telemetry
</h2>

<p>
The application may record authentication and security
telemetry such as device information, browser information,
operating system, IP address, location labels, risk scores
and security decisions.
</p>

<h2>
Purpose
</h2>

<p>
Telemetry is used for authentication security, anomaly
detection, risk assessment, prevention and monitoring.
</p>

<h2>
Third-Party Platforms
</h2>

<p>
The Phase 6 social platform is a controlled simulation.
It does not claim access to private security telemetry
from external social networks.
</p>

</body>
</html>
"""


@web_bp.get("/")
def home():
    return Response(
        HOME_PAGE,
        mimetype="text/html"
    )


@web_bp.get("/social")
def social():
    return Response(
        SOCIAL_PAGE,
        mimetype="text/html"
    )


@web_bp.get("/terms")
def terms():
    return Response(
        TERMS_PAGE,
        mimetype="text/html"
    )


@web_bp.get("/privacy")
def privacy():
    return Response(
        PRIVACY_PAGE,
        mimetype="text/html"
    )
