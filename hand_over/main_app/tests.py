from django.test import TestCase
import pytest


# Create your tests here.


@pytest.mark.django_db
def test_landing_page_url(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_donation_url(client):
    response = client.get('/add-donation/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_url(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_url(client):
    response = client.get('/register/')
    assert response.status_code == 200
