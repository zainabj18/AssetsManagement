DROP TYPE IF EXISTS account_role CASCADE;
DROP TYPE IF EXISTS data_classification CASCADE;
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
	name VARCHAR NOT NULL,
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

 CREATE TABLE attributes_in_types
 (
 	attribute_id INTEGER,
 	type_id INTEGER,
 	PRIMARY KEY (attribute_id, type_id),
 	FOREIGN KEY (attribute_id) REFERENCES attributes(attribute_id),
 	FOREIGN KEY (type_id) REFERENCES types(type_id)
 );
 
 CREATE TABLE assets
(
	asset_id SERIAL,
	name VARCHAR NOT NULL UNIQUE,
	link VARCHAR NOT NULL,
    type INTEGER,
    description VARCHAR NOT NULL,
	classification data_classification NOT NULL DEFAULT 'PUBLIC',
	created_at timestamp NOT NULL DEFAULT now(),
	last_modified_at timestamp NOT NULL DEFAULT now(),
	soft_delete INTEGER DEFAULT 0,
	FOREIGN KEY (type) REFERENCES types(type_id),
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


-- CREATE TABLE assets
-- (
-- 	asset_id SERIAL,
-- 	asset_name VARCHAR NOT NULL,
-- 	link VARCHAR NOT NULL,
-- 	creation_date date NOT NULL,
-- 	acess_level INT NOT NULL,
-- 	project_id BIGINT UNSIGNED,
	
-- 	PRIMARY KEY (asset_id),
-- 	FOREIGN KEY project_id REFERENCES projects(project_id)
-- );


CREATE TABLE people_in_projects
(
	project_id INTEGER,
	account_id INTEGER,

	PRIMARY KEY (project_id, account_id),
	FOREIGN KEY (project_id) REFERENCES projects(id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);


-- CREATE TABLE change_logs
-- (
-- 	log_id SERIAL,
-- 	date date NOT NULL,
-- 	action VARCHAR, /*the system's comment*/
-- 	comment VARCHAR, /*the user's comment*/
-- 	asset_id BIGINT UNSIGNED NOT NULL,
	
-- 	PRIMARY KEY log_id,
-- 	FOREIGN KEY asset_id REFERENCES assets(asset_id)
-- );

-- CREATE TABLE type
-- (
-- 	type_id SERIAL,
-- 	type_name VARCHAR NOT NULL,
	
-- 	PRIMARY KEY (type_id)
-- );

-- CREATE TABLE types_in_assets
-- (
-- 	asset_id BIGINT UNSIGNED,
-- 	type_id BIGINT UNSIGNED,
	
-- 	PRIMARY KEY (asset_id, type_id),
-- 	FOREIGN KEY asset_id REFERENCES assets(asset_id),
-- 	FOREIGN KEY type_id REFERENCES types(type_id)
-- );

-- CREATE TABLE attributes
-- (
-- 	attribute_id SERIAL,
-- 	attribute_name VARCHAR NOT NULL,
-- 	attribute_dataType VARCHAR NOT NULL,
	
-- 	PRIMARY KEY (attribute_id)
-- );

-- CREATE TABLE attribute_values
-- (
-- 	attribute_id BIGINT UNSIGNED,
-- 	asset_id BIGINT UNSIGNED,
-- 	value VARCHAR,
	
-- 	PRIMARY KEY (attribute_id, asset_id),
-- 	FOREIGN KEY attribute_id REFERENCES attributes(attribute_id),
-- 	FOREIGN KEY asset_id REFERENCES assets(asset_id)
-- );

-- CREATE TABLE attributes_in_types
-- (
-- 	attribute_id BIGINT UNSIGNED,
-- 	type_id BIGINT UNSIGNED,
	
-- 	PRIMARY KEY (attribute_id, type_id),
-- 	FOREIGN KEY attribute_id REFERENCES attributes(attribute_id),
-- 	FOREIGN KEY type_id REFERENCES types(type_id)
-- );
