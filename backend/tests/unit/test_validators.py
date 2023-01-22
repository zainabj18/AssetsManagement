from app.schemas import UserCreate
from pydantic.error_wrappers import ValidationError
import pytest
def test_user_create_requires_same_password():
    with pytest.raises(ValidationError) as e_info:
        UserCreate(first_name="John",last_name="Doe",username="JohnDoe",password="Welcome",confirm_password="Welcome1")
    assert "'Passwords do not match" in e_info.value
