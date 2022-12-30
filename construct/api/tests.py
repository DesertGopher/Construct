import string
from datetime import date
from typing import Optional
import json

from django.urls import reverse
from django_rest.http import status
from rest_framework import request
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from .serializers import *
from .ex_handler import ExceptionResolver as ER
from .models import *
from .views import *
from rest_framework import permissions
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
        for id in range(1, 4):
            Product.objects.create(
                id=id,
                name=VAL.string_values(),
                price=VAL.float_values(),
                about=VAL.string_values(50),
                measure='шт.',
                category_class=VAL.int_values()
            )

        self.valid_field_payload = {
            'id': 5,
            'name': VAL.string_values(),
            'price': VAL.float_values(),
            'about': VAL.string_values(50),
            'measure': VAL.string_values(),
            'category': VAL.int_values(),
        }

        self.invalid_field_payload = {
            'invalid_id': 5,
            'invalid_name': VAL.string_values(),
            'invalid_price': VAL.float_values(),
            'invalid_about': VAL.string_values(50),
            'invalid_measure': VAL.string_values(),
            'invalid_category': VAL.int_values(),
        }

        self.invalid_field_payload_data = {
            'id': 10,
            'name': VAL.json(),
            'price': VAL.string_values(),
            'about': VAL.int_values(50),
            'measure': VAL.float_values(),
            'category': VAL.string_values(),
        }

        self.valid_field_payload_put = {
            'id': 1,
            'name': VAL.string_values(),
            'price': VAL.float_values(),
            'about': VAL.string_values(50),
            'measure': 'кг.',
            'category': VAL.int_values(),
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
            serializer.data['measure'], updated_serializer.data['measure'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_product(self):
        """Метод неправильного изменения продукта"""
        response = self.client.put(
            reverse('api:product_detail',
                    kwargs={'id': 1}),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))


class BlogsTests(APITestCase):
    """Класс для тестирования таблицы Products"""

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

        Blog.objects.create(
            id=1,
            title=VAL.string_values(),
            description=VAL.string_values(),
            task=VAL.string_values(),
            pub_date='2022-08-30 23:14:35.715464',
            author=self.user
        )

        self.valid_field_payload = {
            'id': 5,
            'title': VAL.string_values(),
            'description': VAL.string_values(),
            'task': VAL.string_values(),
            'pub_date': VAL.string_values(),
            'author': 'User1'
        }

        self.invalid_field_payload = {
            'invalid_id': 5,
            'invalid_title': VAL.string_values(),
            'invalid_description': VAL.string_values(),
            'invalid_task': VAL.string_values(),
            'invalid_pub_date': VAL.string_values(),
            'invalid_author': 'User1'
        }

        self.invalid_field_payload_data = {
            'id': 10,
            'title': VAL.json(),
            'description': VAL.json(),
            'task': VAL.json(),
            'pub_date': VAL.json(),
            'author': VAL.int_values()
        }


    def test_get_all_blogs(self):
        """Метод получения всех блогов"""
        response = self.client.get(reverse('api:blog'))
        blogs = Blog.objects.all()
        serializer = BlogsSerializer(blogs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_product(self):
        """Метод получения блога по id"""
        response = self.client.get(reverse('api:blog_detail', kwargs={'id': 1}))
        blog = Blog.objects.get(pk=1)
        serializer = BlogsSerializer(blog)
        assert(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invalid_blog(self):
        """Метод получения несуществующего блога"""
        response = self.client.get(reverse('api:blog_detail', kwargs={'id': 6}))
        self.assertEqual(response.data, ER.get_err_message(6, 'Блог'))

    def test_create_blog(self):
        """Метод создания нового блога"""
        response = self.client.post(
            reverse('api:blog'),
            data=json.dumps(self.valid_field_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_blog(self):
        """Метод создания нового блога с неправильно введенными полями"""
        response = self.client.post(
            reverse('api:blog'),
            data=json.dumps(self.invalid_field_payload),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_create_invalid_blog_data(self):
        """Метод создания нового блога с неправильно введенными данными"""
        response = self.client.post(
            reverse('api:blog'),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_invalid_update_blog(self):
        """Метод неправильного изменения продукта"""
        response = self.client.put(
            reverse('api:blog_detail',
                    kwargs={'id': 1}),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))


class CommentsTests(APITestCase):
    """Класс для тестирования таблицы Products"""

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

        self.blog = Blog.objects.create(
            id=1,
            title=VAL.string_values(),
            description=VAL.string_values(),
            task=VAL.string_values(),
            pub_date='2022-08-30 23:14:35.715464',
            author=self.user
        )

        Comment.objects.create(
            id=1,
            text=VAL.string_values(),
            pub_date='2022-08-30 23:14:35.715464',
            author=self.user,
            post=self.blog
        )

        self.valid_field_payload = {
            'id': 5,
            'text': VAL.string_values(),
            'pub_date': '2022-08-30 23:14:35.715464',
            'author': 'self.user',
            'post': 'self.blog'
        }

        self.invalid_field_payload = {
            'invalid_id': 5,
            'invalid_text': VAL.string_values(),
            'invalid_pub_date': '2022-08-30 23:14:35.715464',
            'invalid_author': 'self.user',
            'invalid_post': 'self.blog'
        }

        self.invalid_field_payload_data = {
            'id': 10,
            'text': VAL.json(),
            'pub_date': False,
            'author': None,
            'post': True
        }


    def test_get_all_comments(self):
        """Метод получения всех комментариев"""
        response = self.client.get(reverse('api:comment'))
        comments = Comment.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_comment(self):
        """Метод получения комментария по id"""
        response = self.client.get(reverse('api:comment_detail', kwargs={'id': 1}))
        comment = Comment.objects.get(pk=1)
        serializer = CommentsSerializer(comment)
        assert(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invalid_comment(self):
        """Метод получения несуществующего комментария"""
        response = self.client.get(reverse('api:comment_detail', kwargs={'id': 6}))
        self.assertEqual(response.data, ER.get_err_message(6, 'Комментарий'))

    def test_create_comment(self):
        """Метод создания нового комментария"""
        response = self.client.post(
            reverse('api:comment'),
            data=json.dumps(self.valid_field_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_comment(self):
        """Метод создания нового комментария с неправильно введенными полями"""
        response = self.client.post(
            reverse('api:comment'),
            data=json.dumps(self.invalid_field_payload),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_create_invalid_comment_data(self):
        """Метод создания нового комментария с неправильно введенными данными"""
        response = self.client.post(
            reverse('api:comment'),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))

    def test_invalid_update_comment(self):
        """Метод неправильного изменения комментария"""
        response = self.client.put(
            reverse('api:comment_detail',
                    kwargs={'id': 1}),
            data=json.dumps(self.invalid_field_payload_data),
            content_type='application/json')
        self.assertEqual(response.data, ER.get_err_message(4))
