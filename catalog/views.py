from django.shortcuts import render


def homepage(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'New message from {name}, {email}: {message}')
    return render(request, 'catalog/contacts.html')
