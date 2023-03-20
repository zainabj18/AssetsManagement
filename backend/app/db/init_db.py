import os
import json
import click
from psycopg.rows import class_row,dict_row
from app.db import close_db, get_db,Models,UserRole,DataAccess
from flask import current_app
from werkzeug.security import generate_password_hash
from app.schemas.factories import AssetFactory,TypeVersionFactory,ProjectFactory,TagFactory,TypeFactory
from app.schemas import AssetOut
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
VALUES (%(username)s,%(password)s,%(account_type)s,%(account_privileges)s);""",
            {
                "username": current_app.config["DEFAULT_SUPERUSER_USERNAME"],
                "password": generate_password_hash(
                    current_app.config["DEFAULT_SUPERUSER_USERNAME"]
                ),
                "account_type":max(UserRole),
                "account_privileges":max(DataAccess)

            },
        )
        for model in Models:
            conn.execute(
                """
            INSERT INTO tracked_models(model_id,model_name)
    VALUES (%(model_id)s,%(model_name)s);""",
                {
                    "model_id":model.value,
                    "model_name":model.name.lower(),
                },
            )
    #closes db so when next need a new pool will be created to map enums
    close_db()

def generate_assets(existing_version_ids,db_conn,batch_result,added_assets):
       with db_conn.cursor() as cur:
        for asset in batch_result:

            attribute_ids = []
            cur.execute(
                """SELECT * FROM type_version WHERE version_id=%(version_id)s;""",
                {"version_id":asset.version_id},
                )
            # if no type_version already exists
            if cur.fetchall() != []:
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
            if cur.fetchall() != []:
                continue
            cur.execute(
                """
        INSERT INTO types (type_id,type_name)
    VALUES (%(type_id)s,%(type_name)s) ON CONFLICT (type_name) DO NOTHING;""",
                new_type.dict(),
            )
            cur.execute(
                """SELECT version_id FROM type_version;""",
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
                print("hello",type(attribute))
                db_attribute["validation_data"] = json.dumps(attribute.validation_data)
                cur.execute(
                    """
        INSERT INTO attributes (attribute_name,attribute_data_type,validation_data)
    VALUES (%(attribute_name)s,%(attribute_data_type)s,%(validation_data)s) ON CONFLICT (attribute_name) DO UPDATE
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
            added_assets.append(asset)
            db_conn.commit()

def create_assets(db_conn,batch_size=10,add_to_db=False):
    added_assets=[]
    existing_version_ids=set()
    batch_size_counter=batch_size
    while len(added_assets)<batch_size:
        batch_result = AssetFactory.batch(size=batch_size_counter)
        generate_assets(existing_version_ids,db_conn,batch_result,added_assets)
        batch_size_counter=batch_size-len(added_assets)
    if (add_to_db):
        with db_conn.cursor() as cur:
            for asset in added_assets:
                cur.execute(
                    """
                INSERT INTO assets (name,link,version_id,description, classification)
        VALUES (%(name)s,%(link)s,%(version_id)s,%(description)s,%(classification)s) RETURNING asset_id;""",
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
                    INSERT INTO attributes_values (asset_id,attribute_id,attribute_value)
            VALUES (%(asset_id)s,%(attribute_id)s,%(value)s);""",
                        {
                            "asset_id": asset_id,
                            "attribute_id": attribute.attribute_id,
                            "value": attribute.attribute_value,
                        },
                    )
                db_conn.commit()
    
 
    if (add_to_db):
        with db_conn.cursor(row_factory=class_row(AssetOut)) as cur:
            cur.execute("""WITH combined_attributes AS (
SELECT attributes_values.asset_id,attributes_values.attribute_value,attributes.* FROM attributes_values
INNER JOIN attributes ON attributes.attribute_id=attributes_values.attribute_id)
SELECT *,
ARRAY(SELECT tag_id FROM assets_in_tags WHERE assets_in_tags.asset_id=assets.asset_id) as tags,
ARRAY(SELECT project_id FROM assets_in_projects WHERE assets_in_projects.asset_id=assets.asset_id) as projects,
(SELECT json_agg(row_to_json(combined_attributes)) FROM combined_attributes
INNER JOIN attributes on attributes.attribute_id=combined_attributes.attribute_id WHERE asset_id=assets.asset_id) as metadata
FROM assets;""")
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