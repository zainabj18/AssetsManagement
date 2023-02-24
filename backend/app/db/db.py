from flask import current_app, g
from psycopg_pool import ConnectionPool
from psycopg.types.enum import EnumInfo, register_enum
from enum import Enum
from functools import total_ordering

@total_ordering
class UserRole(Enum):
    VIEWER = "VIEWER",1
    USER = "USER",2
    ADMIN = "ADMIN",3
    
    def __new__(cls, value, permission_level):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.permission_level = permission_level
        return obj
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.permission_level < other.permission_level
        return NotImplemented

class DataAccess(Enum):
    PUBLIC = "PUBLIC",1
    INTERNAL = "INTERNAL",2
    RESTRICTED = "RESTRICTED",3
    CONFIDENTIAL = "CONFIDENTIAL",4

    def __new__(cls, value, permission_level):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.permission_level = permission_level
        return obj
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.permission_level < other.permission_level
        return NotImplemented

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

        class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'username': self.username,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }
