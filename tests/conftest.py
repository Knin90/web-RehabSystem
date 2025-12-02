import pytest

from app import create_app, db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()

    # Use an in-memory database and disable CSRF for easier form testing
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()
