# Session Securer Model

## AI-Based Unusual Login and Session Security Detection System

Session Securer Model is a Flask-based security prototype that combines secure authentication, session management, behavioural analysis, machine-learning anomaly detection, risk-based prevention, OTP verification, and security monitoring.

The project was developed incrementally through five phases. Each phase extends the previous phase and contributes to an end-to-end login and session security pipeline.

---

# Project Objective

The objective of the project is to detect unusual login and session behaviour and respond according to the calculated security risk.

The system is designed around the following flow:

User
-> Authentication
-> Session Creation
-> Session Events
-> Feature Engineering
-> Behavioural Detection
-> Machine Learning
-> Risk Assessment
-> ALLOW / VERIFY / BLOCK
-> OTP Verification or Session Revocation
-> Security Monitoring and Dashboard

The project focuses on defensive security: detecting suspicious activity and protecting sessions rather than bypassing authentication or session controls.

---

# Phase 1 — Working Login System

## Objective

Phase 1 establishes the secure authentication and session-management foundation used by all later phases.

## Implemented Features

### 1. User Registration

The system provides a registration flow for creating users with a username, email address, and password.

Email values are normalized before being used by the authentication layer.

### 2. Password Security

Passwords are not stored as plain text.

The authentication service hashes passwords and verifies supplied passwords against the stored password hash during login.

### 3. Login

The login endpoint authenticates registered users using their credentials.

Successful authentication creates a server-side session.

### 4. Secure Session Creation

A session record stores information required to manage an authenticated login.

Session information includes:

- User ID
- Session token hash
- IP address
- User agent
- Device type
- Browser
- Operating system
- Creation time
- Last activity time
- Expiration time
- Revocation time

The usable session token is not stored directly as a database value; the session token hash is stored for session management.

### 5. Session Expiration

Sessions contain expiration information and an active-session check.

Expired sessions are therefore distinguishable from currently active sessions.

### 6. Session Revocation

Sessions can be revoked.

Revocation is used later by the prevention layer when suspicious or high-risk activity needs to be stopped.

### 7. Device Information

The system extracts device-related information from the login request.

Collected information includes:

- Device type
- Browser
- Operating system
- User agent
- IP address

### 8. Session Management

The session service provides functionality for creating, retrieving, checking, and revoking sessions.

### 9. Authentication Tests

Automated tests were added for the authentication and session-management foundation.

## Phase 1 Result

Phase 1 provides the secure base required for behavioural detection and later security controls.

Status: COMPLETED

---

# Phase 2 — Detection

## Objective

Phase 2 adds behavioural detection on top of the authentication and session system.

The purpose is to collect login/session characteristics and compare current activity with previously observed behaviour.

## Implemented Features

### 1. Session Event Collection

Login and session activity is recorded as security events.

The event information provides historical data for later analysis.

### 2. Behavioural Features

The detection layer works with session characteristics such as:

- IP address
- Device type
- Browser
- Operating system
- User agent
- Session timing
- Historical session activity

### 3. User Behaviour Profile

Historical session events are used to establish a normal behavioural profile for a user.

The profile allows the system to determine whether a new login resembles previously observed activity.

### 4. Historical Event Analysis

The detection service checks the number and characteristics of previous events before making stronger behavioural decisions.

A new user or a user with insufficient historical activity is treated differently from a user with an established profile.

### 5. Unusual Device Detection

The system can identify device characteristics that differ from the user's previously observed behaviour.

### 6. Unusual Location / IP Pattern Detection

IP-related information is used as part of the behavioural analysis.

The system can identify activity that differs from the user's historical IP/location-related patterns.

The system records the IP address and uses it as a behavioural feature; it does not require a third-party geolocation service to perform the core detection.

### 7. Rule-Based Anomaly Detection

Phase 2 provides rule-based classification of session behaviour.

The detection layer can classify activity as normal, unusual, or high-risk according to the available behavioural evidence.

### 8. Detection Service

The detection service combines historical profile information and session features into a detection result that can be consumed by the risk and prevention layers.

## Phase 2 Result

Phase 2 transforms raw authentication/session activity into security-relevant behavioural information.

Status: COMPLETED

---

# Phase 3 — Machine Learning

## Objective

Phase 3 extends the detection system with machine-learning-based anomaly detection and risk scoring.

## Implemented Features

### 1. Training Data Generation

Training-data functionality was added to create data suitable for anomaly-detection experiments.

### 2. Feature Engineering

Session information is converted into a structured feature vector for machine-learning processing.

The feature-engineering layer prepares the behavioural characteristics required by the ML models.

### 3. Isolation Forest

An Isolation Forest model is used for unsupervised anomaly detection.

The model is intended to identify session behaviour that differs from the learned normal pattern.

### 4. ML Model Training

The project includes an ML training service responsible for preparing data and training the Isolation Forest model.

### 5. Model Persistence

The ML pipeline supports saving/loading the trained model so that detection does not require retraining for every request.

### 6. ML Classification

The ML service produces an anomaly-related classification that can be combined with the rule-based detection result.

### 7. Risk Scoring

A risk service converts detection information into a risk score/classification that can be consumed by the prevention and monitoring layers.

### 8. Rule-Based + ML Detection

The system does not depend only on one detection method.

Behavioural/rule-based detection and machine-learning detection can both contribute to the final security assessment.

### 9. Autoencoder Support

An Autoencoder service was included as an optional extension for additional anomaly-detection experimentation.

The Isolation Forest path is the primary ML anomaly-detection component implemented in this phase.

### 10. ML Testing

Automated tests were added for feature generation, ML processing, risk scoring, and detection behaviour.

## Phase 3 Result

Phase 3 adds a machine-learning layer to the behavioural detection pipeline and produces risk information that can be used by the prevention system.

Status: COMPLETED

---

# Phase 4 — Prevention

## Objective

Phase 4 converts detection and risk information into active security actions.

The system can allow normal activity, request additional verification for suspicious activity, or block high-risk sessions.

## Implemented Features

### 1. Prevention Decision Engine

A dedicated prevention service evaluates the detection result and selects a security action.

The main actions are:

- ALLOW
- VERIFY
- BLOCK

### 2. Normal Login

Normal activity is allowed to continue through the normal authentication/session flow.

### 3. Suspicious Login Verification

Unusual activity can require additional verification rather than being immediately treated as a normal login.

### 4. OTP Challenge

The system creates an OTP challenge for verification.

The challenge is associated with the relevant user/session context.

### 5. OTP Hashing

The OTP is stored as a hash rather than as a reusable plain-text database value.

### 6. OTP Expiration

OTP challenges have an expiration time.

An expired challenge cannot be used as a valid verification mechanism.

### 7. Single-Use OTP

Once successfully verified, an OTP challenge is marked as used.

This prevents the same challenge from being reused.

### 8. High-Risk Blocking

High-risk activity can be blocked before the suspicious session is allowed to continue normally.

### 9. Suspicious Session Revocation

Suspicious/high-risk sessions can be revoked through the session service.

### 10. Prevention API

A prevention route was added for OTP verification and related security actions.

### 11. Authentication + Detection + Prevention Integration

The authentication flow was extended so that session creation can be followed by detection and a prevention decision.

This connects the earlier phases into a single security pipeline.

### 12. Prevention Testing

Automated tests cover:

- Normal activity
- Suspicious activity
- High-risk activity
- OTP verification
- Session blocking
- Session revocation

## Phase 4 Result

Phase 4 turns detection into an active defensive response system.

Status: COMPLETED

---

# Phase 5 — Security Dashboard and Monitoring

## Objective

Phase 5 adds security monitoring and dashboard functionality so that session activity, risk assessments, and alerts can be inspected.

## Implemented Features

### 1. Risk Assessment Model

A dedicated risk-assessment model stores security assessment information associated with session activity.

Risk information can include:

- Risk score
- Security classification
- Session context
- Assessment time

### 2. Security Alert Model

A security-alert model was added to represent security events that require monitoring or attention.

### 3. Security Monitoring Service

The monitoring service connects security decisions with persistent monitoring information.

It provides a place for security decisions and alerts to be recorded for later dashboard visibility.

### 4. Dashboard Service

A dashboard service aggregates relevant security information for presentation.

### 5. Active Sessions

The dashboard can display active session information.

This includes session-related details such as:

- Session ID
- User
- Device
- Browser
- Operating system
- IP information
- Session status

### 6. Login History

The dashboard exposes historical login/session activity so that previous authentication events can be inspected.

### 7. Risk Scores

Risk assessment information can be displayed as part of the monitoring view.

This provides visibility into the security classification assigned to session activity.

### 8. Blocked Attempts

Security monitoring includes information about blocked or high-risk activity.

### 9. Device Information

The monitoring view can display device-related information collected during authentication.

### 10. Location / IP Information

The dashboard exposes IP-related information used during login/session analysis.

The core project records IP information rather than depending on an external geolocation provider.

### 11. Security Alerts

Security alerts provide visibility into important security decisions and suspicious activity.

### 12. Dashboard Route

A dedicated dashboard route was added to expose the monitoring interface.

### 13. Dashboard Testing

Automated tests were added for the Phase 5 monitoring/dashboard functionality.

## Phase 5 Result

Phase 5 provides the monitoring layer needed to inspect the security activity generated by the earlier phases.

Status: COMPLETED

---

# Complete Security Pipeline

The final project connects all five phases:

Authentication
|
v
User Login
|
v
Session Creation
|
v
Session Event Collection
|
v
Feature Engineering
|
v
Behavioural Detection
|
v
Machine Learning
|
v
Risk Assessment
|
v
+-----------------------------+
| Security Decision            |
+-----------------------------+
| ALLOW                       |
| VERIFY                      |
| BLOCK                       |
+-----------------------------+
|
+--------------------+
|                    |
v                    v
OTP Verification   Session Revocation
|
v
Security Monitoring
|
v
Dashboard
|
v
Security Alerts

---

# Technology Stack

## Programming Language

Python

## Web Framework

Flask

## Database

SQLite

Flask-SQLAlchemy

## Machine Learning

Scikit-learn

Isolation Forest

Optional Autoencoder support

## Data Processing

Pandas

NumPy

Joblib

## Testing

Pytest

## Development

Google Colab

Git

GitHub

---

# Project Structure

app/
    models/
    routes/
    services/

data/

models/

tests/

requirements.txt

run.py

README.md

The root-level project files such as requirements.txt, run.py, and .gitignore belong to the overall application and are shared across all phases. They do not need separate copies for Phase 2, Phase 3, Phase 4, or Phase 5.

---

# Testing

The project contains automated tests covering the major components developed throughout the five phases.

Testing areas include:

- User registration
- Login
- Password verification
- Session creation
- Session management
- Session expiration
- Session revocation
- Detection
- Feature engineering
- ML anomaly detection
- Risk scoring
- Prevention decisions
- OTP verification
- High-risk blocking
- Suspicious-session revocation
- Security monitoring
- Dashboard functionality

Run the complete test suite with:

pytest -q

---

# Development Progress

Phase 1 — Working Login System — COMPLETED

Phase 2 — Detection — COMPLETED

Phase 3 — Machine Learning — COMPLETED

Phase 4 — Prevention — COMPLETED

Phase 5 — Dashboard and Security Monitoring — COMPLETED

---

# Final Outcome

The completed project provides an end-to-end defensive security prototype that starts with authentication and ends with security monitoring.

The five phases build on each other:

Phase 1 provides authentication and session management.

Phase 2 adds behavioural detection.

Phase 3 adds machine-learning anomaly detection and risk scoring.

Phase 4 adds active prevention and OTP-based verification.

Phase 5 adds security monitoring, risk visibility, alerts, and dashboard functionality.

---

# Author

Gaurav Kumar Mishra

GitHub:
https://github.com/gauravkumarmishra0001

Repository:
https://github.com/gauravkumarmishra0001/Session_Securer_Model
---

# Phase 6 - Security Web Platform and Social Security Lab

**Status: Completed / Prototype Ready**

Phase 6 adds the browser-based security interface and a controlled simulated social-security environment.

## Phase 6 Objectives

- Browser-based Session Securer interface
- User registration and authentication
- Authenticated security dashboard
- Session management
- Security-event monitoring
- Controlled social-security simulation
- Normal, new-device and high-risk scenarios
- Terms of Service and Privacy Policy
- Responsive desktop and mobile interface
- Defense-in-depth browser security controls
- HTTPS support for public demonstrations

## Phase 6 Web Interface

| Route | Purpose |
|---|---|
| `/` | Security platform overview |
| `/login` | User authentication |
| `/register` | Account registration |
| `/dashboard` | Authenticated security dashboard |
| `/sessions` | Session management |
| `/events` | Security event monitoring |
| `/social` | Social Security Lab |
| `/how-it-works` | Security architecture |
| `/terms` | Terms of Service |
| `/privacy` | Privacy Policy |

## Security Dashboard

The dashboard provides authenticated access to:

- Active sessions
- Login history
- Risk assessments
- Blocked attempts
- Security alerts
- Security telemetry

Dashboard access requires authentication.

## Social Security Lab

Phase 6 includes a controlled simulated social platform for defensive security demonstrations.

Available scenarios:

### Normal Authentication

Represents expected authentication behavior from a known context.

### New-Device Authentication

Represents authentication from an unusual device and demonstrates elevated security handling.

### High-Risk Authentication

Represents a high-risk authentication event and demonstrates defensive blocking behavior.

The simulation does not claim access to private security telemetry from external social-media platforms.

## Phase 6 API Routes

### Authentication

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

### Sessions

```text
GET    /api/sessions
DELETE /api/sessions/<session_id>
```

### Detection

```text
GET /api/detection/current
```

### Prevention

```text
POST /api/prevention/otp/verify
```

### Dashboard

```text
GET /api/dashboard/summary
GET /api/dashboard/active-sessions
GET /api/dashboard/login-history
GET /api/dashboard/risk-scores
GET /api/dashboard/blocked-attempts
GET /api/dashboard/security-alerts
```

### Social Security Lab

```text
GET  /api/social/events
POST /api/social/simulate/normal
POST /api/social/simulate/new-device
POST /api/social/simulate/high-risk
```

## Browser Security Controls

Phase 6 applies defense-in-depth controls including:

- HTTP-only session cookies
- SameSite cookie configuration
- Secure cookie configuration for HTTPS
- Content Security Policy
- X-Content-Type-Options
- X-Frame-Options
- Referrer-Policy
- Permissions-Policy
- Protected dashboard routes
- Authenticated session management
- Security event monitoring

These controls improve security but do not guarantee absolute protection against every vulnerability or attack.

## Responsive Design

The web interface is designed for:

- Desktop
- Laptop
- Tablet
- Android devices
- iPhone and other mobile browsers

## HTTPS Demonstration

The application can be exposed temporarily through an HTTPS Cloudflare Quick Tunnel.

```text
Browser
   |
   | HTTPS
   v
Cloudflare Tunnel
   |
   | localhost
   v
Flask Application
   |
   v
Session Securer
```

The Quick Tunnel URL is temporary and depends on the active Colab runtime.

For permanent deployment, the project should use a persistent cloud environment, production database, managed secrets, TLS, monitoring, rate limiting and CSRF protection.

## Phase 6 Security Architecture

```text
Authentication
      |
      v
Session Management
      |
      v
Session Events
      |
      v
Behavioral Detection
      |
      v
ML Risk Analysis
      |
      v
Prevention
      |
      v
Security Monitoring
      |
      v
Web Dashboard
```

No software system can honestly guarantee that it is impossible to hack. Session Securer therefore uses layered defensive controls and controlled security testing.

## Project Phase Status

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Authentication and Session Management | Completed |
| Phase 2 | Behavioral Detection | Completed |
| Phase 3 | Machine Learning Risk Analysis | Completed |
| Phase 4 | Prevention and OTP Security | Completed |
| Phase 5 | Security Dashboard and Monitoring | Completed |
| Phase 6 | Security Web Platform and Social Security Lab | Completed / Prototype Ready |

