# Session Securer Model

## AI-Based Unusual Login and Session Security Detection System

This project is an AI-based security system for detecting unusual login and session activity, calculating risk, preventing suspicious sessions, and providing security monitoring.

# Phase 1 — Working Login System

Features:
- Register/login
- Password hashing
- Session creation
- Device information
- Session management

Status: Completed.

# Phase 2 — Detection

Features:
- Collect login/session features
- Build normal user profile
- Calculate anomaly score
- Detect unusual devices/locations

Status: Completed.

# Phase 3 — ML

Features:
- Generate training data
- Train Isolation Forest
- Optional Autoencoder
- Risk scoring

Status: Completed.

# Phase 4 — Prevention

Features:
- Allow normal login
- Require OTP/2FA for suspicious login
- Block high-risk sessions
- Revoke suspicious sessions

Status: Completed.

# Phase 5 — Dashboard

Features:
- Active sessions
- Login history
- Risk scores
- Blocked attempts
- Device/location information
- Security alerts

Status: Completed.

# Complete Project Flow

Authentication
Session Creation
Session Events
Feature Engineering
Behavioural Detection
Machine Learning
Risk Scoring
ALLOW / VERIFY / BLOCK
OTP Verification
Session Revocation
Security Alerts
Security Dashboard

# Technology Stack

Python
Flask
Flask-SQLAlchemy
SQLite
Scikit-learn
Pandas
NumPy
Joblib
Pytest
Git
GitHub

# Testing

The project contains automated tests for authentication, session management, detection, machine learning, prevention, OTP verification, and dashboard functionality.

Run:

pytest -q

# Project Status

Phase 1 — Working Login System — Completed
Phase 2 — Detection — Completed
Phase 3 — Machine Learning — Completed
Phase 4 — Prevention — Completed
Phase 5 — Dashboard — Completed

# Author

Gaurav Kumar Mishra

GitHub: https://github.com/gauravkumarmishra0001
Repository: https://github.com/gauravkumarmishra0001/Session_Securer_Model
