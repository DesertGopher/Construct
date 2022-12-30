from decimal import Decimal
from urllib import request

from django.conf import settings
from api.models import Product
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

global total


class Cart(object):
    def __init__(self, request):
        """ Инициализация корзины """
        # хранение сессии корзины для доступа в других классах
        self.session = request.session
        # получаем сессию корзины
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """ Добавить продукт в корзину или обновить его количество"""
        product_id = str(product.id)
        boolka = False

        if int(quantity) > int(product.is_stock):
            print('Нельзя добавить чтобы было больше чем в наличии изначально')

        elif not update_quantity:
            if int(quantity) > int(product.is_stock):
                print('Нельзя добавить чтобы было больше')

            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0,
                                         'price': str(product.price),
                                         'discount': str(product.discount)}
            self.cart[product_id]['quantity'] += quantity

            if not self.cart[product_id]['quantity'] > int(product.is_stock):
                self.save()
                boolka = True
            else:
                print('Не поулчится так')


    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных."""
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['priceU'] = Decimal(item['price'])
            item['total_priceU'] = item['priceU'] * item['quantity']

            if item['discount'] == 0:
                item['price'] = Decimal(item['price'])
            else:
                item['price'] = Decimal(Decimal(item['price']) * (100 - Decimal(item['discount']))/100)
            item['total_price'] = item['price'] * item['quantity']
            item['total_discount'] = item['total_priceU'] - item['total_price']
            yield item

    def __len__(self):
        """Подсчет всех товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Подсчет стоимости товаров в корзине."""
        return sum(Decimal(Decimal(item['price']) * (100 - Decimal(item['discount']))/100) * item['quantity'] for item in
                   self.cart.values())

    def get_total_price_cart(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def get_total_discount(self):
        """Подсчет скидки всех товаров"""
        return sum(Decimal(item['total_discount']) for item in
                   self.cart.values())

    def get_all_products(self):
        """Вывод всех продуктов корзины"""
        product_ids = self.cart.keys()
        prod_list = []
        # prod_price = []
        prod_amount = []
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            prod_list.append(str(product.id))
            # prod_price.append(str(product.get_sale()))

        # stringprod = str(prod_list) + str(prod_price)
        for item in self.cart.values():
            prod_amount.append(str(item['quantity']))

        product_list = dict(zip(prod_list, prod_amount))
        return product_list

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
