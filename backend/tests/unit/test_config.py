from app import create_app
from app.core.config import Base

def test_base_config():
    flask_app=create_app(Base())
    assert flask_app.config["APPLICATION_NAME"]=="Asset Repository"
    assert flask_app.config["APPLICATION_PORT"]==5050
    assert flask_app.config["API_VERSION"]=="v1"
    assert flask_app.config["APPLICATION_ROOT_URL"]=="/api/v1"
    assert flask_app.config["DEBUG"]==False