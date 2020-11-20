"""hand_over URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('add-donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('get_institutions/', views.get_institutions_by_category),
    path('donadion-added/', views.donation_added, name='added'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/edit/', views.EditUserView.as_view(), name='edit_profile'),
    path('accounts/profile/change-password/', views.ChangeUserPasswordView.as_view(), name='change_password'),
    path('password-changed', views.password_change_done, name='password_changed'),
    path('institutions/', views.paginate_institutions, name='paginate_institutions'),
]
