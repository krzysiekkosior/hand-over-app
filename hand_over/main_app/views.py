from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from main_app.forms import SignUpForm, DonationForm
from main_app.models import Institution, Category, Donation
from main_app.utils import get_bags_quantity, get_supported_institutions_amount
import json


class LandingPageView(View):

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


class AddDonationView(View):

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return redirect('login')
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'form.html', context)

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        form = DonationForm(data)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            categories_ids = data.get('categories')
            for cat_id in categories_ids:
                donation.categories.add(Category.objects.get(id=int(cat_id)))
            donation.save()
        errors = []
        for error in form.errors:
            errors.append({'error': form.errors[error][0]})
            print(form.errors[error])
        return JsonResponse({'errors': errors})


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('register')

        password = request.POST.get('password')
        if user.check_password(raw_password=password):
            login(self.request, user)
            return redirect('landing_page')
        return render(request, 'login.html', {'error': "Podane hasło jest błędne.",
                                              'email': username})


class RegisterView(View):

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


def get_institutions_by_category(request):
    categories_ids = request.GET.getlist('cat_ids')
    categories_ids = [int(cat_id) for cat_id in categories_ids]

    institutions = Institution.objects.filter(categories__in=categories_ids).distinct()
    institutions_to_display = []
    for institution in institutions:
        json_institution = {'id': institution.id,
                            'name': institution.name,
                            'type': institution.get_type_display(),
                            'description': institution.description}
        institutions_to_display.append(json_institution)
    return JsonResponse({'institutions': institutions_to_display})


def donation_added(request):
    return render(request, 'form-confirmation.html')


class ProfileView(View):

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return redirect('login')
        donations = Donation.objects.filter(user=user)
        return render(request, 'profile.html', {'donations': donations})

