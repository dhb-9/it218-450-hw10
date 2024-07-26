from pydantic import ValidationError, EmailStr, HttpUrl
import pytest
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, LoginRequest

@pytest.fixture
def user_base_data():
    return {
        "nickname": "testuser",
        "email": "testuser@example.com",
        "profile_picture_url": "http://example.com/profile.jpg"
    }

@pytest.fixture
def user_create_data():
    return {
        "nickname": "testuser",
        "password": "ValidPassword123!"
    }

@pytest.fixture
def user_update_data():
    return {
        "email": "updateduser@example.com",
        "first_name": "UpdatedFirstName"
    }

@pytest.fixture
def user_response_data():
    return {
        "id": "user_id",
        "nickname": "testuser",
        "email": "testuser@example.com",
        "last_login_at": None
    }

@pytest.fixture
def login_request_data():
    return {
        "email": "testuser@example.com",
        "password": "ValidPassword123!"
    }

def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]
    assert user.profile_picture_url == user_base_data["profile_picture_url"]

def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.nickname == user_create_data["nickname"]
    assert user.password == user_create_data["password"]

def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]
    assert user_update.first_name == user_update_data["first_name"]

def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    assert user.nickname == user_response_data["nickname"]
    assert user.email == user_response_data["email"]

def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.email == login_request_data["email"]
    assert login.password == login_request_data["password"]

@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

def test_user_base_invalid_email(user_base_data):
    user_base_data_invalid = user_base_data.copy()
    user_base_data_invalid["email"] = "john.doe.example.com"
    with pytest.raises(ValidationError) as exc_info:
        UserBase(**user_base_data_invalid)
    assert "value is not a valid email address" in str(exc_info.value)
    assert "john.doe.example.com" in str(exc_info.value)
