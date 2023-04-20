from http import HTTPStatus

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
def user_create_list_url():
    return reverse("user:user-list-create")


@pytest.mark.django_db
def test_create_list_api_returns_correct_status_code(client, user_create_list_url):
    response = client.get(user_create_list_url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_user_create_api_succeeds_with_valid_inputs(
    client, user_create_list_url, user_payload
):
    response = client.post(user_create_list_url, user_payload)

    assert response.status_code == HTTPStatus.CREATED

    user_payload.pop("password")
    for key, value in user_payload.items():
        assert value == response.json()[key]


@pytest.mark.django_db
def test_check_that_invalid_birthday_format_returns_error(
    client, user_create_list_url, user_payload
):
    user_payload.update(birthdate="19-19-19")

    response = client.post(user_create_list_url, user_payload)
    print(response.json())

    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
def test_user_can_grant_permission_successful(
    client, generated_user, generated_permission, django_user_model
):
    user_id = str(generated_user.id)
    permission_id = str(generated_permission.id)

    user_permissions_url = (
        f"/api/users/permission?user_id={user_id}&permission_id={permission_id}"
    )

    response = client.post(user_permissions_url)

    assert response.status_code == HTTPStatus.OK

    user = django_user_model.objects.get(id=user_id)
    permission = user.permissions.all().filter(id=permission_id)

    assert permission is not None


@pytest.mark.django_db
def test_user_can_revoke_permission_successful(
    client, generated_user, generated_permission, django_user_model
):
    user_id = str(generated_user.id)
    permission_id = str(generated_permission.id)
    generated_user.revoke_permission(permission_id)

    user_permissions_url = (
        f"/api/users/permission?user_id={user_id}&permission_id={permission_id}"
    )

    response = client.delete(user_permissions_url)

    assert response.status_code == HTTPStatus.OK

    user = django_user_model.objects.get(id=user_id)
    permission = user.permissions.all().filter(id=permission_id)

    assert permission.exists() is False
