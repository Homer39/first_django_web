from django.core.cache import cache

from catalog.models import Category
from config import settings

def get_cached_categories():
    queryset = Category.objects.all()
    if settings.CACHE_ENABLE:
        key = 'category_list'
        category_list = cache.get(key)

        if category_list is None:
            category_list = queryset
            cache.set(key, category_list)
        return category_list

    return queryset


