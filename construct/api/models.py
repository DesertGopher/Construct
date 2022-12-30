from django.db import models
from django.contrib.auth.models import User
from datetime import *
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser


class News(models.Model):
    cd = datetime.now()

    title = models.CharField(max_length=255, null=False)
    news = models.TextField(default='Новая новость')
    pub_date = models.DateTimeField(default=cd, verbose_name="Time published")
    picture = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новость'


class ProductCategory(models.Model):
    name = models.CharField(max_length=30, null=False)
    picture = models.ImageField(upload_to='images/', default='default.png')
    description = models.TextField(default='Категория товаров.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'


class Measure(models.Model):
    full_measure = models.CharField(max_length=255, default='Measure')
    measure = models.CharField(max_length=255)

    def __str__(self):
        return self.measure

    class Meta:
        verbose_name = 'Меры товаров'
        verbose_name_plural = 'Мера товара'


class Product(models.Model):
    name = models.CharField(max_length=30, null=False)
    price = models.FloatField(null=False)
    about = models.TextField(null=False)
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE)
    category_class = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=255, null=True, default='Construct inc.')
    is_stock = models.IntegerField(null=False, default=10)
    discount = models.IntegerField(null=True, default=0)
    prod_pic = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_sale(self):
        salePrice = int(self.price * (100 - self.discount) / 100)
        return salePrice

    def get_absolute_url(self):
        return f'/shop/{self.id}/'

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукт'


class Review(models.Model):
    text = models.TextField(max_length=500)
    profile_picture = models.ImageField(upload_to='images/')
    pub_date = models.DateTimeField(default=datetime.now(), verbose_name="Time published")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    post = models.ForeignKey(Product, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/shop/{self.id}/'

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзыв'


class Profile(models.Model):
    profile_status = models.TextField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/')
    bio = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client_id)

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профиль'


class UserCart(models.Model):
    product_list = models.JSONField(default=dict)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client_id)

    class Meta:
        verbose_name = 'Корзины пользователей'
        verbose_name_plural = 'Корзина пользователя'


class OrderStatus(models.Model):
    status_name = models.CharField(max_length=255)

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = 'Статусы заказа'
        verbose_name_plural = 'Статус заказа'


class OrderPayment(models.Model):
    payment_name = models.CharField(max_length=255)

    def __str__(self):
        return self.payment_name

    class Meta:
        verbose_name = 'Методы оплаты'
        verbose_name_plural = 'Метод оплаты'


class District(models.Model):
    region_kladr = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регионы'
        verbose_name_plural = 'Регион'


class Address(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    fact_address = models.TextField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Адреса'
        verbose_name_plural = 'Адрес'

    def __str__(self):
        return self.fact_address


class Order(models.Model):
    cd = datetime.now()

    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=cd, verbose_name="Time published")
    payment_type = models.ForeignKey(OrderPayment, on_delete=models.CASCADE)
    product_list = models.JSONField()
    total_cost = models.IntegerField()
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return str('Заказ № ' + str(self.id))

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказ'

