# Team Project

This repository has been created to store your Team Project.

You may edit it as you like, but please do not remove the default topics or the project members list. These need to stay as currently defined in order for your lecturer to be able to find and mark your work.


Backend Flask,Psycopg for connecting to db /backend/app/
-/app/__init__.py creates the flask app and registers custom commands and config

-/api holds all the endpoints that are registered e.g. /api/v1/auth/login all blueprints are added to this blueprint which is then added to the main blueprint defined in /backend/app/__init__.py

-/asset holds all the endpoints that relates to assets including supporting SQL

-/auth holds all the endpoints that relates to auth including supporting SQL

-/core holds all functions used throughout modules including config and protected route decorator

-/db holds all functions for connecting to db and enum mappings to db enums and schema.sql

-/project holds all the endpoints that relates to project including supporting SQL

-/schemas holds all pydantic models used to validating request jsons and mappings to db rows

-/tag holds all the endpoints that relates to tags including supporting SQL

-/type holds all the endpoints that relates to types including supporting SQL

-/test holds all the tests


Frontend React 
/src

-/componets hold all resuable components to crate the web pages

-/hooks hold all the custom hooks

-/routes hold all the pages

-/theme hold all the addtional styling ontop of chakra

-/App.js holds all the routes


To run install docker and docker compose

Then to run app

docker compose  up --build 

To init db

docker exec backend python -m flask init-db

Go to http://localhost:3000

To run the tests

docker exec backend python -m pytest --reruns 5 --reruns-delay 1


OR

Download postgres and run /db/init.sql to create the users and db


Example .env to be added to the backend folder

DEV_POSTGRES_HOST="localhost"
DEV_POSTGRES_USER="dbmanager"
DEV_POSTGRES_PASSWORD="dbmanager"
DEV_POSTGRES_DB="assets"
DEV_DEBUG=true
DEV_SECRET_KEY="TOJAZMiFQOq1PIoImUaltg"
PROD_POSTGRES_HOST="localhost"
PROD_POSTGRES_USER="dbmanager"
PROD_POSTGRES_PASSWORD="dbmanager"
PROD_POSTGRES_DB="assets"

