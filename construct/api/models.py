from django.db import models
from django.contrib.auth.models import User

from datetime import *


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
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        db_table = 'news'


class ProductCategory(models.Model):
    name = models.CharField(max_length=30, null=False)
    picture = models.ImageField(upload_to='images/', default='default.png')
    description = models.TextField(default='Категория товаров.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'product_category'


class Measure(models.Model):
    full_measure = models.CharField(max_length=255, default='Measure')
    measure = models.CharField(max_length=255)

    def __str__(self):
        return self.measure

    class Meta:
        verbose_name = 'Мера товара'
        verbose_name_plural = 'Меры товаров'
        db_table = 'measure'


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
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'product'


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
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        db_table = 'review'


class Profile(models.Model):
    profile_status = models.TextField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/')
    bio = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client_id)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        db_table = 'profile'


class UserCart(models.Model):
    product_list = models.JSONField(default=dict)
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client_id)

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'
        db_table = 'user_cart'


class OrderStatus(models.Model):
    status_name = models.CharField(max_length=255)

    def __str__(self):
        return self.status_name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'
        db_table = 'order_status'


class OrderPayment(models.Model):
    payment_name = models.CharField(max_length=255)

    def __str__(self):
        return self.payment_name

    class Meta:
        verbose_name = 'Метод оплаты'
        verbose_name_plural = 'Методы оплаты'
        db_table = 'order_payment'


class District(models.Model):
    region_kladr = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'
        db_table = 'district'


class Address(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    fact_address = models.TextField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        db_table = 'address'

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
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'order'


class Support(models.Model):
    cd = datetime.now()

    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    client_mail = models.EmailField(null=False)
    date_created = models.DateTimeField(default=cd, verbose_name="Time sent")
    appeal = models.TextField(null=False)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return str('Обращение № ' + str(self.id) + ' от ' + str(self.client_id))

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        db_table = 'support'


class Templates(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Мой штамп")
    author = models.CharField(max_length=50, null=True, blank=True)
    checker = models.CharField(max_length=50, null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    schema = models.CharField(max_length=50, null=True, blank=True)
    stage = models.CharField(max_length=50, null=True, default="Р", blank=True)
    page = models.CharField(max_length=50, null=True, blank=True)
    object = models.CharField(max_length=50, null=True, blank=True)
    project = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Штамп'
        verbose_name_plural = 'Штампы'
        db_table = 'templates'
