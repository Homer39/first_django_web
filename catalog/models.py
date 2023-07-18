from django.db import models

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

    def __str__(self):
        return f'{self.product_name} ({self.category}) - {self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
