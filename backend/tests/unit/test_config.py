from app import create_app
from app.core.config import Base
import os

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