from django.shortcuts import render
from django.views import View
from main_app.utils import get_bags_quantity, get_supported_institutions


class LandingPage(View):

    def get(self, request):
        bags = get_bags_quantity()
        institutions = get_supported_institutions()
        context = {'bags': bags,
                   'institutions': institutions}
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
