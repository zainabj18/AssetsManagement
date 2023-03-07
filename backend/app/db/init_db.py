import os
import json
import click
from psycopg.rows import class_row
from app.db import close_db, get_db
from flask import current_app
from werkzeug.security import generate_password_hash
from app.schemas.factories import AssetFactory,TypeVersionFactory,ProjectFactory,TagFactory,TypeFactory
from app.schemas import AssetBaseInDB
def init_db():
    db = get_db(new=True)
    absolute_path = os.path.dirname(__file__)
    relative_path = "schema.sql"
    full_path = os.path.join(absolute_path, relative_path)
    with db.connection() as conn:
        with open(full_path) as f:
            conn.execute(f.read())
        conn.execute(
            """
        INSERT INTO accounts (username, hashed_password, account_type,account_privileges)
VALUES (%(username)s,%(password)s,'ADMIN','CONFIDENTIAL');""",
            {
                "username": current_app.config["DEFAULT_SUPERUSER_USERNAME"],
                "password": generate_password_hash(
                    current_app.config["DEFAULT_SUPERUSER_USERNAME"]
                ),
            },
        )
    # closes db so when next need a new pool will be created to map enums
    close_db()

def create_assets(db_conn,batch_size=10,add_to_db=False):
    batch_result = AssetFactory.batch(size=batch_size)
    added_assets=[]
    existing_version_ids=set()
    with db_conn.cursor() as cur:
        for asset in batch_result:
            attribute_ids = []
            if asset.version_id in existing_version_ids:
                continue
            existing_version_ids.add(asset.version_id)
            new_type_version = TypeVersionFactory.build(version_id=asset.version_id) 
            new_type=TypeFactory.build(type_id=new_type_version.type_id)
            # check if type already exists with id
            cur.execute(
                """SELECT * FROM types WHERE type_id=%(type_id)s;""",
                new_type.dict(),
                )
            # if no type already exists
            if cur.fetchall() == []:
                cur.execute(
                    """
            INSERT INTO types (type_id,type_name)
        VALUES (%(type_id)s,%(type_name)s) ON CONFLICT (type_name) DO NOTHING;""",
                    new_type.dict(),
                )
            cur.execute(
                    """
            INSERT INTO type_version (version_id,version_number,type_id)
        VALUES (%(version_id)s,%(version_number)s,%(type_id)s);""",
                    new_type_version.dict(),
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
        INSERT INTO attributes_in_types (attribute_id,type_version)
    VALUES (%(attribute_id)s,%(type_version)s) ON CONFLICT (attribute_id,type_version) DO NOTHING;""",
                    {"attribute_id": id, "type_version": asset.version_id},
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
                for asset in batch_result:
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



@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database intialised.")


@click.command("build-assets")
@click.option('--size', default=100)
def build_assets_command(size):
    db = get_db()
    with db.connection() as conn:
        create_assets(db_conn=conn,batch_size=size,add_to_db=True)
    click.echo("Added assets")