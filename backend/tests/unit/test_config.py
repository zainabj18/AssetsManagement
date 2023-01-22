from app import create_app
from app.core.config import Base,DevelopmentConfig,ProductionConfig,TestingConfig
from unittest import mock
from pydantic.error_wrappers import ValidationError
import os
import pytest

def test_base_config():
    flask_app=create_app(Base())
    assert flask_app.config["APPLICATION_NAME"]=="Asset Repository"
    assert flask_app.config["APPLICATION_PORT"]==5050
    assert flask_app.config["API_VERSION"]=="v1"
    assert flask_app.config["APPLICATION_ROOT_URL"]=="/api/v1"
    assert flask_app.config["DEBUG"]==False

def test_base_config_read_env():
    absolute_path = os.path.dirname(__file__)
    relative_path = "test.env"
    full_path = os.path.join(absolute_path, relative_path)
    flask_app=create_app(Base(_env_file=full_path, _env_file_encoding='utf-8'))
    assert flask_app.config["APPLICATION_NAME"]=="Test"

@mock.patch.dict(os.environ, {"POSTGRES_DATABASE_URI": "hello"})
def test_db_uri_format():
    with pytest.raises(ValidationError):
        create_app(Base())

@mock.patch.dict(os.environ, {"POSTGRES_HOST":"testing","POSTGRES_USER":"test","POSTGRES_PASSWORD":"test","POSTGRES_DB":"test"},clear=True)
def test_db_uri_build():
    flask_app=create_app(Base())
    assert flask_app.config["POSTGRES_DATABASE_URI"]=="postgresql://test:test@testing:5432/test"

def test_development_config():
    flask_app=create_app(DevelopmentConfig())
    assert flask_app.config["DEBUG"]==True
    assert flask_app.config["ENV"]=="development"
    
def test_production():
    flask_app=create_app(ProductionConfig())
    assert flask_app.config["DEBUG"]==False
    assert flask_app.config["ENV"]=="production"

def test_default_superuser_in_base_config():
    flask_app=create_app(Base())
    assert flask_app.config["DEFAULT_SUPERUSER_USERNAME"]==os.environ.get("DEFAULT_SUPERUSER_USERNAME")
    assert flask_app.config["DEFAULT_SUPERUSER_PASSWORD"]==os.environ.get("DEFAULT_SUPERUSER_PASSWORD")

def test_test_config():
    flask_app=create_app(TestingConfig())
    assert flask_app.config["DEBUG"]==True
    assert flask_app.config["ENV"]=="test"