from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import EmptyResultSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from modules.serializers import *
from modules.ex_handler import ex_handler, exception_handler
from .models import *


class Orders(APIView):
    """Класс для работы с таблицей заказов."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="Orders",
                         operation_summary="Выводит информацию о всех заказах пользователей",
                         tags=['Заказы'])
    @exception_handler('Заказ')
    def get(self, request):
        """Возвращает информацию о всех заказах."""
        data = Order.objects.all()
        if not data:
            raise EmptyResultSet
        serializer = OrderSerializer(data, many=True)
        return Response(serializer.data)


class OrderDetail(APIView):
    """Класс для работы с заказом по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="OrderDetail",
                         operation_summary="Выводит информацию о заказе по id заказа",
                         tags=['Заказы'])
    @exception_handler('Заказ')
    def get(self, request, id):
        """Получает информацию о заказе по id"""
        data = Order.objects.get(id=id)
        serializer = OrderSerializer(data, many=False)
        return Response(serializer.data)


class NewsList(APIView):
    """Класс для работы с таблицей новостей."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="NewsList",
                         operation_summary="Выводит информацию о всех активных новостях",
                         tags=['Новости'])
    @exception_handler('Новость')
    def get(self, request):
        """Возвращает информацию о всех новостях."""
        data = News.objects.filter(is_active=True).order_by('-pub_date')
        if not data:
            raise EmptyResultSet
        return data

    @swagger_auto_schema(operation_id="NewsList",
                         operation_summary="Создание новости",
                         tags=['Новости'])
    @exception_handler('Новость')
    def post(self, request):
        """Добавляет новость в базу данных """
        serializer = NewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'data': serializer.data,
             'message': 'Новость успешно добавлен.'}
        )


class NewsDetail(APIView):
    """Класс для работы с новостью по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="NewsDetail",
                         operation_summary="Выводит информацию о новости по id",
                         tags=['Новости'])
    @exception_handler('Новость')
    def get(self, request, id):
        """Получает информацию о новости по id"""
        data = News.objects.get(id=id)
        if not data:
            raise EmptyResultSet
        return data

    @swagger_auto_schema(operation_id="NewsDetail",
                         operation_summary="Изменяет новость по id",
                         tags=['Новости'])
    @exception_handler('Новость')
    def put(self, request, id):
        """Редактирует новость по id"""
        news = News.objects.get(pk=id)
        serializer = NewsSerializer(news, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True,
                        'message': 'Запись о новости успешно изменена.'})


class LastNews(APIView):
    """Класс для работы с таблицей новостей"""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="LastNews",
                         operation_summary="Выводит информацию о последней новости",
                         tags=['Новости'])
    @exception_handler('Новость')
    def get(self, request):
        """Получает информацию о последней новости"""
        data = News.objects.filter(is_active=True).last()
        if not data:
            raise EmptyResultSet
        return data


class UserDetail(APIView):
    """Класс для работы с пользователем по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="UserDetail",
                         operation_summary="Возвращает информацию пользователе по id",
                         tags=['Пользователи'])
    @exception_handler('Пользователь')
    def get(self, request, id):
        """Получает информацию о пользователе по id"""
        data = User.objects.get(id=id)
        serializer = UsersSerializer(data, many=False)
        return Response(serializer.data)

    @swagger_auto_schema(operation_id="UserDetail",
                         operation_summary="Изменяет пользователя по id",
                         tags=['Пользователи'])
    @exception_handler('Пользователь')
    def put(self, request, id):
        """Редактирует пользователя по id"""
        user = User.objects.get(pk=id)
        serializer = UsersSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True,
                        'message': 'Запись о пользователе успешно изменена.'})


class ProductDetail(APIView):
    """Класс для работы с продуктом по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="ProductDetail",
                         operation_summary="Возвращает информацию о товаре по id",
                         tags=['Товары'])
    @exception_handler('Товар')
    def get(self, request, id):
        """Получает информацию о продукте по id"""
        data = Product.objects.get(id=id, is_active=True)
        if not data:
            raise EmptyResultSet
        return data

    @swagger_auto_schema(operation_id="ProductDetail",
                         operation_summary="Изменяет товар по id",
                         tags=['Товары'])
    @exception_handler('Товар')
    def put(self, request, id):
        """Редактирует продукт по id"""
        product = Product.objects.get(pk=id)
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': True,
                        'message': 'Запись о товаре успешно изменена.'})


class CategoryProducts(APIView):
    """Класс для работы с таблицей продуктов."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="CategoryProducts",
                         operation_summary="Выводит список всех активных товаров по категории",
                         tags=['Товары'])
    @exception_handler('Товар')
    def get(self, request, filter):
        """Возвращает информацию о продуктах из категории."""
        data = Product.objects.filter(category_class=filter, is_active=True).order_by('-is_stock')
        if not data:
            raise EmptyResultSet
        return data


class SameProducts(APIView):
    """Класс для работы с таблицей продуктов."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="SameProducts",
                         operation_summary="Выводит список рекомендуемых продуктов",
                         tags=['Товары'])
    @exception_handler('Товар')
    def get(self, request, filter):
        """Возвращает информацию о рекомендуемых продуктах."""
        data = Product.objects.filter(category_class=filter, is_active=True).order_by('-discount')[:6]
        if not data:
            raise EmptyResultSet
        return data


class Products(APIView):
    """Класс для работы с таблицей продуктов."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="Products",
                         operation_summary="Выводит список всех активных товаров",
                         tags=['Товары'])
    @exception_handler('Товар')
    def get(self, request):
        """Возвращает информацию о всех продуктах."""
        data = Product.objects.filter(is_active=True).order_by('-discount')
        if not data:
            raise EmptyResultSet
        return data


class UserProfile(APIView):
    @swagger_auto_schema(operation_id="UserProfile",
                         operation_summary="Возвращает профиль пользователя",
                         tags=['Профиль'])
    @exception_handler('Профиль')
    def get(self, request, client):
        """Возвращает информацию о профиле пользователя."""
        data = Profile.objects.get(client_id=client)
        if not data:
            raise EmptyResultSet
        return data


def index(request):
    """Метод для отображения главной страницы"""
    models_list = []
    app_models = apps.all_models['routers']
    for model in app_models:
        models_list.append(model)
    print(apps.all_models['routers'])

    context = {
        'models_list': app_models,
    }
    return render(request, 'routers/index.html', context)


def lists(request):
    return render(request, 'routers/model_list.html')
