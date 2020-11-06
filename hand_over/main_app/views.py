from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from main_app.forms import SignUpForm
from main_app.models import Institution
from main_app.utils import get_bags_quantity, get_supported_institutions_amount


class LandingPage(View):

    def get(self, request):
        bags = get_bags_quantity()
        institutions = get_supported_institutions_amount()
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local_collections = Institution.objects.filter(type=2)
        context = {'bags': bags,
                   'institutions': institutions,
                   'organizations': organizations,
                   'foundations': foundations,
                   'collections': local_collections}
        return render(request, 'index.html', context)


class AddDonation(View):

    def get(self, request):
        return render(request, 'form.html')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')


class Register(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password2']
            user = User.objects.create(username=email, first_name=first_name, last_name=last_name, email=email)
            user.set_password(raw_password=password)
            user.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})
