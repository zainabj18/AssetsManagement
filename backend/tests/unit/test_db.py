from app.db import db
from app import create_app
from psycopg_pool import ConnectionPool
from flask import g

def test_base_config():
    flask_app=create_app()
    with flask_app.app_context():
        db_conn=db.get_db()
        assert isinstance(db_conn,ConnectionPool)
        assert g.db==db_conn
        assert db_conn.closed == False