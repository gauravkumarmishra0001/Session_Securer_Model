
from flask import Blueprint, render_template_string

web_bp = Blueprint("web", __name__)

BASE_STYLE = """
<style>
:root{
    --bg:#080d11;
    --panel:#0d151a;
    --panel2:#111b21;
    --line:#24343d;
    --line2:#36505b;
    --text:#dce7eb;
    --muted:#83959e;
    --cyan:#54c6d8;
    --green:#70b995;
    --amber:#d2a85d;
    --red:#d66f72;
    --blue:#75a9d6;
    --font:"IBM Plex Mono","Cascadia Mono","SFMono-Regular",Consolas,monospace;
}

*{box-sizing:border-box}

html{
    background:var(--bg);
    color:var(--text);
}

body{
    margin:0;
    background:var(--bg);
    color:var(--text);
    font-family:var(--font);
    line-height:1.55;
}

a{
    color:var(--text);
    text-decoration:none;
}

button,input{
    font:inherit;
}

button{
    cursor:pointer;
}

.nav{
    min-height:64px;
    border-bottom:1px solid var(--line);
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 5vw;
    background:#091015;
    position:sticky;
    top:0;
    z-index:20;
}

.brand{
    font-weight:700;
    letter-spacing:.08em;
}

.navlinks{
    display:flex;
    gap:22px;
    align-items:center;
    flex-wrap:wrap;
}

.navlinks a{
    color:var(--muted);
    font-size:13px;
}

.navlinks a:hover{
    color:var(--text);
}

.container{
    width:min(1180px,90vw);
    margin:0 auto;
}

.hero{
    padding:90px 0 70px;
    border-bottom:1px solid var(--line);
}

.kicker{
    color:var(--cyan);
    font-size:12px;
    letter-spacing:.12em;
    text-transform:uppercase;
}

h1{
    font-size:clamp(32px,6vw,72px);
    line-height:1.02;
    margin:16px 0;
    max-width:900px;
}

h2{
    font-size:24px;
    margin:0 0 14px;
}

h3{
    font-size:16px;
}

.lead{
    max-width:760px;
    color:var(--muted);
    font-size:16px;
}

.actions{
    display:flex;
    gap:12px;
    flex-wrap:wrap;
    margin-top:30px;
}

.btn{
    display:inline-flex;
    align-items:center;
    justify-content:center;
    min-height:44px;
    padding:0 18px;
    border:1px solid var(--line2);
    background:#101a20;
    color:var(--text);
}

.btn.primary{
    background:#15333a;
    border-color:#397784;
    color:#dff8fc;
}

.btn.danger{
    background:#321b1d;
    border-color:#754247;
}

.section{
    padding:65px 0;
    border-bottom:1px solid var(--line);
}

.grid{
    display:grid;
    grid-template-columns:repeat(2,minmax(0,1fr));
    gap:16px;
}

.panel{
    border:1px solid var(--line);
    background:var(--panel);
    padding:22px;
}

.panel p{
    color:var(--muted);
}

.metric-grid{
    display:grid;
    grid-template-columns:repeat(4,minmax(0,1fr));
    gap:12px;
}

.metric{
    border:1px solid var(--line);
    background:var(--panel);
    padding:18px;
}

.metric-value{
    font-size:25px;
    margin-top:8px;
}

.label{
    color:var(--muted);
    font-size:12px;
}

form{
    max-width:520px;
}

.field{
    margin-bottom:15px;
}

label{
    display:block;
    color:var(--muted);
    font-size:12px;
    margin-bottom:7px;
}

input{
    width:100%;
    min-height:46px;
    border:1px solid var(--line2);
    background:#091116;
    color:var(--text);
    padding:10px 12px;
    outline:none;
}

input:focus{
    border-color:var(--cyan);
}

.notice{
    border:1px solid var(--line);
    background:#0c1419;
    padding:15px;
    margin:15px 0;
}

.success{
    color:var(--green);
}

.warning{
    color:var(--amber);
}

.error{
    color:var(--red);
}

.muted{
    color:var(--muted);
}

pre{
    overflow:auto;
    border:1px solid var(--line);
    background:#070c10;
    padding:16px;
    color:#b9ccd3;
}

footer{
    padding:35px 0;
    color:var(--muted);
    font-size:12px;
}

.skeleton{
    min-height:18px;
    background:#17232a;
    margin:8px 0;
}

@media(max-width:800px){
    .nav{
        padding:12px 5vw;
        align-items:flex-start;
        gap:12px;
        flex-direction:column;
    }

    .navlinks{
        gap:12px;
    }

    .hero{
        padding:60px 0 45px;
    }

    .grid,
    .metric-grid{
        grid-template-columns:1fr;
    }

    h1{
        font-size:40px;
    }

    .btn{
        width:100%;
    }

    .actions{
        flex-direction:column;
    }
}
</style>
"""

NAV = """
<nav class="nav">
  <a class="brand" href="/">SESSION SECURER</a>
  <div class="navlinks">
    <a href="/">Home</a>
    <a href="/how-it-works">How it works</a>
    <a href="/social">Social Lab</a>
    <a href="/events">Events</a>
    <a href="/sessions">Sessions</a>
    <a href="/dashboard">Dashboard</a>
    <a href="/login">Login</a>
    <a href="/register">Register</a>
  </div>
</nav>
"""

FOOTER = """
<footer>
  <div class="container">
    <div>Session Securer</div>
    <div>Defensive session security prototype</div>
    <div style="margin-top:10px">
      <a href="/terms">Terms of Service</a> ·
      <a href="/privacy">Privacy Policy</a>
    </div>
  </div>
</footer>
"""

HOME = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Session Securer</title>
""" + BASE_STYLE + """
</head>
<body>
""" + NAV + """
<main>
<section class="hero">
<div class="container">
<div class="kicker">Session security platform</div>
<h1>Detect suspicious sessions before they become incidents.</h1>
<p class="lead">
Session Securer combines authentication, session telemetry,
behavior analysis, risk scoring and response controls in one defensive system.
</p>
<div class="actions">
<a class="btn primary" href="/register">Create account</a>
<a class="btn" href="/social">Open security lab</a>
<a class="btn" href="/how-it-works">View architecture</a>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="grid">
<div class="panel">
<h2>Authentication</h2>
<p>Account registration, password hashing, login and secure session creation.</p>
</div>
<div class="panel">
<h2>Detection</h2>
<p>Session events provide the data used for behavioral analysis and anomaly detection.</p>
</div>
<div class="panel">
<h2>Risk engine</h2>
<p>Rule-based and machine-learning signals can contribute to session risk assessment.</p>
</div>
<div class="panel">
<h2>Response</h2>
<p>Normal activity can proceed while suspicious activity can require verification or blocking.</p>
</div>
</div>
</div>
</section>

<section class="section">
<div class="container">
<div class="kicker">Defense in depth</div>
<h2>One system, multiple security layers.</h2>
<p class="lead">
Authentication, session management, detection, machine-learning analysis,
prevention and monitoring work together rather than relying on one control.
</p>
</div>
</section>
</main>
""" + FOOTER + """
</body>
</html>
"""

AUTH_PAGE = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }} · Session Securer</title>
""" + BASE_STYLE + """
</head>
<body>
""" + NAV + """
<main class="section">
<div class="container">
<div class="panel">
<div class="kicker">{{ title }}</div>
<h1 style="font-size:38px">{{ title }}</h1>

<div id="message" class="notice muted">Ready.</div>

<form id="authForm">
{% if register %}
<div class="field">
<label>Username</label>
<input id="username" autocomplete="username" required>
</div>
{% endif %}

<div class="field">
<label>Email</label>
<input id="email" type="email" autocomplete="email" required>
</div>

<div class="field">
<label>Password</label>
<input id="password" type="password" autocomplete="{{ 'new-password' if register else 'current-password' }}" required>
</div>

<button class="btn primary" type="submit">
{{ "Create account" if register else "Sign in" }}
</button>
</form>
</div>
</div>
</main>

<script>
const form=document.getElementById("authForm");
const msg=document.getElementById("message");

form.addEventListener("submit",async(e)=>{
    e.preventDefault();

    msg.className="notice muted";
    msg.textContent="Authenticating...";

    const payload={
        email:document.getElementById("email").value,
        password:document.getElementById("password").value
    };

    {% if register %}
    payload.username=document.getElementById("username").value;
    const endpoint="/api/auth/register";
    {% else %}
    const endpoint="/api/auth/login";
    {% endif %}

    try{
        const response=await fetch(endpoint,{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            credentials:"same-origin",
            body:JSON.stringify(payload)
        });

        const data=await response.json().catch(()=>({}));

        if(!response.ok){
            msg.className="notice error";
            msg.textContent=data.error || data.message || "Request failed.";
            return;
        }

        msg.className="notice success";
        msg.textContent="{{ 'Account created. Redirecting to login...' if register else 'Login successful. Redirecting...' }}";

        setTimeout(()=>{
            window.location.href="{{ '/login' if register else '/dashboard' }}";
        },700);

    }catch(error){
        msg.className="notice error";
        msg.textContent="Network error. Please try again.";
    }
});
</script>
""" + FOOTER + """
</body>
</html>
"""

INFO_PAGE = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title }} · Session Securer</title>
""" + BASE_STYLE + """
</head>
<body>
""" + NAV + """
<main class="section">
<div class="container">
<div class="kicker">Session Securer</div>
<h1 style="font-size:42px">{{ title }}</h1>
<div class="panel">
{{ body|safe }}
</div>
</div>
</main>
""" + FOOTER + """
</body>
</html>
"""

@web_bp.route("/")
def home():
    return HOME

@web_bp.route("/login")
def login_page():
    return render_template_string(AUTH_PAGE, title="Sign in", register=False)

@web_bp.route("/register")
def register_page():
    return render_template_string(AUTH_PAGE, title="Create account", register=True)

@web_bp.route("/social")
def social_page():
    return render_template_string(INFO_PAGE, title="Social Security Lab", body="""
    <p>Use the Social Security Lab to generate controlled security scenarios.</p>

    <div class="actions">
      <button class="btn primary" onclick="runScenario('normal')">Normal login</button>
      <button class="btn" onclick="runScenario('new-device')">New device</button>
      <button class="btn danger" onclick="runScenario('high-risk')">High risk</button>
    </div>

    <div id="result" class="notice muted">No scenario executed.</div>

    <script>
    async function runScenario(type){
        const result=document.getElementById("result");
        result.className="notice muted";
        result.textContent="Running security scenario...";

        const endpoint="/api/social/simulate/"+type;

        try{
            const r=await fetch(endpoint,{
                method:"POST",
                headers:{"Content-Type":"application/json"},
                credentials:"same-origin"
            });

            const data=await r.json().catch(()=>({}));

            result.className=r.ok ? "notice success" : "notice error";
            result.textContent=JSON.stringify(data,null,2);
        }catch(e){
            result.className="notice error";
            result.textContent="Request failed.";
        }
    }
    </script>
    """)

@web_bp.route("/dashboard")
def dashboard_page():
    return render_template_string(INFO_PAGE, title="Security Dashboard", body="""
    <div id="dashboard">
      <div class="metric-grid">
        <div class="metric"><div class="label">Active sessions</div><div id="active" class="metric-value"><div class="skeleton"></div></div></div>
        <div class="metric"><div class="label">Login events</div><div id="logins" class="metric-value"><div class="skeleton"></div></div></div>
        <div class="metric"><div class="label">Risk assessments</div><div id="risks" class="metric-value"><div class="skeleton"></div></div></div>
        <div class="metric"><div class="label">Alerts</div><div id="alerts" class="metric-value"><div class="skeleton"></div></div></div>
      </div>

      <div class="actions">
        <button class="btn" onclick="loadDashboard()">Refresh</button>
        <button class="btn danger" onclick="logout()">Logout</button>
      </div>

      <div id="status" class="notice muted">Loading dashboard...</div>
      <pre id="data">Loading...</pre>
    </div>

    <script>
    async function getJSON(url){
        const r=await fetch(url,{credentials:"same-origin"});
        if(r.status===401){
            window.location.href="/login";
            return null;
        }
        return await r.json();
    }

    async function loadDashboard(){
        const status=document.getElementById("status");
        const output=document.getElementById("data");

        status.textContent="Loading security telemetry...";

        try{
            const summary=await getJSON("/api/dashboard/summary");
            if(!summary)return;

            document.getElementById("active").textContent=
                summary.active_sessions ?? summary.active ?? 0;

            document.getElementById("logins").textContent=
                summary.login_events ?? summary.login_history ?? 0;

            document.getElementById("risks").textContent=
                summary.risk_assessments ?? summary.risks ?? 0;

            document.getElementById("alerts").textContent=
                summary.security_alerts ?? summary.alerts ?? 0;

            const routes=[
                "/api/dashboard/summary",
                "/api/dashboard/active-sessions",
                "/api/dashboard/login-history",
                "/api/dashboard/risk-scores",
                "/api/dashboard/blocked-attempts",
                "/api/dashboard/security-alerts"
            ];

            const results={};

            for(const route of routes){
                results[route]=await getJSON(route);
            }

            output.textContent=JSON.stringify(results,null,2);
            status.className="notice success";
            status.textContent="Security telemetry loaded.";
        }catch(e){
            status.className="notice error";
            status.textContent="Dashboard request failed.";
        }
    }

    async function logout(){
        await fetch("/api/auth/logout",{
            method:"POST",
            credentials:"same-origin"
        });
        window.location.href="/login";
    }

    loadDashboard();
    </script>
    """)

@web_bp.route("/sessions")
def sessions_page():
    return render_template_string(INFO_PAGE, title="Session Management", body="""
    <p>Authenticated session management.</p>
    <div id="sessions" class="notice muted">Loading sessions...</div>

    <script>
    async function load(){
        const r=await fetch("/api/sessions",{credentials:"same-origin"});
        if(r.status===401){
            location.href="/login";
            return;
        }

        const data=await r.json();
        document.getElementById("sessions").textContent=
            JSON.stringify(data,null,2);
    }
    load();
    </script>
    """)

@web_bp.route("/events")
def events_page():
    return render_template_string(INFO_PAGE, title="Security Events", body="""
    <p>Session and simulated social security events.</p>
    <div id="events" class="notice muted">Loading events...</div>

    <script>
    async function load(){
        const r=await fetch("/api/social/events",{credentials:"same-origin"});
        if(r.status===401){
            location.href="/login";
            return;
        }

        const data=await r.json();
        document.getElementById("events").textContent=
            JSON.stringify(data,null,2);
    }
    load();
    </script>
    """)

@web_bp.route("/how-it-works")
def how_it_works():
    return render_template_string(INFO_PAGE, title="How It Works", body="""
    <h2>01 · Authentication</h2>
    <p>User credentials are verified and an authenticated session is created.</p>

    <h2>02 · Session telemetry</h2>
    <p>Security-relevant session events can include device and network information.</p>

    <h2>03 · Detection</h2>
    <p>Behavioral features are evaluated against available history.</p>

    <h2>04 · Risk analysis</h2>
    <p>Rule-based and ML signals contribute to risk classification.</p>

    <h2>05 · Prevention</h2>
    <p>Depending on the security decision, a session can be allowed, challenged or blocked.</p>

    <h2>06 · Monitoring</h2>
    <p>Security events and assessments are surfaced through the dashboard.</p>
    """)

@web_bp.route("/terms")
def terms():
    return render_template_string(INFO_PAGE, title="Terms of Service", body="""
    <p>This project is a defensive security prototype.</p>
    <p>Do not use it to monitor, access or interfere with accounts or systems without authorization.</p>
    <p>The software is provided for authorized testing, education and security engineering purposes.</p>
    """)

@web_bp.route("/privacy")
def privacy():
    return render_template_string(INFO_PAGE, title="Privacy Policy", body="""
    <p>Session Securer may process authentication and security telemetry required for its defensive functionality.</p>
    <p>Use the system only with appropriate authorization and configure data retention according to your deployment requirements.</p>
    <p>A production deployment should add a formal retention policy, encryption strategy, access controls and applicable legal notices.</p>
    """)
