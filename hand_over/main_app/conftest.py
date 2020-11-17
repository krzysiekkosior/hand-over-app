import pytest
from django.contrib.auth.models import User
from django.test import Client

from main_app.models import Category, Institution


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    user = User.objects.create(username='test@test.com')
    user.set_password(raw_password='testpassword123')
    user.save()
    return user


@pytest.fixture
def donation_category():
    donation_category = Category.objects.create(name='donation_category')
    return donation_category


@pytest.fixture
def institution_category():
    institution_category = Category.objects.create(name='institution_category')
    return institution_category


@pytest.fixture
def institution(institution_category):
    institution = Institution.objects.create(name='institution', description='description')
    institution.categories.add(institution_category)
    institution.save()
    return institution
