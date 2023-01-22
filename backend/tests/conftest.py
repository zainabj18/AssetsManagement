from app import create_app
import pytest

@pytest.fixture
def flask_app():
    app=create_app()
    app.config['TESTING'] = True
    yield app