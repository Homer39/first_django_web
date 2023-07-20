from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Blog


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home_list.html'


class ProductsListView(ListView):
    model = Product


class ProductsDetailView(DetailView):
    model = Product


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'New message from {name}, {email}: {message}')
    return render(request, 'catalog/contacts.html', context)


class ProductCreateView(CreateView):
    model = Product
    fields = ('product_name', 'product_description', 'price', 'category', 'image')
    success_url = reverse_lazy('products_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('product_name', 'product_description', 'price', 'category', 'image')
    success_url = reverse_lazy('products_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products_list')


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'text', 'image')
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'text', 'image')
    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog_list')


def toggle_published(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.is_published:
        blog.is_published = False
    else:
        blog.is_published = True

    blog.save()

    return redirect('blog_list')