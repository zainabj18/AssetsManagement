from flask import current_app, g
from psycopg_pool import ConnectionPool


def get_db():
    if 'db' not in g:
        pool = ConnectionPool(current_app.config['POSTGRES_DATABASE_URI'])
        pool.open()
        g.db = pool
    return g.db
