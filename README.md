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