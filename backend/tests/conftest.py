from app import create_app
from app.db import init_db,get_db
import pytest

@pytest.fixture
def flask_app():
    app=create_app()
    app.config['TESTING'] = True
    with app.app_context():
        init_db.init_db()
        yield app

@pytest.fixture()
def client(flask_app):
    yield flask_app.test_client()

@pytest.fixture()
def db_conn(flask_app):
    db_conn=get_db()
    with db_conn.connection() as conn:
        yield conn
