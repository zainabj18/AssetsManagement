from datetime import datetime, timedelta
from app.db import UserRole, DataAccess
from app.schemas import AssetBaseInDB
from app.schemas.factories import TypeVersionFactory,TypeFactory
import jwt
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
    return create_assets(db_conn,request.param["batch_size"],request.param.get("add_to_db"))
    

@pytest.fixture(params=[
        {"size":1,"add_to_db": False}
    ])
def type_verions(db_conn,request):
    batch_size=request.param["size"]
    added_versions=[]
    new_type=TypeFactory.build(type_id=1)
    verion_ids=set()
    batch_size_counter=batch_size
    while len(added_versions)<batch_size:
        batch_result = TypeVersionFactory.batch(size=batch_size_counter,type_id=1) 
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
                    VALUES (%(version_id)s,%(version_number)s,%(type_id)s);""",
                                type_version.dict(),
                            )