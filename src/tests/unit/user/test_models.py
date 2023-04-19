import pytest
from django.contrib.auth import get_user_model


UserModel = get_user_model()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "given_name": "Test",
        "family_name": "User",
        "gender": "Male",
        "phone_number": "+1234567890",
        "birthdate": "1990-01-01",
        "password": "testpass123",
        "is_verified": True,
        "is_active": True,
        "is_staff": False,
        "is_admin": False,
        "is_superuser": False,
    }


@pytest.fixture
def create_user(db, django_user_model, user_data):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.mark.django_db
def test_create_user(create_user, user_data):
    user = create_user(**user_data)
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.given_name == user_data["given_name"]
    assert user.family_name == user_data["family_name"]
    assert user.birthdate == user_data["birthdate"]
    assert user.gender == user_data["gender"]
    assert user.phone_number == user_data["phone_number"]
    assert user.check_password(user_data["password"])
    assert user.is_verified == user_data["is_verified"]
    assert user.is_active == user_data["is_active"]
    assert user.is_staff == user_data["is_staff"]
    assert user.is_admin == user_data["is_admin"]
    assert user.is_superuser == user_data["is_superuser"]
