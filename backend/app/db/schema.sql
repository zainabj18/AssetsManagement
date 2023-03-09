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
    version_id INTEGER,
    description VARCHAR NOT NULL,
	classification data_classification NOT NULL DEFAULT 'PUBLIC',
	created_at timestamp NOT NULL DEFAULT now(),
	last_modified_at timestamp NOT NULL DEFAULT now(),
	soft_delete INTEGER DEFAULT 0,
	FOREIGN KEY (version_id) REFERENCES type_version(version_id),
	PRIMARY KEY (asset_id)
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
	value VARCHAR,
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

 INSERT INTO tracked_models(model_id,model_name) 
 VALUES
 (1,'assets'),
 (2,'projects'),
 (3,'type'),
 (4,'tags'),
 (5,'accounts');