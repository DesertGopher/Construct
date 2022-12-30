from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from api.models import Product, Review, ProductCategory, Profile, UserCart, User, Address, Order, OrderStatus
from django.template import loader
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .forms import ReviewForm, OrderCreate, OrderEdit
from datetime import datetime
from api.serializers import LoadCartSerializer, OrderProducts
from django.urls import reverse
from dashboard.exceptions import *


@server_error_decorator
def index(request):
    categories = ProductCategory.objects.all()
    title = 'Каталоги'
    context = {
        'categories': categories,
        'title': title
    }
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        context['profile'] = profile

    return render(request, 'shop/index.html', context)


@server_error_decorator
def category(request):
    cart_product_form = CartAddProductForm()
    filter = str(request.GET.get('name'))
    categories = ProductCategory.objects.all()
    if filter:
        product_list = Product.objects.filter(category_class=int(filter), is_active=True).order_by('-is_stock')
        title = ProductCategory.objects.get(id=int(filter)).name
        context = {
            'categories': categories,
            'product_list': product_list,
            'cart_product_form': cart_product_form,
            'title': title
        }
    else:
        product_list = Product.objects.filter(is_active=True).order_by('-discount')
        title = 'Все товары'
        context = {
            'categories': categories,
            'product_list': product_list,
            'cart_product_form': cart_product_form,
            'title': title
        }
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        context['profile'] = profile
    return render(request, 'shop/CategoryLSTK.html', context)


@server_error_decorator
def detail(request, product_id):
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        reviews = Review.objects.order_by('-pub_date')
        categories = ProductCategory.objects.all()
        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            message = 'Такого товара не существует.'
            return render(request, 'dashboard/404.html', {'message': message})
        cart_product_form = CartAddProductForm()
        title = str(product.name)
        same_products = Product.objects.filter(category_class=product.category_class).order_by('-discount')[:6]

        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                comment_f = form.save(commit=False)
                comment_f.author = request.user
                comment_f.pub_date = datetime.now()
                comment_f.post = Product.objects.get(pk=product_id)
                comment_f.profile_picture = Profile.objects.get(client_id=request.user).profile_picture
                comment_f.save()
                form = ReviewForm()
                context = {'profile': profile,
                           'product': product,
                           'categories': categories,
                           'cart_product_form': cart_product_form,
                           'title': title,
                           'same_products': same_products,
                           'reviews': reviews,
                           'form': form
                           }
                return render(request, 'shop/detail.html', context)
        form = ReviewForm()
        context = {'profile': profile,
                   'categories': categories,
                   'product': product,
                   'cart_product_form': cart_product_form,
                   'title': title,
                   'same_products': same_products,
                   'reviews': reviews,
                   'form': form
                   }

        return render(request, 'shop/detail.html', context)
    else:
        return render(request, 'dashboard/401.html')


@server_error_decorator
def create_order(request):
    if request.user.is_active:
        cart = Cart(request)
        categories = ProductCategory.objects.all()

        product_list = UserCart.objects.get(client_id=request.user)
        serializer = LoadCartSerializer(product_list, many=False)
        keys = serializer.data['product_list'].keys()
        get_keys = []
        for key in keys:
            get_keys.append(int(key))
        cart_products = Product.objects.filter(id__in=get_keys)
        addresses = Address.objects.filter(client_id=request.user, is_active=True)

        user = User.objects.get(username=request.user)
        profile = Profile.objects.get(client_id=request.user)
        address_list = Address.objects.filter(client_id=request.user, is_active=True)
        title = 'Оформление заказа'

        for i in cart:
            print(i['product'].is_stock)
        if not cart.get_all_products():
            message = 'Оформление заказа с пустой корзиной невозможно.\n Добавьте товары в корзину.'
            return render(request, 'dashboard/error_page.html', {'message': message})

        if not addresses:
            message = 'Для оформления заказа, у вас должен быть хотя бы один активный адрес.' \
                      '\n Добавьте адрес доставки на странице профиля.'
            return render(request, 'dashboard/error_page.html', {'message': message})

        for item in cart:
            prod = Product.objects.get(name=item['product'])
            if int(item['quantity']) > int(prod.is_stock):
                message = 'Заказываемые товары превышают количество на складе'
                return render(request, 'dashboard/error_page.html', {'message': message})

        if request.method == "POST":
            form = OrderCreate(request.POST, user=request.user)
            if form.is_valid():
                order_form = form.save(commit=False)
                order_form.client_id = request.user
                order_form.status = OrderStatus.objects.get(status_name='В сборке')
                order_form.date_created = datetime.now()
                order_form.product_list = cart.get_all_products()
                order_form.total_cost = cart.get_total_price_cart()
                order_form.save()
                for prod in cart:
                    prod['product'].is_stock = int(prod['product'].is_stock) - int(prod['quantity'])
                    prod['product'].save()
                return HttpResponseRedirect(reverse('shop:orders'))
        form = OrderCreate(user=request.user)

        context = {
            'categories': categories,
            'cart_products': cart_products,
            'cart': cart,
            'user': user,
            'form': form,
            'profile': profile,
            'address_list': address_list,
            'title': title
        }
        return render(request, 'shop/OrderCreate.html', context)
    else:
        return render(request, 'dashboard/401.html')


@server_error_decorator
def orders(request):
    if request.user.is_active:
        orders_list = Order.objects.filter(client_id=request.user).order_by('-id')
        status1 = OrderStatus.objects.get(status_name="В сборке")
        status2 = OrderStatus.objects.get(status_name="В доставке")
        status3 = OrderStatus.objects.get(status_name="Доставлен")
        status4 = OrderStatus.objects.get(status_name="Отменен")
        profile = Profile.objects.get(client_id=request.user)
        categories = ProductCategory.objects.all()
        title = 'Мои заказы'
        context = {
            'categories': categories,
            'orders_list': orders_list,
            'status1': status1,
            'status2': status2,
            'status3': status3,
            'status4': status4,
            'title': title,
            'profile': profile,
        }
        return render(request, 'shop/orders.html', context)
    else:
        return render(request, 'dashboard/401.html')


@server_error_decorator
def order_detail(request, order_id):
    if request.user.is_active:
        cart = Cart(request)
        try:
            order = Order.objects.get(pk=order_id, client_id=request.user)
        except Order.DoesNotExist:
            message = 'У вас нет такого заказа'
            return render(request, 'dashboard/404.html', {'message': message})

        serializer = OrderProducts(order, many=False)
        keys = serializer.data['product_list'].keys()
        get_keys = []
        amount = []
        for key in keys:
            get_keys.append(int(key))
            amount.append(int(serializer.data['product_list'].get(key)))
        order_products = Product.objects.filter(id__in=get_keys)

        profile = Profile.objects.get(client_id=request.user)
        categories = ProductCategory.objects.all()
        title = order
        total = float(0)
        len = int(0)
        for product in order_products:
            total += product.get_sale() * amount[len]
            len += 1
        context = {
            'categories': categories,
            'keys': keys,
            'amount': amount,
            'order_products': order_products,
            'title': title,
            'profile': profile,
            'order': order,
            'cart': cart,
            'total': total,
        }
        return render(request, 'shop/order_detail.html', context)
    else:
        return render(request, 'dashboard/401.html')
