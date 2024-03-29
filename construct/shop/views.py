from datetime import datetime

from api.models import (Address, Order, OrderStatus, Product, ProductCategory,
                        Profile, Review, User, UserCart)
from api.views import (CategoryProducts, ProductDetail, Products, SameProducts,
                       UserProfile)
from cart.cart import Cart
from cart.forms import CartAddProductForm
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from loguru import logger
from modules.exceptions import *
from modules.serializers import LoadCartSerializer, OrderProducts

from .forms import OrderCreate, ReviewForm


def get_params(request):
    categories = ProductCategory.objects.all()
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    params = {
        "categories": categories,
        "cart_product_form": cart_product_form,
        "cart": cart,
    }
    return params


@server_error_decorator
def index(request):
    title = "Каталоги"
    context = {**get_params(request), "title": title}
    if request.user.is_active:
        profile = UserProfile().get(request=request, client=request.user)
        context["profile"] = profile

    return render(request, "shop/index.html", context)


@server_error_decorator
def category(request):
    filter = str(request.GET.get("name"))
    if filter:
        product_list = CategoryProducts().get(request=request, filter=int(filter))
        title = ProductCategory.objects.get(id=int(filter)).name
        context = {**get_params(request), "product_list": product_list, "title": title}
    else:
        product_list = Products().get(request=request)
        title = "Все товары"
        context = {**get_params(request), "product_list": product_list, "title": title}
    if request.user.is_active:
        profile = UserProfile().get(request=request, client=request.user)
        context["profile"] = profile
    return render(request, "shop/CategoryLSTK.html", context)


@server_error_decorator
@is_active_decorator
def detail(request, product_id):
    profile = UserProfile().get(request=request, client=request.user)
    reviews = Review.objects.order_by("-pub_date")
    try:
        product = ProductDetail().get(request=request, id=product_id)
    except Product.DoesNotExist:
        message = "Такого товара не существует."
        return render(request, "dashboard/404.html", {"message": message})
    title = str(product.name)
    same_products = SameProducts().get(request=request, filter=product.category_class)
    params = {
        "profile": profile,
        "product": product,
        "title": title,
        "same_products": same_products,
        "reviews": reviews,
    }

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.pub_date = datetime.now()
            comment_f.post = Product.objects.get(pk=product_id)
            comment_f.profile_picture = Profile.objects.get(
                client_id=request.user
            ).profile_picture
            comment_f.save()
            form = ReviewForm()
            context = {**get_params(request), **params, "form": form}
            return render(request, "shop/detail.html", context)

    form = ReviewForm()
    context = {**get_params(request), **params, "form": form}
    return render(request, "shop/detail.html", context)


# @orders_decorator
@is_active_decorator
def create_order(request):
    product_list = UserCart.objects.get(client_id=request.user)
    serializer = LoadCartSerializer(product_list, many=False)
    keys = serializer.data["product_list"].keys()
    get_keys = []
    for key in keys:
        get_keys.append(int(key))
    cart_products = Product.objects.filter(id__in=get_keys)
    addresses = Address.objects.filter(client_id=request.user, is_active=True)

    cart = Cart(request)
    user = User.objects.get(username=request.user)
    profile = UserProfile().get(request=request, client=request.user)
    address_list = Address.objects.filter(client_id=request.user, is_active=True)
    title = "Оформление заказа"

    if not cart.get_all_products():
        message = "Оформление заказа с пустой корзиной невозможно.\n Добавьте товары в корзину."
        return render(request, "dashboard/error_page.html", {"message": message})

    if not addresses:
        message = (
            "Для оформления заказа, у вас должен быть хотя бы один активный адрес."
            "\n Добавьте адрес доставки на странице профиля."
        )
        return render(request, "dashboard/error_page.html", {"message": message})

    for item in cart:
        prod = Product.objects.get(name=item["product"])
        if int(item["quantity"]) > int(prod.is_stock):
            message = "Заказываемые товары превышают количество на складе"
            return render(request, "dashboard/error_page.html", {"message": message})

    if request.method == "POST":
        form = OrderCreate(request.POST, user=request.user)
        if form.is_valid():
            order_form = form.save(commit=False)
            order_form.client_id = request.user
            order_form.status = OrderStatus.objects.get(status_name="В сборке")
            order_form.date_created = datetime.now()
            order_form.product_list = cart.get_all_products()
            order_form.total_cost = cart.get_total_price_cart()
            order_form.save()

            subject = f"Пользователь {request.user} сделал заказ."
            message = (
                f"Номер заказа: {order_form.id}\n"
                f"Клиент: {request.user}\n"
                f"Адрес: {order_form.address_id}\n"
                f"Дата создания заказа клиентом: {order_form.date_created}\n"
                f"Тип оплаты: {order_form.payment_type}\n"
                f"Сумма заказа: {order_form.total_cost} руб\n"
                f"Статус заказа: {order_form.status}"
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                settings.RECIPIENTS_EMAIL,
            )
            for prod in cart:
                prod["product"].is_stock = int(prod["product"].is_stock) - int(
                    prod["quantity"]
                )
                prod["product"].save()
            # order_logger.debug(str('Пользователь ' + str(request.user) + ' сделал заказ №' + str(order_form.id)))
            return HttpResponseRedirect(reverse("shop:orders"))
    form = OrderCreate(user=request.user)

    context = {
        **get_params(request),
        "cart_products": cart_products,
        "user": user,
        "form": form,
        "profile": profile,
        "address_list": address_list,
        "title": title,
    }

    return render(request, "shop/OrderCreate.html", context)


@server_error_decorator
@is_active_decorator
def orders(request):
    orders_list = Order.objects.filter(client_id=request.user).order_by("-id")
    status1 = OrderStatus.objects.get(status_name="В сборке")
    status2 = OrderStatus.objects.get(status_name="В доставке")
    status3 = OrderStatus.objects.get(status_name="Доставлен")
    status4 = OrderStatus.objects.get(status_name="Отменен")
    profile = Profile.objects.get(client_id=request.user)
    statuses = {
        "status1": status1,
        "status2": status2,
        "status3": status3,
        "status4": status4,
    }
    title = "Мои заказы"
    context = {
        **get_params(request),
        **statuses,
        "orders_list": orders_list,
        "title": title,
        "profile": profile,
    }
    return render(request, "shop/orders.html", context)


@server_error_decorator
@is_active_decorator
def order_detail(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, client_id=request.user)
    except Order.DoesNotExist:
        message = "У вас нет такого заказа"
        return render(request, "dashboard/404.html", {"message": message})

    serializer = OrderProducts(order, many=False)
    keys = serializer.data["product_list"].keys()
    get_keys = []
    amount = []
    for key in keys:
        get_keys.append(int(key))
        amount.append(int(serializer.data["product_list"].get(key)))
    order_products = Product.objects.filter(id__in=get_keys)

    profile = UserProfile().get(request=request, client=request.user)
    title = order
    total = float(0)
    len = int(0)
    for product in order_products:
        total += product.get_sale() * amount[len]
        len += 1
    context = {
        **get_params(request),
        "keys": keys,
        "amount": amount,
        "order_products": order_products,
        "title": title,
        "profile": profile,
        "order": order,
        "total": total,
    }
    return render(request, "shop/order_detail.html", context)
