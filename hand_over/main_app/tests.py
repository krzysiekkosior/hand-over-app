from django.contrib.auth.models import User
import pytest
from django.urls import reverse_lazy
from django.contrib.auth import get_user

from main_app.models import Donation


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


@pytest.mark.django_db
def test_login_user(client, user):
    context = {'username': 'tesat@test.com', 'password': 'testpassword123'}
    client.post(reverse_lazy('login'), context)
    logged_user = get_user(client)
    assert logged_user.is_authenticated


@pytest.mark.django_db
def test_create_donation(client, user, institution_category, institution):
    client.login(username='test@test.com', password='testpassword123')
    context = {'quantity': '2',
               'categories': [f'{institution_category.id}'],
               'institution': f'{institution.id}',
               'address': 'Road 12',
               'phone_number': '506295378',
               'city': 'Warsaw',
               'zip_code': '03-123',
               'pick_up_date': '2020-11-18',
               'pick_up_time': '15:34',
               'pick_up_comment': 'comment'
               }

    client.post(reverse_lazy('add_donation'), context, content_type='application/json')
    assert Donation.objects.count() == 1


@pytest.mark.django_db
def test_profile_url_as_logged_user(client, user):
    client.login(username='test@test.com', password='testpassword123')
    response = client.get(reverse_lazy('profile'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_url_as_anonymous_user(client):
    response = client.get(reverse_lazy('profile'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_change_donation_status_to_taken(client, user, donation):
    client.login(username='test@test.com', password='testpassword123')
    assert donation.is_taken is False
    client.post(reverse_lazy('profile'), {'is_taken': '1'})
    donation.refresh_from_db()
    assert donation.is_taken is True
