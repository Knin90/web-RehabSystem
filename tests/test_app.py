# tests/test_app.py
"""Unit tests for RehabSystem Flask application.

Run with:
    pytest -q
"""
import pytest
from flask import url_for
from app import create_app, db
from app.models import User
from app.forms import LoginForm

def create_user(username, password, role='admin'):
    user = User(username=username, email=f'{username}@rehab.com', role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def test_create_app_initializes_extensions(app):
    """Case 1: ensure extensions are attached to the app."""
    # The extensions are imported in app/__init__.py and attached in create_app
    from app import login_manager
    assert "sqlalchemy" in app.extensions
    assert hasattr(app, "login_manager")
    assert app.login_manager is login_manager
    assert "migrate" in app.extensions

def test_successful_login_redirects_to_dashboard(client, app):
    """Case 2: correct credentials redirect to appropriate dashboard based on role."""
    # create a test user (admin role)
    with app.app_context():
        create_user('admin', 'admin123', role='admin')
    # post login form
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=False)
    # Should redirect (302) to dashboard route
    assert response.status_code == 302
    # Follow the redirect to ensure we land on admin dashboard
    follow = client.get(response.headers['Location'])
    assert b'Dashboard' in follow.data or b'admin' in follow.data

def test_failed_login_shows_error_message(client, app):
    """Case 3: incorrect credentials show flash error."""
    with app.app_context():
        create_user('patient', 'paci123', role='patient')
    response = client.post('/login', data={
        'username': 'patient',
        'password': 'wrongpass'
    }, follow_redirects=True)
    # Should stay on login page (200) and contain error flash text
    assert response.status_code == 200
    assert b'Credenciales incorrectas' in response.data

def test_role_required_decorator_blocks_unauthorized_access(client, app):
    """Case 4: role_required restricts access to unauthorized users."""
    # Create a patient user but try to access admin dashboard
    with app.app_context():
        create_user('patient', 'paci123', role='patient')
    # Log in as patient
    client.post('/login', data={'username': 'patient', 'password': 'paci123'}, follow_redirects=True)
    # Attempt to access admin dashboard directly
    response = client.get('/admin/dashboard', follow_redirects=False)
    # Should be redirected (302) to login
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_user_password_hashing_and_check():
    """Case 5: User.set_password hashes and check_password verifies."""
    user = User(username='testuser', email='test@rehab.com', role='patient')
    raw = 'mysecret'
    user.set_password(raw)
    # Ensure stored password is not the raw password
    assert user.password_hash != raw
    # Verify correct password returns True
    assert user.check_password('mysecret') is True
    # Incorrect password returns False
    assert user.check_password('wrong') is False
