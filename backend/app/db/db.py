from flask import current_app, g
from psycopg_pool import ConnectionPool
from psycopg.types.enum import EnumInfo, register_enum
from enum import Enum,auto
class UserRole(Enum):
    VIEWER = "VIEWER"
    USER = "USER"
    ADMIN = "ADMIN"

class DataAccess(Enum):
    PUBLIC = auto()
    INTERNAL = auto()
    RESTRICTED = auto()
    CONFIDENTIAL = auto()
def custom_pool_config(conn):
    register_enum(EnumInfo.fetch(conn, "account_role"), conn, UserRole)
    register_enum(EnumInfo.fetch(conn, "data_classification"), conn, DataAccess)
    return conn

def get_db():
    if 'db' not in g:
        pool = ConnectionPool(current_app.config['POSTGRES_DATABASE_URI'],configure=custom_pool_config)
        pool.open()
        g.db = pool
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
