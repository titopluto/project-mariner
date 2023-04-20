import datetime
import uuid

import pytest

from django.urls import reverse


@pytest.fixture
def permission_payload():
    return {
        "name": "Can Invoke server",
        "type": "EC2",
        "description": "Permssion for users that can invoke lambda on EC2 Servers",
        "granted_date": "2023-06-01",
    }


@pytest.fixture
def permission_create_list_url():
    return reverse("permission:permission-list-create")


@pytest.mark.django_db
def test_create_list_api_returns_correct_status_code(
    client, permission_create_list_url
):
    response = client.get(permission_create_list_url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_create_api_succeeds_with_valid_inputs(
    client, permission_create_list_url, permission_payload
):
    response = client.post(permission_create_list_url, permission_payload)

    assert response.status_code == 201

    for key, value in permission_payload.items():
        assert value == response.json()[key]


@pytest.mark.django_db
def test_user_create_api_succeeds_with_valid_minimum_requirements_data(
    client, permission_create_list_url, permission_payload
):
    permission_payload.pop("name")
    permission_payload.pop("description")

    response = client.post(permission_create_list_url, permission_payload)

    assert response.status_code == 201

    for key, value in permission_payload.items():
        assert value == response.json()[key]


@pytest.mark.django_db
def test_user_create_api_uses_todays_date_when_grant_date_is_missing(
    client, permission_create_list_url, permission_payload
):
    permission_payload.pop("granted_date")

    response = client.post(permission_create_list_url, permission_payload)

    assert response.status_code == 201

    assert response.data["granted_date"] == datetime.date.today().isoformat()
