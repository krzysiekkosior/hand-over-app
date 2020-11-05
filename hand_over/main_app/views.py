from django.shortcuts import render
from django.views import View

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
        return render(request, 'register.html')
