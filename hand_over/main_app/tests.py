from django.contrib.auth.models import User
import pytest
from django.urls import reverse_lazy


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


@pytest.mark.django_db
def test_create_user(client):
    context = {
        'first_name': 'TestoweImie',
        'last_name': 'TestoweNazwisko',
        'email': 'test@test.com',
        'password1': 'trudnehaslo123',
        'password2': 'trudnehaslo123'
    }
    client.post(reverse_lazy('register'), context)
    assert User.objects.exists()
    assert User.objects.first().password != 'trudnehaslo123'
