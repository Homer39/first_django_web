from django.urls import path

from django.views.decorators.cache import cache_page

from catalog.views import contacts, ProductCreateView, ProductsListView, ProductsDetailView, HomeListView, \
    ProductUpdateView, ProductDeleteView, BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, \
    toggle_published, CategoryListView, CategoryProductListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home_list'),
    path('contacts/', cache_page(60)(contacts), name='contacts'),

    path('category/', CategoryListView.as_view(), name='category_list'),

    path('<int:pk>/products/', CategoryProductListView.as_view(), name='category_product'),

    path('product_list/', ProductsListView.as_view(), name='products_list'),
    path('product_detail/<int:pk>/', cache_page(60)(ProductsDetailView.as_view()), name='products_detail'),

    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('edit_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),

    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog_update/<int:pk>/', BlogUpdateView.as_view(), name='update_blog'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
    path('is_published/<int:pk>/', toggle_published, name='is_published')

]
