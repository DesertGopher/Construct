from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .ex_handler import ExceptionResolver as ER
from .models import *
from django.apps import apps


class Orders(APIView):
    """Класс для работы с таблицей новостей."""

    def get(self, request):
        """Возвращает информацию о всех новостях."""
        data = Order.objects.all()
        if data:
            serializer = OrderSerializer(data, many=True)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)


class Statuses(APIView):
    """Класс для работы с таблицей новостей."""

    def get(self, request):
        """Возвращает информацию о всех новостях."""
        data = OrderStatus.objects.all()
        if data:
            serializer = OrderStatusSerializer(data, many=True)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)


class NewsList(APIView):
    """Класс для работы с таблицей новостей."""

    def get(self, request):
        """Возвращает информацию о всех новостях."""
        data = News.objects.all()
        if data:
            serializer = NewsSerializer(data, many=True)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)

    def post(self, request):
        """Добавляет новость в базу данных """
        try:
            serializer = NewsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Новость успешно добавлен.'})
        except Exception as e:
            return ER.exception_handler(e, 'Новость')


class NewsDetail(APIView):
    """Класс для работы с новостью по id."""

    def get(self, request, id):
        """Получает информацию о новости по id"""
        try:
            data = News.objects.get(id=id)
            serializer = NewsSerializer(data, many=False)
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Новость')

    def put(self, request, id):
        """Редактирует новость по id"""
        if request.data:
            try:
                news = News.objects.get(pk=id)
                serializer = NewsSerializer(news, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'status': True,
                                'message': 'Запись о новости успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Новость')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})


class UserDetail(APIView):
    """Класс для работы с пользователем по id."""
    # permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """Получает информацию о пользователе по id"""
        try:
            data = User.objects.get(id=id)
            serializer = UsersSerializer(data, many=False)
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Пользователь')

    def put(self, request, id):
        """Редактирует пользователя по id"""
        if request.data:
            try:
                user = User.objects.get(pk=id)
                serializer = UsersSerializer(user, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'status': True,
                                'message': 'Запись о пользователе успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Пользователь')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})


class Users(APIView):
    """Класс для работы с таблицей пользователей."""

    def get(self, request):
        """Возвращает информацию о всех пользователях."""
        data = User.objects.all()
        if data:
            serializer = UsersSerializer(data, many=True)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)

    def post(self, request):
        """Добавляет пользователя в базу данных """
        try:
            serializer = UserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Пользователь успешно добавлен.'})
        except Exception as e:
            return ER.exception_handler(e, 'Пользователь')


class IsUserAdmin(APIView):
    """Класс для получения списка суперпользователей."""

    def get(self, request):
        """Возвращает информацию о всех суперпользователях."""
        data = User.objects.filter(is_superuser=True)
        if data:
            serializer = UsersSerializer(data, many=True)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)


class ProductDetail(APIView):
    """Класс для работы с продуктом по id."""

    def get(self, request, id):
        """Получает информацию о продукте по id"""
        try:
            data = Product.objects.get(id=id)
            serializer = ProductsSerializer(data, many=False)
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Продукт')

    def put(self, request, id):
        """Редактирует продукт по id"""
        if request.data:
            try:
                product = Product.objects.get(pk=id)
                serializer = ProductsSerializer(product, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'status': True,
                                'message': 'Запись о продукте успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Продукт')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})

    def delete(self, request, id):
        """Удаляет продукт по id"""
        if request.data:
            try:
                product = Products.objects.get(pk=id)
                product.delete()
            except Exception as e:
                return ER.exception_handler(e, 'Продукт')


class Products(APIView):
    """Класс для работы с таблицей продуктов."""

    def get(self, request):
        """Возвращает информацию о всех продуктах."""
        data = Product.objects.all()
        if data:
            serializer = ProductsSerializer(data, many=True)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)

    def post(self, request):
        """Добавляет продукт в базу данных """
        try:
            serializer = ProductsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Продукт успешно добавлен.'})
        except Exception as e:
            return ER.exception_handler(e, 'Продукт')


class Categories(APIView):
    """Класс для работы с таблицей категорий товаров."""

    def get(self, request):
        """Возвращает информацию о всех категориях."""
        data = ProductCategory.objects.all()
        if data:
            serializer = CategorySerializer(data, many=True)
            return Response(serializer.data)
        else:
            context = ER.get_err_message(2)
            return Response(context)

    def post(self, request):
        """Добавляет категорию в базу данных """
        try:
            serializer = CategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Категория успешно добавлена.'})
        except Exception as e:
            return ER.exception_handler(e, 'Категория')


class CategoryDetail(APIView):
    """Класс для работы с категориями по id."""

    def get(self, request, id):
        """Получает информацию о категории по id"""
        try:
            data = ProductCategory.objects.get(id=id)
            serializer = CategorySerializer(data, many=False)
            return Response(serializer.data)
        except Exception as e:
            return ER.exception_handler(e, 'Категория')

    def put(self, request, id):
        """Редактирует категорию по id"""
        if request.data:
            try:
                category = ProductCategory.objects.get(pk=id)
                serializer = CategorySerializer(category, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'status': True,
                                'message': 'Запись о категории успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Категория')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})


class CartDetail(APIView):
    def put(self, request, id):
        """Загрузка корзины"""
        if request.data:
            try:
                cart = UserCart.objects.get(client_id=id)
                request.data['product_list'] = {"some": "sas"}
                serializer = CartSerializer(cart, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'status': True,
                                'message': 'Запись о категории успешно изменена.'})
            except Exception as e:
                return ER.exception_handler(e, 'Категория')
        else:
            return Response({'status': False, 'message': "Пустой запрос!"})


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
