import pytest
from pydantic.error_wrappers import ValidationError

from app.schemas import UserCreate


def test_user_create_requires_same_password():
    with pytest.raises(ValidationError) as e_info:
        UserCreate(
            first_name="John",
            last_name="Doe",
            username="JohnDoe",
            password="fit!xog4?aze08noqLda",
            confirm_password="1fit!xog4?aze08noqLda",
        )
    assert "Passwords do not match" in str(e_info.value)
