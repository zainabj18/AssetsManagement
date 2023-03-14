from datetime import datetime, timedelta
from app.db import UserRole, DataAccess
from app.schemas import AssetBaseInDB
from app.schemas.factories import TypeVersionFactory,TypeFactory,AttributeFactory
import jwt
import json
import pytest
from app import create_app
from app.db import get_db, init_db,create_assets
from flask import current_app

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
            "account_id": 1,
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
    return create_assets(db_conn,request.param["batch_size"],request.param.get("add_to_db"))
    

@pytest.fixture(params=[
        {"size":1,"add_to_db": False}
    ])
def type_verions(db_conn,request):
    batch_size=request.param["size"]
    added_versions=[]
    with db_conn.cursor() as cur:
        cur.execute(
                """SELECT type_id FROM types;""",
        )
        types_in_db=[row[0] for row in cur.fetchall()]
    if types_in_db !=[]:
        new_type_id=max(types_in_db)+1
    else:
        new_type_id=1
    new_type=TypeFactory.build(type_id=new_type_id,type_name=f'Test-{new_type_id}-{len(types_in_db)}')
    verion_ids=set()
    batch_size_counter=batch_size
    while len(added_versions)<batch_size:
        batch_result = TypeVersionFactory.batch(size=batch_size_counter,type_id=new_type_id) 
        for type_verion in batch_result:
            if type_verion.version_id not in verion_ids:
                verion_ids.add(type_verion.version_id)
                added_versions.append(type_verion)
        batch_size_counter=batch_size-len(added_versions)
    with db_conn.cursor() as cur:
      
        cur.execute(
                        """
                INSERT INTO types (type_id,type_name)
            VALUES (%(type_id)s,%(type_name)s) ON CONFLICT (type_name) DO NOTHING;""",
                        new_type.dict(),
                    )
        for type_version in added_versions:
            cur.execute(
                                """
                        INSERT INTO type_version (version_id,version_number,type_id)
                    VALUES (%(version_id)s,%(version_number)s,%(type_id)s) RETURNING version_id;""",
                                type_version.dict(),
                            )
            type_version.version_id=cur.fetchone()[0]
            attributes=AttributeFactory.batch(size=20)
            type_version.attributes=attributes
            attribute_ids=[]
            for attribute in attributes:
                attribute_in = attribute.dict(exclude={"validation_data"})
                attribute_in["validation_data"] = json.dumps(attribute.validation_data)
                cur.execute(
                    """
        INSERT INTO attributes (attribute_name,attribute_data_type,validation_data)
    VALUES (%(attribute_name)s,%(attribute_data_type)s,%(validation_data)s) ON CONFLICT (attribute_name) DO UPDATE
  SET attribute_name = excluded.attribute_name RETURNING attribute_id;""",
                    attribute_in,
                )
                id = cur.fetchone()[0]
                attribute.attribute_id=id
                attribute_ids.append(id)
            for id in attribute_ids:
                cur.execute(
                    """
        INSERT INTO attributes_in_types (attribute_id,type_version)
    VALUES (%(attribute_id)s,%(type_version)s) ON CONFLICT (attribute_id,type_version) DO NOTHING;""",
                    {"attribute_id": id, "type_version": type_version.version_id},
                )
        db_conn.commit()
        return (added_versions,new_type)