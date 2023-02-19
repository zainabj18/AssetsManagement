import json
from datetime import datetime, timedelta
from app.db import UserRole, DataAccess
from app.schemas import AssetBaseInDB
import jwt
import pytest
from app import create_app
from app.db import get_db, init_db
from flask import current_app
from psycopg.rows import class_row
from .factories import (
    AssetFactory,
    AttributeFactory,
    ProjectFactory,
    TagFactory,
    TypeFactory,
)


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


@pytest.fixture(
    params=[
        {"account_type": UserRole.ADMIN, "account_privileges": DataAccess.CONFIDENTIAL}
    ]
)
def valid_client(flask_app, request):
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
    client = flask_app.test_client()
    client.set_cookie("localhost", "access-token", token)
    yield client
    client.set_cookie("localhost", "access-token", "", expires=0)


@pytest.fixture()
def expected_res(request):
    return request.param


# creates a new asset object with supported db structure
@pytest.fixture(params=[
        {"batch_size":1,"add_to_db": False}
    ])
def new_assets(db_conn, request):
    batch_result = AssetFactory.batch(size=request.param["batch_size"])
    add_to_db=request.param.get("add_to_db")
    with db_conn.cursor() as cur:
        for asset in batch_result:
            attribute_ids = []
            new_type = TypeFactory.build(type_id=asset.type)
            cur.execute(
                """
        INSERT INTO types (type_id,type_name)
    VALUES (%(type_id)s,%(type_name)s) ON CONFLICT (type_id) DO NOTHING;""",
                new_type.dict(),
            )

            for attribute in asset.metadata:
                db_attribute = attribute.dict(exclude={"validation_data"})
                db_attribute["validation_data"] = json.dumps(attribute.validation_data)
                cur.execute(
                    """
        INSERT INTO attributes (attribute_name,attribute_data_type,validation_data)
    VALUES (%(attribute_name)s,%(attribute_type)s,%(validation_data)s) ON CONFLICT (attribute_name) DO UPDATE
  SET attribute_name = excluded.attribute_name RETURNING attribute_id;""",
                    db_attribute,
                )
                id = cur.fetchone()[0]
                attribute.attribute_id = id
                attribute_ids.append(id)
            for id in attribute_ids:
                cur.execute(
                    """
        INSERT INTO attributes_in_types (attribute_id,type_id)
    VALUES (%(attribute_id)s,%(type_id)s) ON CONFLICT (attribute_id,type_id) DO NOTHING;""",
                    {"attribute_id": id, "type_id": asset.type},
                )
            for project in asset.projects:
                p = ProjectFactory.build(id=project)
                cur.execute(
                    """
        INSERT INTO projects (id,name,description)
    VALUES (%(id)s,%(name)s,%(description)s) ON CONFLICT DO NOTHING;""",
                    p.dict(),
                )
            for tag in asset.tags:
                t = TagFactory.build(id=tag)
                cur.execute(
                """SELECT * FROM tags WHERE id=%(id)s;""",
                {"id": tag},
            )
                if cur.fetchall() == []:
                    cur.execute(
                        """
            INSERT INTO tags (id,name)
        VALUES (%(id)s,%(name)s) ON CONFLICT (name) DO UPDATE SET name = excluded.name;""",
                        t.dict(),
                    )
            db_conn.commit()
    
        if (add_to_db):
            with db_conn.cursor() as cur:
                cur.execute(
                    """
                INSERT INTO assets (name,link,type,description, classification)
        VALUES (%(name)s,%(link)s,%(type)s,%(description)s,%(classification)s) RETURNING asset_id;""",
                    asset.dict(),
                )
                asset_id = cur.fetchone()[0]
                for tag in asset.tags:
                    cur.execute(
                        """
                    INSERT INTO assets_in_tags (asset_id,tag_id)
            VALUES (%(asset_id)s,%(tag_id)s);""",
                        {"asset_id": asset_id, "tag_id": tag},
                    )
                # add asset to projects to db
                for project in asset.projects:
                    cur.execute(
                        """
                    INSERT INTO assets_in_projects (asset_id,project_id)
            VALUES (%(asset_id)s,%(project_id)s);""",
                        {"asset_id": asset_id, "project_id": project},
                    )
                # add attribute values to db
                for attribute in asset.metadata:
                    cur.execute(
                        """
                    INSERT INTO attributes_values (asset_id,attribute_id,value)
            VALUES (%(asset_id)s,%(attribute_id)s,%(value)s);""",
                        {
                            "asset_id": asset_id,
                            "attribute_id": attribute.attribute_id,
                            "value": attribute.attribute_value,
                        },
                    )
                db_conn.commit()
    if (add_to_db):
        with db_conn.cursor(row_factory=class_row(AssetBaseInDB)) as cur:
            cur.execute("""SELECT * FROM assets WHERE soft_delete=0;""")
            assets = cur.fetchall()
            return assets
    return batch_result
