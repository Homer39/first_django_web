from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, LoginView, LogoutView, ActivateView, CustomPasswordResetView, \
    CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView, recover_password_view, \
    ProfileView, send_activate_mail_view, forget_password_view

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('recover_password/', recover_password_view, name='recover_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm_prof/', send_activate_mail_view, name='send_activate_mail'),
    path('random_password_form/', forget_password_view, name='random_password_form')
]
