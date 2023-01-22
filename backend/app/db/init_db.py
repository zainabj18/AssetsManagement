import click
import os

from werkzeug.security import generate_password_hash
from app.db import get_db,close_db
from flask import current_app

def init_db():
    db = get_db()
    absolute_path = os.path.dirname(__file__)
    relative_path = "schema.sql"
    full_path = os.path.join(absolute_path, relative_path)
    with db.connection() as conn:
        with open(full_path) as f:
            conn.execute(f.read())
        conn.execute("""
        INSERT INTO accounts (username, hashed_password, account_type,account_privileges)
VALUES (%(username)s,%(password)s,'ADMIN','CONFIDENTIAL');""",{'username':current_app.config['DEFAULT_SUPERUSER_USERNAME'], 'password':generate_password_hash(current_app.config['DEFAULT_SUPERUSER_USERNAME'])})
    # closes db so when next need a new pool will be created to map enums
    close_db()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Databse intialised.')
