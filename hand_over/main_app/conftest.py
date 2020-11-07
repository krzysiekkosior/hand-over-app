import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    user = User.objects.create(username='test@test.com')
    user.set_password(raw_password='testpassword123')
    user.save()
    return user
