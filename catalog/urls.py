from django.urls import path

from catalog.views import homepage, contacts

urlpatterns = [
    path('', homepage),
    path('contacts/', contacts),
]
