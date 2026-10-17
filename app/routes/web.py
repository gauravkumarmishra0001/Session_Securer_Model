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

<a href="/login">
Login
</a>

<a href="/register">
Register
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




AUTH_PAGE_STYLE = """
<style>
:root { color-scheme: dark; }
* { box-sizing: border-box; }
body {
  margin: 0; background: #0b1014; color: #e5edf1;
  font-family: Arial, Helvetica, sans-serif;
}
header { border-bottom: 1px solid #26343d; background: #0d1419; }
nav {
  max-width: 1000px; margin: auto; padding: 20px 24px;
  display: flex; justify-content: space-between; gap: 18px;
  flex-wrap: wrap;
}
a { color: #55c7d9; text-decoration: none; }
main {
  width: min(460px, calc(100% - 32px));
  margin: 64px auto; padding: 28px;
  background: #11181e; border: 1px solid #26343d;
}
h1 { margin-top: 0; }
p, .muted { color: #a3b1b9; line-height: 1.6; }
label { display: block; margin: 18px 0 7px; }
input {
  width: 100%; padding: 12px; color: #e5edf1;
  background: #0b1014; border: 1px solid #34444e;
}
button {
  margin-top: 22px; width: 100%; padding: 13px;
  background: #131c22; color: #e5edf1;
  border: 1px solid #55c7d9; cursor: pointer;
}
button:disabled { opacity: .6; cursor: wait; }
#status { overflow-wrap: anywhere; }
</style>
"""


def _auth_page(title, intro, fields, endpoint, mode):
    field_markup = []
    for name, label, input_type, autocomplete in fields:
        field_markup.append(
            '<label for="' + name + '">' + label + '</label>'
            '<input id="' + name + '" name="' + name + '" type="' +
            input_type + '" autocomplete="' + autocomplete +
            '" required' +
            (' minlength="8"' if name == 'password' and mode == 'register' else '') +
            '>'
        )

    alternate = (
        '<p class="muted">Already registered? <a href="/login">Log in</a></p>'
        if mode == "register"
        else '<p class="muted">Need an account? <a href="/register">Register</a></p>'
    )

    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>""" + title + """ | Session Securer</title>
""" + AUTH_PAGE_STYLE + """
</head>
<body>
<header><nav>
<strong>SESSION SECURER</strong>
<div>
<a href="/">Home</a> &nbsp;·&nbsp;
<a href="/security-center">Security Center</a>
</div>
</nav></header>
<main>
<h1>""" + title + """</h1>
<p>""" + intro + """</p>
<form id="auth-form">
""" + "\n".join(field_markup) + """
<button id="submit-button" type="submit">""" + title + """</button>
</form>
<p id="status" role="status" aria-live="polite"></p>
""" + alternate + """
</main>
<script>
(function () {
  const form = document.getElementById("auth-form");
  const status = document.getElementById("status");
  const button = document.getElementById("submit-button");

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    status.textContent = "";
    button.disabled = true;

    const payload = {};
    for (const field of form.elements) {
      if (field.name) payload[field.name] = field.value;
    }

    try {
      const response = await fetch("""" + endpoint + """", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const result = await response.json().catch(function () { return {}; });

      if (response.status === 202) {
        status.textContent =
          "Additional verification is required. This page does not complete OTP verification. " +
          "Your account has not been reported as fully signed in.";
      } else if (!response.ok) {
        status.textContent = result.error || "Request failed. Please try again.";
      } else if (response.ok && response.status === 201) {
        status.textContent = "Registration successful. Redirecting to login...";
        window.location.assign("/login");
      } else if (response.ok && result.message === "login successful") {
        status.textContent = "Login successful. Opening dashboard...";
        window.location.assign("/dashboard");
      } else {
        status.textContent = result.message || "Request completed.";
      }
    } catch (_) {
      status.textContent = "Could not contact the server. Please try again.";
    } finally {
      button.disabled = false;
    }
  });
})();
</script>
</body>
</html>"""
    return Response(page, mimetype="text/html")


@web_bp.get("/login")
def phase721_login_page():
    return _auth_page(
        "Login",
        "Sign in through Session Securer's existing authentication and risk checks.",
        [
            ("email", "Email address", "email", "username"),
            ("password", "Password", "password", "current-password"),
        ],
        "/api/auth/login",
        "login",
    )


@web_bp.get("/register")
def phase721_register_page():
    return _auth_page(
        "Register",
        "Create an account. Passwords must contain at least eight characters.",
        [
            ("username", "Username", "text", "username"),
            ("email", "Email address", "email", "email"),
            ("password", "Password", "password", "new-password"),
        ],
        "/api/auth/register",
        "register",
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


@web_bp.get("/security-overview")
def security_overview_718():
    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Security Overview | Session Securer</title>
<style>
body{margin:0;background:#101715;color:#e8f0ec;font:16px/1.6 system-ui,sans-serif}
header,main,footer{width:min(960px,calc(100% - 32px));margin:auto}
header{padding:22px 0;border-bottom:1px solid #40544a}
nav{display:flex;flex-wrap:wrap;gap:14px;margin-top:12px}
a{color:#80d9b2}
main{padding:28px 0}
.panel{background:#17221e;border:1px solid #40544a;padding:18px;margin:16px 0;overflow-wrap:anywhere}
.muted{color:#a7b7af}
.skeleton{height:14px;background:#2a3932;max-width:520px;margin:12px 0}
button{padding:10px 14px;background:#203b30;color:#e8f0ec;border:1px solid #80d9b2;cursor:pointer}
:focus-visible{outline:2px solid #80d9b2;outline-offset:3px}
@media(max-width:520px){header,main,footer{width:calc(100% - 24px)}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
</style>
</head>
<body>
<header>
<strong>SESSION SECURER</strong>
<p class="muted">Session monitoring and defensive security</p>
<nav aria-label="Main navigation">
<a href="/security-overview" aria-current="page">Overview</a>
<a href="/dashboard">Dashboard</a>
<a href="/social">Security Lab</a>
<a href="/terms">Terms</a>
<a href="/privacy">Privacy</a>
</nav>
</header>
<main>
<p class="muted">SECURITY / OVERVIEW</p>
<h1>Security overview</h1>
<p class="muted">Monitoring information from the application's existing APIs.</p>
<div id="status" class="panel" role="status" aria-live="polite">Loading monitoring data...</div>
<section class="panel">
<h2>Dashboard summary</h2>
<div id="summary" aria-busy="true">
<div class="skeleton"></div><div class="skeleton"></div>
<p class="muted">Loading summary...</p>
</div>
</section>
<section class="panel">
<h2>Active sessions</h2>
<pre id="sessions" class="muted">Loading sessions...</pre>
</section>
<section class="panel">
<h2>Security alerts</h2>
<pre id="alerts" class="muted">Loading alerts...</pre>
</section>
<section class="panel">
<h2>Quick actions</h2>
<p><a href="/dashboard">Open dashboard</a></p>
<p><a href="/social">Open Security Lab</a></p>
<button id="logout" type="button">Log out</button>
<p id="logout-status" class="muted" role="status" aria-live="polite"></p>
</section>
</main>
<footer class="muted"><p>Security depends on correctly configured controls and deployment.</p></footer>
<script>
"use strict";

function renderSummaryPanel(container, data) {
  container.replaceChildren();

  const entries = data && typeof data === "object" && !Array.isArray(data)
    ? Object.entries(data)
    : [["Summary", data]];

  if (entries.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "No summary data is currently available.";
    container.appendChild(empty);
    return;
  }

  const grid = document.createElement("div");
  grid.style.display = "grid";
  grid.style.gridTemplateColumns = "repeat(auto-fit, minmax(min(100%, 180px), 1fr))";
  grid.style.gap = "12px";

  for (const [key, value] of entries) {
    const item = document.createElement("section");
    item.style.background = "#17221e";
    item.style.border = "1px solid #40544a";
    item.style.padding = "14px";
    item.style.minWidth = "0";

    const label = document.createElement("h3");
    label.style.fontSize = "0.9rem";
    label.style.fontWeight = "500";
    label.style.overflowWrap = "anywhere";
    label.textContent = String(key)
      .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
      .replace(/[_-]+/g, " ");

    const metric = document.createElement("p");
    metric.style.fontSize = "1.15rem";
    metric.style.fontWeight = "600";
    metric.style.overflowWrap = "anywhere";

    if (value === null || value === undefined || value === "") {
      metric.textContent = "No data";
    } else if (typeof value === "object") {
      metric.textContent = JSON.stringify(value);
    } else {
      metric.textContent = String(value);
    }

    item.append(label, metric);
    grid.appendChild(item);
  }

  container.appendChild(grid);
}

async function loadPanel(url, target) {
 const el = document.getElementById(target);
 try {
  const response = await fetch(url, {
   credentials:"same-origin",
   headers:{"Accept":"application/json"}
  });
  const text = await response.text();
  if (!response.ok) {
      if (response.status === 401) {
          el.textContent = "Sign in is required to view this information.";
          el.setAttribute("aria-busy", "false");
           return false;
      }
      throw new Error("HTTP " + response.status);
  }
  let data;
  try { data = JSON.parse(text); } catch { data = text; }
  if (target === "summary") {
    renderSummaryPanel(el, data);
  } else {
    el.textContent = typeof data === "string"
      ? data
      : JSON.stringify(data, null, 2);
  }
  el.setAttribute("aria-busy", "false");
  return true;
 } catch (error) {
  el.textContent = "Data unavailable: " + error.message;
  el.setAttribute("aria-busy", "false");
  return false;
 }
}
(async () => {
 const results = await Promise.all([
  loadPanel("/api/dashboard/summary", "summary"),
  loadPanel("/api/dashboard/active-sessions", "sessions"),
  loadPanel("/api/dashboard/security-alerts", "alerts")
 ]);
 const status = document.getElementById("status");
 status.textContent = results.every(Boolean)
  ? "Monitoring data loaded."
  : "Some endpoints are unavailable. Review the sections below.";
})();
document.getElementById("logout").addEventListener("click", async () => {
 const button = document.getElementById("logout");
 const message = document.getElementById("logout-status");
 button.disabled = true;
 message.textContent = "Signing out...";
 try {
  const response = await fetch("/api/auth/logout", {
   method:"POST", credentials:"same-origin",
   headers:{"Accept":"application/json"}
  });
  if (response.ok) { window.location.assign("/"); return; }
  message.textContent = "Logout failed with HTTP " + response.status + ".";
 } catch {
  message.textContent = "Could not contact the server. Please retry.";
 } finally {
  button.disabled = false;
 }
});
</script>
</body>
</html>"""
    return Response(page, mimetype="text/html; charset=utf-8")


@web_bp.get("/security-center")
def security_center():
    """Security Center: sessions, events, and detection-flow overview."""
    from flask import Response

    page = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Security Center | Session Securer</title>
<style>
:root {
  color-scheme: dark;
  --bg: #101419;
  --panel: #171d24;
  --panel2: #1c242d;
  --line: #303b46;
  --text: #e8edf2;
  --muted: #a6b2bf;
  --accent: #7ec7bd;
  --danger: #ff9d9d;
  --focus: #f4d37a;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font: 16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
}
a { color: var(--accent); }
a:focus-visible, button:focus-visible {
  outline: 3px solid var(--focus); outline-offset: 3px;
}
header {
  border-bottom: 1px solid var(--line);
  padding: 1rem clamp(1rem, 4vw, 2.5rem);
}
nav {
  display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;
}
nav a { text-decoration: none; }
main {
  max-width: 1240px; margin: auto;
  padding: 1.5rem clamp(1rem, 4vw, 2.5rem) 3rem;
}
h1 { font-size: clamp(1.8rem, 4vw, 2.6rem); margin-bottom: .3rem; }
h2 { font-size: 1.2rem; margin-top: 0; }
.lead, .muted { color: var(--muted); }
.layout {
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem; margin-top: 1.5rem;
}
.panel {
  min-width: 0; padding: 1.2rem; border: 1px solid var(--line);
  border-radius: 12px; background: var(--panel);
}
.wide { grid-column: 1 / -1; }
.toolbar { display: flex; gap: .6rem; flex-wrap: wrap; }
button {
  font: inherit; color: var(--text); cursor: pointer;
  background: var(--panel2); border: 1px solid var(--line);
  padding: .55rem .8rem; border-radius: 6px;
}
button:hover { border-color: var(--accent); }
button.danger { border-color: #9d5555; color: var(--danger); }
.status { min-height: 1.5rem; color: var(--muted); }
.status.error { color: var(--danger); }
.list { display: grid; gap: .7rem; }
.item {
  padding: .8rem; border: 1px solid var(--line);
  border-radius: 8px; overflow-wrap: anywhere;
}
.item strong { display: block; }
.skeleton {
  height: 3.2rem; margin: .65rem 0; border-radius: 6px;
  background: #252e37;
}
dl { display: grid; grid-template-columns: minmax(100px, .4fr) 1fr; gap: .4rem .8rem; }
dt { color: var(--muted); } dd { margin: 0; overflow-wrap: anywhere; }
.flow {
  display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: .65rem; margin-top: 1rem;
}
.step {
  border: 1px solid var(--line); border-radius: 8px;
  padding: .85rem; background: var(--panel2); min-width: 0;
}
.step b { display: block; margin-bottom: .35rem; }
footer { border-top: 1px solid var(--line); margin-top: 2rem; padding-top: 1rem; }
@media (max-width: 760px) {
  .layout { grid-template-columns: 1fr; }
  .wide { grid-column: auto; }
  .flow { grid-template-columns: 1fr 1fr; }
  dl { grid-template-columns: 1fr; }
}
@media (max-width: 420px) {
  .flow { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; }
}
</style>
</head>
<body>
<header>
  <nav aria-label="Main navigation">
    <a href="/security-overview">Overview</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/security-center" aria-current="page">Security Center</a>
    <a href="/terms">Terms</a>
    <a href="/privacy">Privacy</a>
    <button id="logout-button" type="button">Log out</button>
  </nav>
</header>
<main>
  <h1>Security Center</h1>
  <p class="lead">Review sessions and security activity, and understand the detection flow.</p>
  <p id="global-status" class="status" role="status" aria-live="polite">Loading security data…</p>
  <div class="layout">
    <section class="panel wide" aria-labelledby="sessions-title">
      <h2 id="sessions-title">Active sessions</h2>
      <p class="muted">Revoke sessions you no longer recognize. Your current session may also appear here.</p>
      <div class="toolbar"><button id="refresh-sessions" type="button">Refresh sessions</button></div>
      <p id="sessions-status" class="status" role="status" aria-live="polite">Loading sessions…</p>
      <div id="sessions-list" class="list">
        <div class="skeleton" aria-hidden="true"></div>
        <div class="skeleton" aria-hidden="true"></div>
      </div>
    </section>
    <section class="panel" aria-labelledby="history-title">
      <h2 id="history-title">Login history</h2>
      <p id="history-status" class="status" role="status" aria-live="polite">Loading history…</p>
      <div id="history-list" class="list"><div class="skeleton" aria-hidden="true"></div></div>
    </section>
    <section class="panel" aria-labelledby="alerts-title">
      <h2 id="alerts-title">Security alerts</h2>
      <p id="alerts-status" class="status" role="status" aria-live="polite">Loading alerts…</p>
      <div id="alerts-list" class="list"><div class="skeleton" aria-hidden="true"></div></div>
    </section>
    <section class="panel wide" aria-labelledby="events-title">
      <h2 id="events-title">Security events</h2>
      <p id="events-status" class="status" role="status" aria-live="polite">Loading events…</p>
      <div id="events-list" class="list"><div class="skeleton" aria-hidden="true"></div></div>
    </section>
    <section class="panel wide" aria-labelledby="flow-title">
      <h2 id="flow-title">Architecture and detection flow</h2>
      <p class="muted">Conceptual overview of the application's security lifecycle. Actual behavior depends on configured services and policies.</p>
      <div class="flow" aria-label="Security detection flow">
        <div class="step"><b>1. Request</b><span class="muted">Browser sends a request and session cookie.</span></div>
        <div class="step"><b>2. Validation</b><span class="muted">Server resolves the session and checks access.</span></div>
        <div class="step"><b>3. Detection</b><span class="muted">Configured risk and security checks evaluate activity.</span></div>
        <div class="step"><b>4. Response</b><span class="muted">Application permits, challenges, blocks, logs, or revokes as configured.</span></div>
      </div>
    </section>
  </div>
  <footer class="muted">
    Security Center displays information returned by this application's existing APIs.
    It does not independently guarantee that a session or device is safe.
  </footer>
</main>
<script>
"use strict";
const $ = (id) => document.getElementById(id);

function status(id, message, isError=false) {
  const node = $(id);
  node.textContent = message;
  node.classList.toggle("error", Boolean(isError));
}
function asArray(payload) {
  if (Array.isArray(payload)) return payload;
  if (!payload || typeof payload !== "object") return [];
  for (const key of ["sessions", "items", "events", "alerts", "history", "data", "results"]) {
    if (Array.isArray(payload[key])) return payload[key];
  }
  return [];
}
function safeText(value) {
  if (value === null || value === undefined || typeof value === "object") return "";
  return String(value).slice(0, 500);
}
function field(obj, names) {
  for (const name of names) {
    if (obj && obj[name] !== undefined && obj[name] !== null) {
      const value = safeText(obj[name]);
      if (value) return value;
    }
  }
  return "";
}
function card(title, details) {
  const article = document.createElement("article");
  article.className = "item";
  const heading = document.createElement("strong");
  heading.textContent = title || "Activity";
  article.appendChild(heading);
  for (const detail of details) {
    if (!detail) continue;
    const line = document.createElement("div");
    line.textContent = detail;
    article.appendChild(line);
  }
  return article;
}
function showEmptyOrError(containerId, message) {
  const node = $(containerId);
  node.replaceChildren(card(message, []));
}
async function getJson(url) {
  const response = await fetch(url, {
    method: "GET",
    credentials: "same-origin",
    headers: { "Accept": "application/json" }
  });
  let data = null;
  try { data = await response.json(); } catch (_) {}
  if (!response.ok) {
    const error = new Error(
      response.status === 401 ? "Authentication required. Please sign in again." :
      response.status === 403 ? "Access denied." :
      "Request failed (HTTP " + response.status + ")."
    );
    error.status = response.status;
    throw error;
  }
  return data;
}
async function loadList({url, containerId, statusId, label, titleFields, detailFields}) {
  const container = $(containerId);
  status(statusId, "Loading " + label + "…");
  container.replaceChildren();
  try {
    const payload = await getJson(url);
    const items = asArray(payload);
    if (!items.length) {
      status(statusId, "No " + label + " returned.");
      showEmptyOrError(containerId, "No " + label + " available.");
      return;
    }
    for (const item of items.slice(0, 100)) {
      const title = field(item, titleFields) || label;
      const details = detailFields.map(names => field(item, names)).filter(Boolean);
      container.appendChild(card(title, details));
    }
    status(statusId, items.length + " record(s) loaded.");
  } catch (error) {
    status(statusId, error.message || "Could not load " + label + ".", true);
    showEmptyOrError(containerId, error.message || "Unable to load " + label + ".");
  }
}
async function loadSessions() {
  const container = $("sessions-list");
  status("sessions-status", "Loading sessions…");
  container.replaceChildren();
  try {
    // Use the existing sessions blueprint endpoint.
    const payload = await getJson("/api/sessions");
    const sessions = asArray(payload);
    if (!sessions.length) {
      status("sessions-status", "No active sessions returned.");
      showEmptyOrError("sessions-list", "No active sessions available.");
      return;
    }
    for (const session of sessions.slice(0, 100)) {
      const id = field(session, ["id", "session_id"]);
      const details = [
        field(session, ["device_type", "device", "device_info", "user_agent"]),
        field(session, ["browser"]),
        field(session, ["ip_address", "ip", "ip_address_masked"]),
        field(session, ["created_at", "issued_at", "login_at"]),
        field(session, ["last_seen", "last_seen_at", "last_activity"])
      ].filter(Boolean);
      const article = card(id ? "Session " + id : "Active session", details);
      if (id && /^\d+$/.test(id)) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "danger";
        button.textContent = "Revoke session";
        button.setAttribute("aria-label", "Revoke session " + id);
        button.addEventListener("click", async () => {
          if (!window.confirm("Revoke session " + id + "? This action cannot be undone.")) return;
          button.disabled = true;
          status("sessions-status", "Revoking session…");
          try {
            const response = await fetch("/api/sessions/" + encodeURIComponent(id), {
              method: "DELETE",
              credentials: "same-origin",
              headers: { "Accept": "application/json" }
            });
            if (!response.ok) {
              throw new Error(
                response.status === 401 ? "Authentication required." :
                response.status === 403 ? "Access denied." :
                response.status === 404 ? "Session not found." :
                "Revocation failed (HTTP " + response.status + ")."
              );
            }
            status("sessions-status", "Session revocation requested successfully.");
            await loadSessions();
          } catch (error) {
            status("sessions-status", error.message || "Could not revoke session.", true);
            button.disabled = false;
          }
        });
        article.appendChild(button);
      } else {
        const note = document.createElement("div");
        note.className = "muted";
        note.textContent = "A session identifier was not supplied, so revocation is unavailable for this record.";
        article.appendChild(note);
      }
      container.appendChild(article);
    }
    status("sessions-status", sessions.length + " session record(s) loaded.");
  } catch (error) {
    status("sessions-status", error.message || "Could not load sessions.", true);
    showEmptyOrError("sessions-list", error.message || "Unable to load sessions.");
  }
}
async function logout() {
  const button = $("logout-button");
  button.disabled = true;
  status("global-status", "Logging out…");
  try {
    const response = await fetch("/api/auth/logout", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Accept": "application/json" }
    });
    if (!response.ok) throw new Error("Logout failed (HTTP " + response.status + ").");
    status("global-status", "Logout successful. Redirecting…");
    window.location.assign("/login");
  } catch (error) {
    status("global-status", error.message || "Logout failed.", true);
    button.disabled = false;
  }
}
$("refresh-sessions").addEventListener("click", loadSessions);
$("logout-button").addEventListener("click", logout);

Promise.all([
  loadSessions(),
  loadList({
    url: "/api/dashboard/login-history",
    containerId: "history-list", statusId: "history-status",
    label: "login history",
    titleFields: ["event_type", "action", "status", "type", "title"],
    detailFields: [
      ["created_at", "timestamp", "occurred_at"],
      ["ip_address", "ip"],
      ["device", "user_agent"],
      ["message", "description"]
    ]
  }),
  loadList({
    url: "/api/dashboard/security-alerts",
    containerId: "alerts-list", statusId: "alerts-status",
    label: "security alerts",
    titleFields: ["title", "type", "severity", "event_type"],
    detailFields: [
      ["created_at", "timestamp", "occurred_at"],
      ["message", "description", "reason"],
      ["status", "classification"]
    ]
  }),
  loadList({
    url: "/api/social/events",
    containerId: "events-list", statusId: "events-status",
    label: "security events",
    titleFields: ["event_type", "type", "action", "title"],
    detailFields: [
      ["created_at", "timestamp", "occurred_at"],
      ["severity", "classification"],
      ["message", "description", "reason"]
    ]
  })
]).then(() => status("global-status", "Security data loading completed. Check each section for access or API errors."));
</script>
</body>
</html>"""
    return Response(page, mimetype="text/html")

# PHASE_7_20_PRIVACY_CONTROLS
# Self-contained pages; do not render API/user-supplied values as HTML.
# Browser permission prompts are controlled by the browser and user agent.
# The telemetry preference below is local to this browser and is not a
# server-side consent record or proof that telemetry is disabled server-side.

_PHASE720_CSS = """
:root {
  color-scheme: dark;
  --p720-bg: #111418;
  --p720-panel: #191e24;
  --p720-border: #343c46;
  --p720-text: #edf1f5;
  --p720-muted: #b7c0cb;
  --p720-accent: #a9c8e8;
  --p720-focus: #f4d27a;
}
.p720-page {
  max-width: 980px;
  margin: 0 auto;
  padding: clamp(1rem, 4vw, 2.5rem);
  color: var(--p720-text);
  background: var(--p720-bg);
  font: 16px/1.65 system-ui, -apple-system, "Segoe UI", sans-serif;
}
.p720-page * { box-sizing: border-box; }
.p720-page h1, .p720-page h2, .p720-page h3 { line-height: 1.25; }
.p720-page h1 { font-size: clamp(1.8rem, 4vw, 2.6rem); }
.p720-page h2 { margin-top: 2rem; font-size: 1.35rem; }
.p720-page p, .p720-page li { max-width: 78ch; }
.p720-page .p720-muted { color: var(--p720-muted); }
.p720-page .p720-panel {
  border: 1px solid var(--p720-border);
  background: var(--p720-panel);
  padding: clamp(1rem, 3vw, 1.5rem);
  margin: 1rem 0;
}
.p720-page .p720-actions { display: flex; flex-wrap: wrap; gap: .75rem; }
.p720-page button, .p720-page a.p720-button {
  display: inline-block;
  color: var(--p720-text);
  background: #273542;
  border: 1px solid #66798b;
  padding: .65rem .9rem;
  font: inherit;
  cursor: pointer;
  text-decoration: none;
}
.p720-page a { color: var(--p720-accent); }
.p720-page button:disabled { cursor: not-allowed; opacity: .65; }
.p720-page :focus-visible {
  outline: 3px solid var(--p720-focus);
  outline-offset: 3px;
}
.p720-page .p720-status { min-height: 1.5em; overflow-wrap: anywhere; }
.p720-page .p720-check { display: flex; align-items: flex-start; gap: .7rem; }
.p720-page input { margin-top: .45rem; }
.p720-page .p720-skip {
  position: absolute; left: -10000px; top: auto;
  width: 1px; height: 1px; overflow: hidden;
}
.p720-page .p720-skip:focus {
  position: static; width: auto; height: auto;
}
@media (prefers-reduced-motion: reduce) {
  .p720-page *, .p720-page *::before, .p720-page *::after {
    scroll-behavior: auto !important;
    animation-duration: .01ms !important;
    transition-duration: .01ms !important;
  }
}
"""

def _phase720_shell(title, body, extra_script=""):
    # title/body are developer-authored constants, not request parameters.
    from flask import make_response
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>""" + title + """ | Session Securer</title>
<style>""" + _PHASE720_CSS + """</style>
</head>
<body>
<div class="p720-page">
<a class="p720-skip" href="#main-content">Skip to main content</a>
<header>
  <p class="p720-muted">Session Securer · Security and privacy</p>
  <nav aria-label="Privacy navigation">
    <a href="/security-center">Security Center</a> ·
    <a href="/terms">Terms of Service</a> ·
    <a href="/privacy">Privacy Policy</a>
  </nav>
</header>
<main id="main-content">
""" + body + """
</main>
<footer class="p720-muted">
  <p>Review these controls in your browser and verify server-side behavior
  before relying on them for compliance or security decisions.</p>
</footer>
</div>
""" + (("<script>" + extra_script + "</script>") if extra_script else "") + """
</body>
</html>"""
    response = make_response(html, 200)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=(), payment=()"
    )
    return response

@web_bp.get("/terms")
def phase720_terms():
    body = """
<h1>Terms of Service</h1>
<p class="p720-muted">Informational project terms. Have these reviewed and
approved for your actual deployment before treating them as a legal agreement.</p>
<section class="p720-panel">
<h2>1. Acceptable use</h2>
<p>Use Session Securer only with accounts, devices, sessions, and systems
you are authorized to access. Do not use the service to violate law,
impersonate others, interfere with systems, or gain unauthorized access.</p>
<h2>2. Security limitations</h2>
<p>Security controls reduce risk but cannot guarantee that every attack,
compromise, outage, or data loss will be prevented. Keep your devices and
account credentials secure and report suspected vulnerabilities responsibly.</p>
<h2>3. Availability and changes</h2>
<p>Features may change, be unavailable, or be withdrawn for maintenance,
security, or operational reasons. Do not rely on the service as your only
means of protecting critical accounts or preserving important records.</p>
<h2>4. No unsupported promises</h2>
<p>No warranty, service level, compliance status, or fitness for a particular
purpose is promised by this informational page. Any binding terms must be
approved and published by the service operator.</p>
<h2>5. Contact and updates</h2>
<p>Before production release, the operator should provide a monitored contact
channel, an effective date, and a process for communicating material changes.</p>
</section>
<p><a href="/privacy">Read the Privacy Policy</a></p>
"""
    return _phase720_shell("Terms of Service", body)

@web_bp.get("/privacy")
def phase720_privacy():
    body = """
<h1>Privacy Policy</h1>
<p class="p720-muted">This page describes intended privacy principles. Confirm
actual data flows, retention, vendors, and legal requirements before production.</p>
<section class="p720-panel">
<h2>Information and purpose</h2>
<p>Authentication identifiers, session metadata, security events, and login
history may be processed when the application implements those features.
Collect only what is needed to operate the service, secure accounts, and
investigate abuse.</p>
<h2>Retention and access</h2>
<p>Define retention periods for sessions, audit events, and logs. Restrict access
to authorized operators and protect stored records against unauthorized reading,
alteration, and deletion.</p>
<h2>Sharing and third parties</h2>
<p>Disclose hosting providers, analytics tools, and other recipients only after
verifying which services the deployment actually uses. Do not assume that
this page disables collection performed by the server or third parties.</p>
<h2>Your choices</h2>
<p>You can manage browser permissions using the controls below and your browser
settings. The local telemetry preference is only a preference stored in this
browser; it does not disable server-side logging or network requests by itself.</p>
<h2>Contact and policy updates</h2>
<p>Publish a real privacy contact, applicable jurisdiction, effective date,
and a process for access, correction, deletion, and complaints where required.</p>
</section>
<section class="p720-panel" aria-labelledby="p720-controls-title">
<h2 id="p720-controls-title">Privacy controls</h2>
<p>These controls report browser capabilities and save a local preference.
They do not replace server-side consent enforcement.</p>
<div class="p720-check">
<input id="p720-telemetry" type="checkbox">
<label for="p720-telemetry">Allow optional telemetry preference in this browser</label>
</div>
<p id="p720-telemetry-status" class="p720-status" role="status" aria-live="polite"></p>
<h3>Browser permissions</h3>
<p class="p720-muted">Permission queries may be unsupported. Use your browser's
site settings to revoke permissions when a query or prompt is unavailable.</p>
<div class="p720-actions">
<button type="button" id="p720-check-permissions">Check permission status</button>
<button type="button" id="p720-location">Request location permission</button>
<button type="button" id="p720-notifications">Request notification permission</button>
</div>
<ul id="p720-permission-results" aria-live="polite"></ul>
<p id="p720-permission-status" class="p720-status" role="status" aria-live="polite"></p>
</section>
<p><a href="/terms">Read the Terms of Service</a></p>
"""
    script = r"""
(function () {
  "use strict";
  const telemetry = document.getElementById("p720-telemetry");
  const telemetryStatus = document.getElementById("p720-telemetry-status");
  const permissionResults = document.getElementById("p720-permission-results");
  const permissionStatus = document.getElementById("p720-permission-status");
  const storageKey = "session-securer.optional-telemetry-preference.v1";

  function setStatus(node, message) {
    node.textContent = message;
  }

  function loadPreference() {
    try {
      const saved = window.localStorage.getItem(storageKey);
      telemetry.checked = saved === "enabled";
      setStatus(
        telemetryStatus,
        saved === null
          ? "No preference saved in this browser."
          : "Saved local preference: " + (saved === "enabled" ? "enabled" : "disabled") + "."
      );
    } catch (_) {
      telemetry.checked = false;
      telemetry.disabled = true;
      setStatus(telemetryStatus, "Local storage is unavailable; no preference was changed.");
    }
  }

  telemetry.addEventListener("change", function () {
    try {
      window.localStorage.setItem(storageKey, telemetry.checked ? "enabled" : "disabled");
      setStatus(
        telemetryStatus,
        "Saved local preference: " + (telemetry.checked ? "enabled" : "disabled") +
        ". This does not change server-side logging or network requests."
      );
    } catch (_) {
      setStatus(telemetryStatus, "Could not save the preference in this browser.");
    }
  });

  async function queryPermission(name) {
    if (!navigator.permissions || typeof navigator.permissions.query !== "function") {
      return "status unavailable in this browser";
    }
    try {
      const result = await navigator.permissions.query({ name: name });
      return result.state;
    } catch (_) {
      return "unsupported or unavailable";
    }
  }

  async function checkPermissions() {
    permissionResults.replaceChildren();
    const checks = [
      ["geolocation", "Location"],
      ["notifications", "Notifications"],
      ["camera", "Camera"],
      ["microphone", "Microphone"]
    ];
    for (const entry of checks) {
      const li = document.createElement("li");
      const state = await queryPermission(entry[0]);
      li.textContent = entry[1] + ": " + state;
      permissionResults.appendChild(li);
    }
    setStatus(permissionStatus, "Permission status check finished.");
  }

  document.getElementById("p720-check-permissions").addEventListener("click", function () {
    checkPermissions().catch(function () {
      setStatus(permissionStatus, "Unable to check permissions in this browser.");
    });
  });

  document.getElementById("p720-location").addEventListener("click", function () {
    if (!navigator.geolocation) {
      setStatus(permissionStatus, "Geolocation is unavailable in this browser.");
      return;
    }
    setStatus(permissionStatus, "Waiting for the browser's location decision.");
    navigator.geolocation.getCurrentPosition(
      function () {
        setStatus(permissionStatus,
          "Location access was granted for this request. No coordinates are displayed here.");
      },
      function (error) {
        const messages = {
          1: "Location permission denied.",
          2: "Location position unavailable.",
          3: "Location request timed out."
        };
        setStatus(permissionStatus, messages[error.code] || "Location request failed.");
      },
      { maximumAge: 0, timeout: 10000, enableHighAccuracy: false }
    );
  });

  document.getElementById("p720-notifications").addEventListener("click", async function () {
    if (!("Notification" in window) || typeof Notification.requestPermission !== "function") {
      setStatus(permissionStatus, "Notifications are unavailable in this browser.");
      return;
    }
    try {
      const result = await Notification.requestPermission();
      setStatus(permissionStatus, "Notification permission: " + result + ".");
    } catch (_) {
      setStatus(permissionStatus, "Could not request notification permission.");
    }
  });

  loadPreference();
})();
"""
    return _phase720_shell("Privacy Policy", body, script)
