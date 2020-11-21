from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.core.paginator import Paginator
from main_app.forms import SignUpForm, DonationForm, EditUserForm
from main_app.models import Institution, Category
from main_app.tokens import account_activation_token
from main_app.utils import get_bags_quantity, get_supported_institutions_amount, get_donation_list, \
    change_donation_status_to_taken
import json


class LandingPageView(View):

    def get(self, request):
        bags = get_bags_quantity()
        institutions = get_supported_institutions_amount()
        context = {'bags': bags,
                   'institutions': institutions}
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
        return JsonResponse({'errors': errors})


class LoginView(View):

    def get(self, request):
        return render(request, 'registration/login.html')

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
        return render(request, 'registration/login.html', {'error': "Podane hasło jest błędne.",
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
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta (Oddam w dobre ręce)'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user=user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            context = {'activate_acc': 'Na podany adres email został wysłany link aktywacyjny.'}
            return render(request, 'email_verification.html', context)
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


def paginate_institutions(request):
    page = int(request.GET.get('page'))
    inst_type = int(request.GET.get('type')) - 1
    print(f'typ: {inst_type}, strona: {page}')

    objects = Institution.objects.filter(type=inst_type)
    paginator = Paginator(objects, 2)
    amount_of_pages = paginator.num_pages
    institutions = []
    for institution in paginator.get_page(page):
        categories = []
        for category in institution.categories.all():
            categories.append({'name': category.name})
        json_institution = {'name': institution.name,
                            'description': institution.description,
                            'categories': categories}
        institutions.append(json_institution)
    return JsonResponse({'institutions': institutions, 'page': page, 'last_page': amount_of_pages})


def donation_added(request):
    return render(request, 'form-confirmation.html')


class ProfileView(View):

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return redirect('login')
        taken_donations, not_taken_donations, not_taken_donations_amount = get_donation_list(user)
        context = {
            'taken_donations': taken_donations,
            'not_taken_donations': not_taken_donations,
            'not_taken_donations_amount': not_taken_donations_amount
        }
        return render(request, 'profile.html', context)

    def post(self, request):
        donations_ids = request.POST.getlist('is_taken')
        change_donation_status_to_taken(donations_ids)
        taken_donations, not_taken_donations, not_taken_donations_amount = get_donation_list(request.user)
        context = {
            'taken_donations': taken_donations,
            'not_taken_donations': not_taken_donations,
            'not_taken_donations_amount': not_taken_donations_amount
        }
        return render(request, 'profile.html', context)


class EditUserView(View):

    def get(self, request):
        user = request.user
        form = EditUserForm(instance=user)
        context = {'form': form, 'title': 'Edycja profilu'}
        return render(request, 'edit_user_form.html', context)

    def post(self, request):
        user = request.user
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password_confirm')
            if user.check_password(password):
                edited_user = form.save(commit=False)
                if user.email != email:
                    edited_user.username = email
                edited_user.save()
                return redirect('profile')
            error = "Błędne hasło"
        context = {'form': form, 'title': 'Edycja profilu', 'error': error}
        return render(request, 'edit_user_form.html', context)


class ChangeUserPasswordView(View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        context = {'form': form, 'title': 'Zmiana hasła'}
        return render(request, 'edit_user_form.html', context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            auth.logout(request)
            return redirect('password_changed')
        context = {'form': form, 'title': 'Zmiana hasła'}
        return render(request, 'edit_user_form.html', context)


def password_change_done(request):
    return render(request, 'password_change_done.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context = {'activate_pass': 'Konto zostało aktywowane. Możesz się teraz zalogować.'}
        return render(request, 'email_verification.html', context)
    else:
        context = {'activate_fail': 'Link aktywacyjny jest niepoprawny.'}
        return render(request, 'email_verification.html', context)
