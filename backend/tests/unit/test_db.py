from flask import g
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from werkzeug.security import check_password_hash

from app.db import DataAccess, UserRole, get_db, init_db


def test_db_connection(flask_app):
    with flask_app.app_context():
        db_conn = get_db()
        assert isinstance(db_conn, ConnectionPool)
        assert g.db == db_conn
        assert db_conn.closed == False


def test_db_connection_close(flask_app):
    with flask_app.app_context():
        db_conn = get_db()
    assert db_conn.closed == True


def test_db_init(flask_app):
    with flask_app.app_context():
        init_db.init_db()
        db_conn = get_db()
        with db_conn.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """SELECT * FROM accounts WHERE username=%(username)s;""",
                    {"username": flask_app.config["DEFAULT_SUPERUSER_USERNAME"]},
                )
                superuser = cur.fetchone()
                assert superuser["account_id"] == 1
                assert (
                    superuser["username"]
                    == flask_app.config["DEFAULT_SUPERUSER_USERNAME"]
                )
                assert check_password_hash(
                    superuser["hashed_password"],
                    flask_app.config["DEFAULT_SUPERUSER_USERNAME"],
                )
                assert superuser["account_type"] == UserRole.ADMIN
                assert superuser["account_privileges"] == DataAccess.CONFIDENTIAL


def test_connection_map_enums(flask_app):
    with flask_app.app_context():
        init_db.init_db()
        db_conn = get_db()
        with db_conn.connection() as conn:
            user_roles = [role for role in UserRole]
            user_roles_sql_select = conn.execute("SELECT %s;", (user_roles,)).fetchone()
            assert user_roles_sql_select[0] == user_roles
            data_acess_classifications = [priv for priv in DataAccess]
            data_acess_classifications_sql_select = conn.execute(
                "SELECT %s;", (data_acess_classifications,)
            ).fetchone()
            assert (
                data_acess_classifications_sql_select[0] == data_acess_classifications
            )
