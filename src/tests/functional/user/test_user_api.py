import pytest

from django.urls import reverse


@pytest.fixture
def user_payload():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "secure-password",
        "given_name": "Test",
        "family_name": "User",
        "birthdate": "1990-01-01",
    }


@pytest.fixture
def create_list_url():
    return reverse("user:user-list-create")


@pytest.mark.django_db
def test_create_list_api_returns_correct_status_code(client, create_list_url):
    response = client.get(create_list_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_create_api_succeeds_with_valid_inputs(
    client, create_list_url, user_payload
):
    response = client.post(create_list_url, user_payload)

    assert response.status_code == 201

    user_payload.pop("password")
    for key, value in user_payload.items():
        assert value == response.json()[key]


@pytest.mark.django_db
def test_check_that_invalid_birthday_format_returns_error(
    client, create_list_url, user_payload
):
    user_payload.update(birthdate="19-19-19")

    response = client.post(create_list_url, user_payload)
    print(response.json())

    assert response.status_code == 400
