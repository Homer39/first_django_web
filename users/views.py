from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.utils.encoding import force_bytes, force_str

from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.views import View

from django.views.generic import CreateView, UpdateView

from config import settings
from users.email_verification_token_generator import email_verification_token
from users.forms import UserRigisterForm, CustomPasswordResetForm, CustomResetConfirmForm, RecoverPasswordForm, \
    UserProfileForm
from users.models import User
from users.random_password import generate_new_password

from django.core.exceptions import ObjectDoesNotExist


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRigisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:send_activate_mail')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        current_site = get_current_site(self.request)
        send_mail(
            subject='Поздравляем с регистрацией',
            message=f'Активируйте ваш профиль: http://{current_site.domain}/users/activate/{urlsafe_base64_encode(force_bytes(new_user.pk))}/{email_verification_token.make_token(new_user)}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]

        )
        return super().form_valid(form)


def send_activate_mail_view(request):
    return render(request, 'users/send_activate_mail.html')


class ActivateView(View):

    def get_user_from_email_verification_token(self, uid, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                get_user_model().DoesNotExist):
            return None

        if user is not None \
                and \
                email_verification_token.check_token(user, token):
            return user
        return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64, token)
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:login')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/password_reset_email.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomResetConfirmForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        # Метод, который отрабатывает при успешной валидации формы
        if form.is_valid():
            self.object = form.save()
            send_mail(
                subject='Изменения пароля',
                message=f'Вы поменяли пароль от своего профиля',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    success_url = reverse_lazy('users:login')


def forget_password_view(request):
    if request.method == 'POST':
        recover_form = RecoverPasswordForm(request.POST)
        if recover_form.is_valid():
            email = recover_form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                generate_new_password(user)
                return redirect('users:recover_password')
            except ObjectDoesNotExist:
                form = RecoverPasswordForm()
                context = {'form': form,
                           'user_does_not_exist': recover_form.cleaned_data['email']}
                return render(request, 'users/random_password_form.html', context)
    else:
        form = RecoverPasswordForm()
        context = {'form': form}
        return render(request, 'users/random_password_form.html', context=context)


def recover_password_view(request):
    return render(request, 'users/recover_password.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
