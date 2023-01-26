DROP TYPE IF EXISTS account_role CASCADE;
DROP TYPE IF EXISTS data_classification CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS assets CASCADE;
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

CREATE TABLE assets
(
	asset_id SERIAL,
	name VARCHAR NOT NULL UNIQUE,
	link VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    tags VARCHAR ARRAY,
	access_level data_classification NOT NULL DEFAULT 'PUBLIC',
    metadata JSON ARRAY,
	created_at timestamp NOT NULL DEFAULT now(),
	last_modified_at timestamp NOT NULL DEFAULT now(),
	project VARCHAR NOT NULL,
	PRIMARY KEY (asset_id)
);