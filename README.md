# Session Securer Model

## Phase 1: Secure Authentication and Session Management

Session Securer Model is a defensive security prototype designed to collect and manage authentication and session information for future behavioral security analysis.

## Phase 1 Objectives

- User registration
- Secure password hashing
- User authentication
- Session creation
- Session expiration
- Device information collection
- Active session management
- Session revocation
- Logout
- Automated testing

## Architecture

Authentication
    ↓
Session Events
    ↓
User Behavior + Global Patterns
    ↓
Feature Engineering
    ↓
Machine Learning
    ↓
Risk Engine
    ↓
ALLOW / VERIFY / BLOCK

Machine learning is intentionally not implemented in Phase 1.

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Werkzeug password hashing
- user-agents
- pytest

## API Endpoints

### Register

POST `/api/auth/register`

### Login

POST `/api/auth/login`

### Current User / Session

GET `/api/auth/me`

### Logout

POST `/api/auth/logout`

### List Active Sessions

GET `/api/sessions`

### Revoke Session

DELETE `/api/sessions/<session_id>`

## Security Features

- Passwords are stored using secure password hashing.
- Authentication uses session tokens.
- Session tokens are stored in hashed form in the database.
- Session cookies are HttpOnly.
- Session cookies use SameSite=Strict.
- Sessions have an expiration time.
- Sessions can be revoked.
- Device information is collected from the User-Agent.
- Logout invalidates the current session.

## Testing

Run:

python -m pytest -q

Expected result:

4 passed

## Phase 1 Status

Phase 1 authentication and session management implementation is complete.
