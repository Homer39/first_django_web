from django.shortcuts import render
from catalog.models import Product


def homepage(request):
    products_list = Product.objects.all()
    contex = {
        'object_list': products_list,
    }
    return render(request, 'catalog/home.html', contex)


def products(request):
    products_list = Product.objects.all()
    contex = {
        'object_list': products_list,
    }
    return render(request, 'catalog/products.html', contex)



def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'New message from {name}, {email}: {message}')
    return render(request, 'catalog/contacts.html')
