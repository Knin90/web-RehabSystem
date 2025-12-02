from flask import url_for

from app import db, create_app, login_manager, bcrypt, migrate
from app.models import User


def test_create_app_initializes_extensions():
    """create_app should initialize all core Flask extensions."""
    app = create_app()

    assert app is not None
    # SQLAlchemy
    assert "sqlalchemy" in app.extensions
    # Flask-Migrate
    assert "migrate" in app.extensions
    # Login manager attached to app
    assert hasattr(app, "login_manager")
    assert app.login_manager is login_manager
    # Login view configured
    assert login_manager.login_view == "login"


def _create_user(username: str, role: str, password: str = "testpass") -> User:
    user = User(
        username=username,
        email=f"{username}@example.com",
        role=role,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def test_login_success_redirects_to_role_dashboard(app, client):
    """User with correct credentials is logged in and redirected based on role."""
    with app.app_context():
        _create_user("patient_user", "patient", "secret")
        _create_user("therapist_user", "therapist", "secret")
        _create_user("admin_user", "admin", "secret")

    test_cases = [
        ("patient_user", "patient", "/patient/dashboard"),
        ("therapist_user", "therapist", "/therapist/dashboard"),
        ("admin_user", "admin", "/admin/dashboard"),
    ]

    for username, _role, expected_path in test_cases:
        # Login
        response = client.post(
            "/login",
            data={"username": username, "password": "secret"},
            follow_redirects=False,
        )
        # First redirect should be to generic /dashboard
        assert response.status_code == 302
        assert "/dashboard" in response.headers["Location"]

        # Now hit /dashboard and ensure we are redirected to role-specific dashboard
        dash_response = client.get("/dashboard", follow_redirects=False)
        assert dash_response.status_code == 302
        assert dash_response.headers["Location"].endswith(expected_path)

        # Logout between iterations to reset session
        client.get("/logout", follow_redirects=False)


def test_login_fails_with_incorrect_credentials(app, client):
    """Login with wrong credentials should not authenticate and should show error message."""
    with app.app_context():
        _create_user("valid_user", "patient", "correct-password")

    # Wrong password
    response = client.post(
        "/login",
        data={"username": "valid_user", "password": "wrong-password"},
        follow_redirects=True,
    )

    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Credenciales incorrectas." in text

    # Non-existent user
    response = client.post(
        "/login",
        data={"username": "unknown", "password": "any"},
        follow_redirects=True,
    )
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Credenciales incorrectas." in text


def test_role_required_restricts_unauthorized_access(app, client):
    """role_required decorator should prevent users with the wrong role from accessing dashboards."""
    with app.app_context():
        # Create a therapist user
        _create_user("therapist_only", "therapist", "secret")

    # Log in as therapist
    login_response = client.post(
        "/login",
        data={"username": "therapist_only", "password": "secret"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    # Try to access patient dashboard with therapist role
    response = client.get("/patient/dashboard", follow_redirects=False)
    # Should be redirected (302) to login by role_required decorator
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_user_password_hashing_and_verification(app):
    """User.set_password should hash the password and check_password should verify it."""
    with app.app_context():
        user = User(username="hash_user", email="hash@example.com", role="patient")
        raw_password = "my-secret-password"

        user.set_password(raw_password)

        # Password should be hashed and not equal to the raw password
        assert user.password_hash != raw_password
        assert isinstance(user.password_hash, str)

        # Correct password validates
        assert user.check_password(raw_password) is True
        # Incorrect password fails
        assert user.check_password("wrong") is False
