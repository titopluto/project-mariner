import uuid

import pytest
from django.contrib.auth import get_user_model

from permission.models import Permission

UserModel = get_user_model()


@pytest.fixture
def permission_data():
    return {
        "name": "Can Invoke server",
        "type": "EC2",
        "description": "Permssion for users that can invoke lambda on EC2 Servers",
        "granted_date": "2023-06-01",
    }


@pytest.fixture
def create_permission(db, permission_data):
    def make_permission(**kwargs):
        return Permission.objects.create(**kwargs)

    return make_permission


@pytest.mark.django_db
def test_create_permission(create_permission, permission_data):
    permission = create_permission(**permission_data)

    for key, value in permission_data.items():
        assert value == permission.__dict__[key]
