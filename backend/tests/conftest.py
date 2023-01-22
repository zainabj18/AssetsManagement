from app import create_app
import pytest

@pytest.fixture
def flask_app():
    app=create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture()
def client(flask_app):
    yield flask_app.test_client()