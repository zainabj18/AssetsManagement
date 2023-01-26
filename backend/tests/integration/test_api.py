import json
import os

from app import create_app


def test_api_returns_json():
    flask_app = create_app()
    response = flask_app.test_client().get(os.environ["APPLICATION_ROOT_URL"] + "/")
    assert response.status_code == 200
    data_decoded = response.data.decode("utf-8")
    assert json.loads(data_decoded) == {
        "msg": "Hello World!",
        "url": os.environ["APPLICATION_ROOT_URL"],
        "version": os.environ["API_VERSION"],
    }
