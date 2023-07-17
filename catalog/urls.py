from django.urls import path

from catalog.views import homepage, contacts, products

urlpatterns = [
    path('', homepage),
    path('contacts/', contacts),
    path('products/', products),
]
