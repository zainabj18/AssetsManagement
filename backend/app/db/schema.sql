DROP TYPE IF EXISTS account_role CASCADE;
DROP TYPE IF EXISTS data_classification CASCADE;
DROP TYPE IF EXISTS actions CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS assets CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS types CASCADE;
DROP TABLE IF EXISTS attributes CASCADE;
DROP TABLE IF EXISTS types CASCADE;
DROP TABLE IF EXISTS attributes_in_types CASCADE;
DROP TABLE IF EXISTS assets_in_tags CASCADE;
DROP TABLE IF EXISTS assets_in_projects CASCADE;
DROP TABLE IF EXISTS attributes_values CASCADE;
DROP TABLE IF EXISTS people_in_projects CASCADE;
DROP TABLE IF EXISTS asset_logs CASCADE;
DROP TABLE IF EXISTS assets_in_assets CASCADE;
DROP TABLE IF EXISTS type_version_link CASCADE;
DROP TABLE IF EXISTS type_version CASCADE;
DROP TABLE IF EXISTS tracked_models CASCADE;
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS comments CASCADE;

CREATE TYPE actions AS ENUM ('ADD', 'CHANGE', 'DELETE');
CREATE TYPE account_role AS ENUM ('VIEWER', 'USER', 'ADMIN');
CREATE TYPE data_classification AS ENUM ('PUBLIC', 'INTERNAL','RESTRICTED','CONFIDENTIAL');

CREATE TABLE accounts
(
	account_id SERIAL,
	first_name VARCHAR,
	last_name VARCHAR,
	username VARCHAR NOT NULL UNIQUE,
	hashed_password VARCHAR NOT NULL,
	account_type account_role NOT NULL DEFAULT 'VIEWER',
	account_privileges data_classification NOT NULL DEFAULT 'PUBLIC',
	PRIMARY KEY (account_id)
);

CREATE TABLE tags
(
	id SERIAL,
	name VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY (id)
);

CREATE TABLE projects
(
	id SERIAL,
	name VARCHAR NOT NULL UNIQUE,
	description VARCHAR,
	PRIMARY KEY (id)
);

CREATE TABLE attributes
(
	attribute_id SERIAL,
	attribute_name VARCHAR NOT NULL UNIQUE,
	attribute_data_type VARCHAR NOT NULL,
	validation_data JSON,
	PRIMARY KEY (attribute_id)
);

 CREATE TABLE types
 (
 	type_id SERIAL,
 	type_name VARCHAR NOT NULL UNIQUE,
 	PRIMARY KEY (type_id)
 );

 CREATE TABLE type_version
(
	version_id SERIAL,
	version_number INTEGER NOT NULL,
	type_id INTEGER,

	PRIMARY KEY (version_id),
	FOREIGN KEY (type_id) REFERENCES types(type_id)
);

 CREATE TABLE attributes_in_types
 (
 	attribute_id INTEGER,
 	type_version INTEGER,
 	PRIMARY KEY (attribute_id, type_version),
 	FOREIGN KEY (attribute_id) REFERENCES attributes(attribute_id),
 	FOREIGN KEY (type_version) REFERENCES type_version(version_id)
 );
 
 CREATE TABLE assets
(
	asset_id SERIAL,
	name VARCHAR NOT NULL UNIQUE,
	link VARCHAR NOT NULL,
    version_id INTEGER NOT NULL,
    description VARCHAR NOT NULL,
	classification data_classification NOT NULL DEFAULT 'PUBLIC',
	created_at timestamp NOT NULL DEFAULT now(),
	last_modified_at timestamp NOT NULL DEFAULT now(),
	soft_delete INTEGER DEFAULT 0,
	FOREIGN KEY (version_id) REFERENCES type_version(version_id),
	PRIMARY KEY (asset_id)
);

 
 CREATE TABLE comments
(
	comment_id SERIAL,
	asset_id INTEGER NOT NULL,
	account_id INTEGER NOT NULL,
	comment VARCHAR NOT NULL,
	datetime timestamp NOT NULL DEFAULT now(),
	FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id),
	PRIMARY KEY (comment_id)
);

 CREATE TABLE assets_in_tags
(
	asset_id SERIAL,
	tag_id SERIAL,
	FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
	FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
	PRIMARY KEY (asset_id,tag_id)
);

 CREATE TABLE assets_in_projects
(
	asset_id INTEGER,
	project_id INTEGER,
	FOREIGN KEY (project_id) REFERENCES projects(id),
	FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
	PRIMARY KEY (asset_id,project_id)
);

CREATE TABLE attributes_values
 (
 	attribute_id INTEGER,
 	asset_id INTEGER,
	attribute_value VARCHAR,
 	PRIMARY KEY (attribute_id, asset_id),
	FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
 	FOREIGN KEY (attribute_id) REFERENCES attributes(attribute_id)
 );

CREATE TABLE asset_logs
 (
 	log_id SERIAL,
	account_id INTEGER,
 	asset_id INTEGER,
	diff JSON,
	date timestamp NOT NULL DEFAULT now(),
 	PRIMARY KEY (log_id),
	FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id)
 );


 CREATE TABLE type_version_link
 (
	type_version_from INTEGER,
	type_version_to INTEGER,
	FOREIGN KEY (type_version_from) REFERENCES type_version(version_id),
	FOREIGN KEY (type_version_to) REFERENCES type_version(version_id),
	PRIMARY KEY (type_version_from, type_version_to)
 );

CREATE TABLE people_in_projects
(
	project_id INTEGER,
	account_id INTEGER,

	PRIMARY KEY (project_id, account_id),
	FOREIGN KEY (project_id) REFERENCES projects(id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

 CREATE TABLE assets_in_assets
(
	from_asset_id INTEGER,
	to_asset_id INTEGER,
	FOREIGN KEY (from_asset_id) REFERENCES assets(asset_id),
	FOREIGN KEY (to_asset_id) REFERENCES assets(asset_id),
	PRIMARY KEY (from_asset_id,to_asset_id)
);

 CREATE TABLE tracked_models(
	model_id SERIAL,
	model_name VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY (model_id)
);

CREATE TABLE audit_logs
 (
 	log_id SERIAL,
	account_id INTEGER,
	object_id INTEGER,
 	model_id INTEGER,
	action actions,
	diff JSON,
	date timestamp NOT NULL DEFAULT now(),
 	PRIMARY KEY (log_id),
	FOREIGN KEY (model_id) REFERENCES tracked_models(model_id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id)
 );
--VIEWS 
DROP VIEW IF EXISTS flatten_assets;
DROP VIEW IF EXISTS combined_attributes;
DROP VIEW IF EXISTS assets_projects;
DROP VIEW IF EXISTS assets_tags;
DROP VIEW IF EXISTS assets_assets;
DROP VIEW IF EXISTS type_names_versions;
DROP VIEW IF EXISTS all_atributes;

CREATE or REPLACE view all_atributes as
SELECT asset_id,
   unnest(array[-1,-2,-3]) AS "attribute_id",
   unnest(array[name, link, description]) AS "values"
FROM assets
UNION ALL 
SELECT * FROM attributes_values;

CREATE or REPLACE VIEW combined_attributes AS
SELECT attributes_values.asset_id,attributes_values.attribute_value,attributes.* FROM attributes_values
INNER JOIN attributes ON attributes.attribute_id=attributes_values.attribute_id;

CREATE or REPLACE VIEW assets_projects AS
SELECT projects.*,assets_in_projects.asset_id FROM assets_in_projects
INNER JOIN projects on projects.id=assets_in_projects.project_id;

CREATE or REPLACE VIEW assets_tags AS
SELECT tags.id,name,assets_in_tags.asset_id FROM assets_in_tags 
INNER JOIN tags on tags.id=assets_in_tags.tag_id;

CREATE or REPLACE VIEW assets_assets AS
SELECT assets.asset_id,assets_in_assets.from_asset_id FROM assets_in_assets
INNER JOIN assets on assets.asset_id=assets_in_assets.to_asset_id;

CREATE or REPLACE VIEW type_names_versions AS
SELECT CONCAT(type_name,'-',version_number) AS type_name,type_version.* FROM type_version
INNER JOIN types ON types.type_id=type_version.type_id;


CREATE or REPLACE VIEW flatten_assets AS(
SELECT assets.*,type_names_versions.type_name,
(SELECT COALESCE(json_agg(row_to_json(assets_tags)),'[]'::json) FROM assets_tags WHERE assets_tags.asset_id=assets.asset_id) as tags,
(SELECT COALESCE(json_agg(row_to_json(assets_projects)),'[]'::json) FROM assets_projects WHERE assets_projects.asset_id=assets.asset_id) as projects,
(SELECT COALESCE(json_agg(row_to_json(assets_assets)),'[]'::json) FROM assets_assets WHERE assets_assets.from_asset_id=assets.asset_id) as assets,
(SELECT COALESCE(json_agg(row_to_json(combined_attributes)),'[]'::json)  FROM combined_attributes WHERE asset_id=assets.asset_id) AS metadata
FROM assets
INNER JOIN type_names_versions ON type_names_versions.version_id=assets.version_id);