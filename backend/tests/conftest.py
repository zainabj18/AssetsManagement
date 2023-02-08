from datetime import datetime, timedelta
import json
import jwt
import pytest
from flask import current_app

from app import create_app
from app.db import get_db, init_db
from .factories import AttributeFactory,TagFactory,AssetFactory,ProjectFactory,TypeFactory

@pytest.fixture
def flask_app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        init_db.init_db()
        yield app


@pytest.fixture()
def client(flask_app):
    yield flask_app.test_client()


@pytest.fixture()
def db_conn(flask_app):
    db_conn = get_db()
    with db_conn.connection() as conn:
        yield conn


@pytest.fixture()
def valid_token(request):
    token = jwt.encode(
        {
            "account_id": None,
            "account_type": request.param["account_type"].value,
            "account_privileges": request.param["account_privileges"].value,
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGO"],
    )
    return token


@pytest.fixture()
def valid_client(flask_app):
    token = jwt.encode(
        {
            "account_id": None,
            "account_type": "ADMIN",
            "account_privileges": "CONFIDENTIAL",
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        current_app.config["SECRET_KEY"],
        algorithm=current_app.config["JWT_ALGO"],
    )
    client = flask_app.test_client()
    client.set_cookie("localhost", "access-token", token)
    yield client


@pytest.fixture()
def expected_res(request):
    return request.param

@pytest.fixture()
def new_asset(db_conn):
    asset = AssetFactory.build()
    attribute_ids=[]
    with db_conn.cursor() as cur:
        new_type=TypeFactory.build(type_id=asset.type)
        cur.execute(
                """
    INSERT INTO types (type_id,type_name)
VALUES (%(type_id)s,%(type_name)s);""",
                new_type.dict(),
            )

        for attribute in asset.metadata:
            db_attribute = attribute.dict(exclude={"validation_data"})
            db_attribute["validation_data"] = json.dumps(attribute.validation_data)
            cur.execute(
                """
    INSERT INTO attributes (attribute_name,attribute_data_type,validation_data)
VALUES (%(attribute_name)s,%(attribute_type)s,%(validation_data)s) RETURNING attribute_id;""",
                db_attribute,
            )
            id = cur.fetchone()[0]
            attribute_ids.append(id)
        for id in attribute_ids:
            cur.execute(
                """
    INSERT INTO attributes_in_types (attribute_id,type_id)
VALUES (%(attribute_id)s,%(type_id)s) RETURNING attribute_id;""",
                {"attribute_id":id,"type_id":asset.type},
            )
        for project in asset.projects:
            p=ProjectFactory.build(id=project)
            cur.execute(
                """
    INSERT INTO projects (id,name,description)
VALUES (%(id)s,%(name)s,%(description)s);""",
                p.dict(),
            )
        for tag in asset.tags:
            t=TagFactory.build(id=tag)
            cur.execute(
                """
    INSERT INTO tags (id,name)
VALUES (%(id)s,%(name)s);""",
                t.dict(),
            )
        
        db_conn.commit()
    return asset
