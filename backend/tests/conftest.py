from app import create_app
from app.db import init_db
import pytest

@pytest.fixture
def flask_app():
    app=create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture()
def client(flask_app):
    with flask_app.app_context():
        init_db.init_db()
    yield flask_app.test_client()