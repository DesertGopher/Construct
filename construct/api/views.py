from django.shortcuts import render
from django.apps import apps
from django.views.decorators.clickjacking import xframe_options_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import AllowAny

from modules.serializers import *
from modules.ex_handler import ExceptionResolver as ER
from .models import *


class Orders(APIView):
    """Класс для работы с таблицей новостей."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="Orders",
                         operation_summary="Выводит информацию о всех заказах пользователей",
                         tags=['Заказы'])
    def get(self, request):
        """Возвращает информацию о всех заказах."""
        data = Order.objects.all()
        if data:
            serializer = OrderSerializer(data, many=True)
            # view_logger.info('Получен список заказов')
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)


class OrderDetail(APIView):
    """Класс для работы с заказом по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="OrderDetail",
                         operation_summary="Выводит информацию о заказе по id заказа",
                         tags=['Заказы'])
    def get(self, request, id):
        """Получает информацию о заказе по id"""
        try:
            data = Order.objects.get(id=id)
            serializer = OrderSerializer(data, many=False)
            # view_logger.info({'order': data, 'id': serializer.data['id']})
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Заказ')


class NewsList(APIView):
    """Класс для работы с таблицей новостей."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="NewsList",
                         operation_summary="Выводит информацию о всех активных новостях",
                         tags=['Новости'])
    def get(self, request):
        """Возвращает информацию о всех новостях."""
        data = News.objects.filter(is_active=True)
        if data:
            serializer = NewsSerializer(data, many=True)
            # view_logger.info('Получен список новостей')
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)

    @swagger_auto_schema(operation_id="NewsList",
                         operation_summary="Создание новости",
                         tags=['Новости'])
    def post(self, request):
        """Добавляет новость в базу данных """
        try:
            serializer = NewsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # view_logger.info({'data': serializer.data, 'message': 'Новость успешно добавлен.'})
            return Response({'data': serializer.data, 'message': 'Новость успешно добавлен.'})
        except Exception as e:
            return ER.exception_handler(e, 'Новость')


class NewsDetail(APIView):
    """Класс для работы с новостью по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="NewsDetail",
                         operation_summary="Выводит информацию о новости по id",
                         tags=['Новости'])
    def get(self, request, id):
        """Получает информацию о новости по id"""
        try:
            data = News.objects.get(id=id)
            serializer = NewsSerializer(data, many=False)
            # view_logger.info({'news': serializer.data['title'], 'id': serializer.data['id']})
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Новость')

    @swagger_auto_schema(operation_id="NewsDetail",
                         operation_summary="Изменяет новость по id",
                         tags=['Новости'])
    def put(self, request, id):
        """Редактирует новость по id"""
        if request.data:
            try:
                news = News.objects.get(pk=id)
                serializer = NewsSerializer(news, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                # view_logger.info({'status': True,
                #                 'message': 'Запись о новости успешно изменена.'})
                return Response({'status': True,
                                'message': 'Запись о новости успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Новость')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})


class UserDetail(APIView):
    """Класс для работы с пользователем по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="UserDetail",
                         operation_summary="Возвращает информацию пользователе по id",
                         tags=['Пользователи'])
    def get(self, request, id):
        """Получает информацию о пользователе по id"""
        try:
            data = User.objects.get(id=id)
            serializer = UsersSerializer(data, many=False)
            # view_logger.info({'user': serializer.data['username'], 'id': serializer.data['id']})
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Пользователь')

    @swagger_auto_schema(operation_id="UserDetail",
                         operation_summary="Изменяет пользователя по id",
                         tags=['Пользователи'])
    def put(self, request, id):
        """Редактирует пользователя по id"""
        if request.data:
            try:
                user = User.objects.get(pk=id)
                serializer = UsersSerializer(user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                # view_logger.info({'status': True,
                #                 'message': 'Запись о пользователе успешно изменена.'})
                return Response({'status': True,
                                'message': 'Запись о пользователе успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Пользователь')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})


class Users(APIView):
    """Класс для работы с таблицей пользователей."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="Users",
                         operation_summary="Возвращает информацию о всех пользователях",
                         tags=['Пользователи'])
    @xframe_options_exempt
    def get(self, request):
        """Возвращает информацию о всех пользователях."""
        data = User.objects.all()
        if data:
            serializer = UsersSerializer(data, many=True)
            # view_logger.info('Получен список пользователей')
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)

    @swagger_auto_schema(operation_id="Users",
                         operation_summary="Создание пользователя",
                         tags=['Пользователи'])
    @xframe_options_exempt
    def post(self, request):
        """Добавляет пользователя в базу данных """
        try:
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # view_logger.info({'data': serializer.data, 'message': 'Пользователь успешно добавлен.'})
            return Response({'data': serializer.data, 'message': 'Пользователь успешно добавлен.'})
        except Exception as e:
            return ER.exception_handler(e, 'Пользователь')


class IsUserAdmin(APIView):
    """Класс для получения списка суперпользователей."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="IsUserAdmin",
                         operation_summary="Возвращает список суперпользователей",
                         tags=['Пользователи'])
    def get(self, request):
        """Возвращает информацию о всех суперпользователях."""
        data = User.objects.filter(is_superuser=True)
        if data:
            serializer = UsersSerializer(data, many=True)
            # view_logger.info(serializer.data)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)


class ProductDetail(APIView):
    """Класс для работы с продуктом по id."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="ProductDetail",
                         operation_summary="Возвращает информацию о товаре по id",
                         tags=['Товары'])
    def get(self, request, id):
        """Получает информацию о продукте по id"""
        try:
            data = Product.objects.get(id=id)
            serializer = ProductsSerializer(data, many=False)
            # view_logger.info({'product': serializer.data['name'], 'id': serializer.data['id']})
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Продукт')

    @swagger_auto_schema(operation_id="ProductDetail",
                         operation_summary="Изменяет товар по id",
                         tags=['Товары'])
    def put(self, request, id):
        """Редактирует продукт по id"""
        if request.data:
            try:
                product = Product.objects.get(pk=id)
                serializer = ProductsSerializer(product, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                # view_logger.info({'status': True,
                #                  'message': 'Запись о продукте успешно изменена.'})
                return Response({'status': True,
                                'message': 'Запись о продукте успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Продукт')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})


class Products(APIView):
    """Класс для работы с таблицей продуктов."""
    permission_classes = [HasAPIKey]

    @swagger_auto_schema(operation_id="Products",
                         operation_summary="Выводит список всех активных товаров",
                         tags=['Товары'])
    def get(self, request):
        """Возвращает информацию о всех продуктах."""
        data = Product.objects.filter(is_active=True)
        if data:
            serializer = ProductsSerializer(data, many=True)
            # view_logger.info('Получен список товаров')
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)

    @swagger_auto_schema(operation_id="Products",
                         operation_summary="Создание товара",
                         tags=['Товары'])
    def post(self, request):
        """Добавляет продукт в базу данных """
        try:
            serializer = ProductsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # view_logger.info({'data': serializer.data, 'message': 'Продукт успешно добавлен.'})
            return Response({'data': serializer.data, 'message': 'Продукт успешно добавлен.'})
        except Exception as e:
            return ER.exception_handler(e, 'Продукт')


def index(request):
    """Метод для отображения главной страницы"""

    models_list = []
    app_models = apps.all_models['api']
    for model in app_models:
        models_list.append(model)
    print(apps.all_models['api'])

    context = {
        'models_list': app_models,
    }
    return render(request, 'api/index.html', context)


def lists(request):
    return render(request, 'api/model_list.html')
