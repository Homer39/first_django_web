from django.urls import path

from catalog.views import homepage, contacts, products, product

urlpatterns = [
    path('', homepage),
    path('contacts/', contacts),
    path('products/', products),
    path('<int:pk>/product/', product, name='product')
]
