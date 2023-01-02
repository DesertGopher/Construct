import string
from typing import Optional
import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .views import *
import random


class Values():

    letters = string.ascii_letters

    def string_values(self, str_length: Optional[int] = 5):
        return ''.join(random.choice(self.letters) for i in range(str_length))

    def int_values(self, int1: Optional[int] = 1000, int2: Optional[int] = 10000):
        return random.randint(int1, int2)

    def smallint_values(self):
        return random.randint(0, 1)

    def float_values(self, float1: Optional[int] = 1000, float2: Optional[int] = 10000):
        float_num = random.uniform(float1, float2)
        return round(float_num, 2)

    def date_values(self, date1: Optional[int] = date.today().replace(day=1, month=1),
                    date2: Optional[int] = date.today().toordinal()):
        return date.fromordinal(random.randint(date1, date2))

    def json(self, pairs: Optional[int]=1) -> dict:
        json_data = {}
        for _ in range(pairs):
            json_data[self.string_values()] = self.string_values()
        return json_data

    def boolean_vlues(self):
        bool_val = random.randint(0, 1)
        if bool_val == 0:
            return False
        else:
            return True


VAL = Values()


class UsersTests(APITestCase):
    """Класс для тестирования таблицы Users"""

    # Users.permission_classes = [AllowAny]
    # UserDetail.permission_classes = [AllowAny]

    def setUp(self):
        """Метод для ввода новых записей в тестовую БД"""
        for id in range(1, 4):
            User.objects.create(
                id=id,
                password=VAL.string_values(),
                # last_login=VAL.int_values(),
                is_superuser=False,
                username=str('User'+str(id)),
                first_name=VAL.string_values(),
                last_name=VAL.string_values(),
                email='email@mail.ru',
                is_staff=False,
                is_active=True,
                # date_joined=VAL.int_values(),
                # groups=[],
                # user_permissions=[]
            )

        self.valid_field_payload = {
            'id': 5,
            'password': VAL.string_values(),
            # 'last_login': VAL.int_values(),
            'is_superuser': False,
            'username': VAL.string_values(),
            'first_name': VAL.string_values(),
            'last_name': VAL.string_values(),
            'email': 'email@mail.ru',
            'is_staff': False,
            'is_active': True,
            # 'date_joined': VAL.int_values(),
            # 'groups': [],
            # 'user_permissions': []
        }

        self.invalid_field_payload = {
            'invalid_id': 5,
            'invalid_password': VAL.string_values(),
            # 'invalid_last_login': VAL.int_values(),
            'invalid_is_superuser': False,
            'invalid_username': VAL.string_values(),
            'invalid_first_name': VAL.string_values(),
            'invalid_last_name': VAL.string_values(),
            'invalid_email': 'email@mail.ru',
            'invalid_is_staff': False,
            'invalid_is_active': True,
            # 'invalid_date_joined': VAL.int_values(),
            # 'invalid_groups': [],
            # 'invalid_user_permissions': []
        }

        self.invalid_field_payload_data = {
            'id': 10,
            'password': VAL.json(),
            # 'last_login': VAL.string_values(),
            'is_superuser': VAL.string_values(),
            'username': VAL.float_values(),
            'first_name': VAL.json(),
            'last_name': VAL.json(),
            'email': VAL.json(),
            'is_staff': VAL.float_values(),
            'is_active': VAL.float_values(),
            # 'date_joined': VAL.json(),
            # 'groups': VAL.int_values(),
            # 'user_permissions': VAL.int_values()
        }

        self.valid_field_payload_put = {
            'id': 1,
            'password': VAL.string_values(),
            # 'last_login': VAL.int_values(),
            'is_superuser': False,
            'username': VAL.string_values(),
            'first_name': VAL.string_values(),
            'last_name': VAL.string_values(),
            'email': 'email2@mail.ru',
            'is_staff': False,
            'is_active': True,
            # 'date_joined': VAL.int_values(),
            # 'groups': [],
            # 'user_permissions': []
        }

    def test_get_all_users(self):
        """Метод получения всех пользователей"""
        response = self.client.get(reverse('api:user'))
        users = User.objects.all()
        serializer = UsersSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_user(self):
        """Метод получения пользователя по id"""
        response = self.client.get(reverse('api:user_detail', kwargs={'id': 1}))
        user = User.objects.get(pk=1)
        serializer = UsersSerializer(user)
        assert(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invalid_user(self):
        """Метод получения несуществующего пользователя"""
        response = self.client.get(reverse('api:user_detail', kwargs={'id': 6}))
        self.assertEqual(response.data, ER.get_err_message(6, 'Пользователь'))

    def test_create_user(self):
        """Метод создания нового пользователя"""
        response = self.client.post(
            reverse('api:user'),
            data=json.dumps(self.valid_field_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_user(self):
        """Метод создания нового пользователя с неправильно введенными полями"""
        response = self.client.post(
            reverse('api:user'),
            data=json.dumps(self.invalid_field_payload),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_create_invalid_user_data(self):
        """Метод создания нового пользователя с неправильно введенными данными"""
        response = self.client.post(
            reverse('api:user'),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_valid_update_user(self):
        """Метод изменения пользователя"""
        data = User.objects.get(pk=1)
        response = self.client.put(
            reverse('api:user_detail',
            kwargs={'id': 1}),
            data=json.dumps(self.valid_field_payload_put),
            content_type='application/json')
        updated_data = User.objects.get(
            pk=1)
        serializer = UsersSerializer(data)
        updated_serializer = UsersSerializer(updated_data)
        self.assertNotEqual(
            serializer.data['email'], updated_serializer.data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        """Метод неправильного изменения региона"""
        response = self.client.put(
            reverse('api:user_detail',
                    kwargs={'id': 1}),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_is_user_active(self):
        """Метод получения активного пользователя по id"""
        response = self.client.get(reverse('api:user_detail', kwargs={'id': 1}))
        user = User.objects.get(pk=1, is_active=True)
        serializer = UsersSerializer(user)
        assert(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_is_user_client(self):
        """Метод получения пользователя-клиента по id"""
        response = self.client.get(reverse('api:user_detail', kwargs={'id': 1}))
        user = User.objects.get(pk=1, is_superuser=False)
        serializer = UsersSerializer(user)
        assert(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductsTests(APITestCase):
    """Класс для тестирования таблицы Products"""

    def setUp(self):
        """Метод для ввода новых записей в тестовую БД"""

        self.measure = Measure.objects.create(
            id=1,
            full_measure=VAL.string_values(),
            measure=VAL.string_values(),
        )

        self.category = ProductCategory.objects.create(
            id=1,
            name=VAL.string_values(),
            description=VAL.string_values(),
        )

        for id in range(1, 4):
            Product.objects.create(
                id=id,
                name=VAL.string_values(),
                price=VAL.float_values(),
                about=VAL.string_values(50),
                measure=self.measure,
                category_class=self.category,
                vendor=VAL.string_values(),
                is_stock=VAL.int_values(),
                discount=VAL.int_values(1, 50),
                is_active=True,
            )

        self.valid_field_payload = {
            'id': 5,
            'name': VAL.string_values(),
            'price': VAL.float_values(),
            'about': VAL.string_values(50),
            # 'measure': self.measure,
            # 'category_class': self.category,
            'vendor': VAL.string_values(),
            'is_stock': VAL.int_values(),
            'discount': VAL.int_values(1, 50),
            'is_active': True,
        }

        self.invalid_field_payload = {
            'invalid_id': 5,
            'invalid_name': VAL.string_values(),
            'invalid_price': VAL.float_values(),
            'invalid_about': VAL.string_values(50),
            # 'invalid_measure': self.measure,
            # 'invalid_category_class': self.category,
            'invalid_vendor': VAL.string_values(),
            'invalid_is_stock': VAL.int_values(),
            'invalid_discount': VAL.int_values(1, 50),
            'invalid_is_active': True,
        }

        self.invalid_field_payload_data = {
            'id': 10,
            'name': VAL.json(),
            'price': VAL.string_values(),
            'about': VAL.int_values(50),
            # 'measure': self.measure,
            # 'category_class': self.category,
            'vendor': VAL.int_values(),
            'is_stock': VAL.string_values(),
            'discount': VAL.string_values(),
            'is_active': VAL.string_values(),
        }

        self.valid_field_payload_put = {
            'id': 1,
            'name': VAL.string_values(),
            'price': VAL.float_values(),
            'about': VAL.string_values(50),
            # 'measure': self.measure,
            # 'category_class': self.category,
            'vendor': VAL.string_values(),
            'is_stock': VAL.int_values(),
            'discount': VAL.int_values(51, 60),
            'is_active': True,
        }

    def test_get_all_products(self):
        """Метод получения всех продуктах"""
        response = self.client.get(reverse('api:product'))
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_product(self):
        """Метод получения продукта по id"""
        response = self.client.get(reverse('api:product_detail', kwargs={'id': 1}))
        product = Product.objects.get(pk=1)
        serializer = ProductsSerializer(product)
        assert(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invalid_product(self):
        """Метод получения несуществующего продукта"""
        response = self.client.get(reverse('api:product_detail', kwargs={'id': 6}))
        self.assertEqual(response.data, ER.get_err_message(6, 'Продукт'))

    def test_create_product(self):
        """Метод создания нового продукта"""
        response = self.client.post(
            reverse('api:product'),
            data=json.dumps(self.valid_field_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_product(self):
        """Метод создания нового продукта с неправильно введенными полями"""
        response = self.client.post(
            reverse('api:product'),
            data=json.dumps(self.invalid_field_payload),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_create_invalid_product_data(self):
        """Метод создания нового продукта с неправильно введенными данными"""
        response = self.client.post(
            reverse('api:product'),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_valid_update_product(self):
        """Метод изменения продукта"""
        data = Product.objects.get(pk=1)
        response = self.client.put(
            reverse('api:product_detail',
            kwargs={'id': 1}),
            data=json.dumps(self.valid_field_payload_put),
            content_type='application/json')
        updated_data = Product.objects.get(
            pk=1)
        serializer = ProductsSerializer(data)
        updated_serializer = ProductsSerializer(updated_data)
        self.assertNotEqual(
            serializer.data['discount'], updated_serializer.data['discount'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_product(self):
        """Метод неправильного изменения продукта"""
        response = self.client.put(
            reverse('api:product_detail',
                    kwargs={'id': 1}),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))


class OrdersTests(APITestCase):
    """Класс для тестирования таблицы orders"""

    def setUp(self):
        """Метод для ввода новых записей в тестовую БД"""

        self.user = User.objects.create(
            id=1,
            password=VAL.string_values(),
            is_superuser=False,
            username='User1',
            first_name=VAL.string_values(),
            last_name=VAL.string_values(),
            email='email@mail.ru',
            is_staff=False,
            is_active=True,
        )

        self.district = District.objects.create(
            id=1,
            region_kladr=VAL.string_values(),
            name=VAL.string_values(),
        )

        self.address = Address.objects.create(
            id=1,
            client_id=self.user,
            district=self.district,
            fact_address='fact_address',
            is_active=True,
        )

        self.status = OrderStatus.objects.create(
            id=1,
            status_name=VAL.string_values(50),
        )

        self.payment = OrderPayment.objects.create(
            id=1,
            payment_name=VAL.string_values(50),
        )

        Order.objects.create(
            id=1,
            client_id=self.user,
            status=self.status,
            date_created="2022-12-18T03:50:16.939176Z",
            payment_type=self.payment,
            product_list=VAL.json(),
            total_cost=VAL.int_values(),
            address_id=self.address,
        )

        self.valid_field_payload = {
            'id': 5,
            'date_created': "2022-12-18T03:50:16.939176Z",
            'product_list': VAL.json(),
            'total_cost': VAL.int_values(),
            'address_id': self.address,
            'payment_type': self.payment,
            'client_id': self.user,
            'status': self.status,
        }

        self.invalid_field_payload = {
            'invalid_id': 5,
            'invalid_date_created': "2022-12-18T03:50:16.939176Z",
            'invalid_product_list': VAL.json(),
            'invalid_total_cost': VAL.int_values(),
        }

        self.invalid_field_payload_data = {
            'id': 10,
            'date_created': "2022-12-18T03:50:16.939176Z",
            'product_list': VAL.int_values(),
            'total_cost': VAL.string_values(),
        }

    def test_get_all_orders(self):
        """Метод получения всех заказов"""
        response = self.client.get(reverse('api:orders'))
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_order(self):
        """Метод получения заказа по id"""
        response = self.client.get(reverse('api:order_detail', kwargs={'id': 1}))
        order = Order.objects.get(pk=1)
        serializer = OrderSerializer(order)
        assert(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invalid_order(self):
        """Метод получения несуществующего заказа"""
        response = self.client.get(reverse('api:order_detail', kwargs={'id': 6}))
        self.assertEqual(response.data, ER.get_err_message(6, 'Заказ'))
