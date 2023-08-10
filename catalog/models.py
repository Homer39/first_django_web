from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Наименование')
    category_description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Наименование')
    product_description = models.TextField(verbose_name='Описание', max_length=100)
    image = models.ImageField(verbose_name='Изображение', upload_to='product/', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
    creation_date = models.DateField(auto_now=True, auto_now_add=False, verbose_name='дата создания')
    last_change_date = models.DateField(auto_now=False, auto_now_add=True, verbose_name='дата последнего изменения')

    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Продавец', **NULLABLE)

    def __str__(self):
        return f'{self.product_name} ({self.category}) - {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_actual = models.BooleanField(default=True, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.product} - {self.version_name} ({self.is_actual})'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'





class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, unique=True, verbose_name='slug', **NULLABLE)
    text = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(verbose_name='Изображение', upload_to='blog/', **NULLABLE)
    creation_date = models.DateField(auto_now=True, auto_now_add=False, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
