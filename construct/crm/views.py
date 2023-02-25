from datetime import datetime

from django.urls import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpRequest

from modules.serializers import LoadCartSerializer, OrderProducts
from cart.cart import Cart
from shop.forms import OrderEdit
from api.models import Profile, Order, Product, News, ProductCategory, OrderStatus
from modules.exceptions import *
from .forms import *


@server_error_decorator
@is_staff_decorator
def index(request):
    profile = Profile.objects.get(client_id=request.user)
    with open(settings.PATH_LOG / f"api_view_logs.log", encoding="utf-8") as file:
        api_logs = file.read()
    with open(settings.PATH_LOG / f"orders_logs.log", encoding="utf-8") as file:
        order_logs = file.read()
    with open(settings.PATH_LOG / f"server_logs.log", encoding="utf-8") as file:
        server_logs = file.read()
    with open(settings.PATH_LOG / f"logs.log", encoding="utf-8") as file:
        logs = file.read()

    params = {
        'profile': profile,
        'api_logs': api_logs,
        'order_logs': order_logs,
        'server_logs': server_logs,
        'logs': logs
    }

    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            prod_results = Product.objects.filter(Q(name__icontains=cd['query']) |
                                                  Q(vendor__icontains=cd['query']))
            prod_total_results = prod_results.count()

            news_results = News.objects.filter(Q(title__icontains=cd['query']) |
                                               Q(news__icontains=cd['query']))
            news_total_results = news_results.count()

            orders_results = Order.objects.filter(Q(id__icontains=cd['query']))
            orders_total_results = orders_results.count()

            users_results = User.objects.filter(Q(username__icontains=cd['query']) |
                                                Q(first_name__icontains=cd['query']) |
                                                Q(last_name__icontains=cd['query']) |
                                                Q(email__icontains=cd['query']) |
                                                Q(id__icontains=cd['query']))
            users_total_results = users_results.count()

            search_params = {
                'prod_results': prod_results,
                'prod_total_results': prod_total_results,
                'news_results': news_results,
                'news_total_results': news_total_results,
                'orders_results': orders_results,
                'orders_total_results': orders_total_results,
                'users_results': users_results,
                'users_total_results': users_total_results,
            }

            context = {
                **params,
                **search_params,
                'form': form,
                'cd': cd,
            }
            return render(request, 'crm/index.html', context)

    context = {
        **params,
        'form': form
    }

    if str(request.GET.get('name')) != 'None':
        context['name'] = str(request.GET.get('name'))
    return render(request, 'crm/index.html', context)


@server_error_decorator
@is_staff_decorator
def news_edit(request, news_id):
    try:
        new_item = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        message = 'Такой новости не существует.'
        return render(request, 'dashboard/404.html', {'message': message})
    profile = Profile.objects.get(client_id=request.user)

    if request.method == "POST":
        form = NewsEdit(request.POST, request.FILES, instance=new_item)
        if form.is_valid():
            news_form = form.save(commit=False)
            news_form.pub_date = datetime.now()
            news_form.save()
            return HttpResponseRedirect(reverse('crm:news_list'))
    else:
        form = NewsEdit(instance=new_item)
    return render(request, 'crm/news_edit.html', {'form': form,
                                                        'profile': profile,
                                                        'new_item': new_item,
                                                        })


@server_error_decorator
@is_staff_decorator
def products_list(request):
    profile = Profile.objects.get(client_id=request.user)
    products = Product.objects.all().order_by('id')
    categories = ProductCategory.objects.all().order_by('id')
    filter = str(request.GET.get('deleted'))
    restore = str(request.GET.get('restored'))
    context = {
        'profile': profile,
        'products': products,
        'categories': categories,
    }
    if filter != 'None':
        if (isinstance(int(filter), int)):
            product_to_delete = Product.objects.get(id=int(filter))
            product_to_delete.is_active = False
            product_to_delete.save()
            return render(request, 'crm/products_list.html', context)

    if restore != 'None':
        if (isinstance(int(restore), int)):
            product_to_restore = Product.objects.get(id=int(restore))
            product_to_restore.is_active = True
            product_to_restore.save()
            return render(request, 'crm/products_list.html', context)

    return render(request, 'crm/products_list.html', context)


@server_error_decorator
@is_staff_decorator
def product_edit(request, product_id):
    try:
        product_item = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        message = 'Такого продукта нет.'
        return render(request, 'dashboard/404.html', {'message': message})
    profile = Profile.objects.get(client_id=request.user)
    if request.method == "POST":
        form = ProductEdit(request.POST, request.FILES, instance=product_item)
        if form.is_valid():
            product_form = form.save(commit=False)
            product_form.save()
            return HttpResponseRedirect(reverse('crm:products_list'))
    else:
        form = ProductEdit(instance=product_item)
    return render(request, 'crm/product_edit.html', {'form': form,
                                                           'profile': profile,
                                                           'product_item': product_item,
                                                           })


@server_error_decorator
@is_staff_decorator
def create_news(request):
    profile = Profile.objects.get(client_id=request.user)
    assert isinstance(request, HttpRequest)
    form = NewsEdit(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            new_f = form.save(commit=False)
            new_f.pub_date = datetime.now()
            new_f.save()
            return redirect('crm:news_list')
        else:
            form = NewsEdit()
    return render(request, 'crm/create_news.html', {
        'form': form,
        'profile': profile,
    })


@server_error_decorator
@is_staff_decorator
def create_product(request):
    profile = Profile.objects.get(client_id=request.user)
    assert isinstance(request, HttpRequest)
    form = ProductEdit(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            new_f = form.save(commit=False)
            new_f.save()
            return redirect('crm:products_list')
        else:
            form = ProductEdit()
    return render(request, 'crm/create_product.html', {
        'form': form,
        'profile': profile,
    })


@server_error_decorator
@is_staff_decorator
def news_list(request):
    profile = Profile.objects.get(client_id=request.user)
    news = News.objects.all().order_by('id')
    filter = str(request.GET.get('deleted'))
    restore = str(request.GET.get('restored'))
    context = {
        'profile': profile,
        'news': news,
    }
    if filter != 'None':
        if (isinstance(int(filter), int)):
            new_to_delete = News.objects.get(id=int(filter))
            new_to_delete.is_active = False
            new_to_delete.save()
            return render(request, 'crm/news_list.html', context)

    if restore != 'None':
        if (isinstance(int(restore), int)):
            new_to_restore = News.objects.get(id=int(restore))
            new_to_restore.is_active = True
            new_to_restore.save()
            return render(request, 'crm/news_list.html', context)

    return render(request, 'crm/news_list.html', context)


@server_error_decorator
@is_staff_decorator
def user_orders(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    orders_list = Order.objects.all().order_by('-id')
    status1 = OrderStatus.objects.get(status_name="В сборке")
    status2 = OrderStatus.objects.get(status_name="В доставке")
    status3 = OrderStatus.objects.get(status_name="Доставлен")
    status4 = OrderStatus.objects.get(status_name="Отменен")

    profile = Profile.objects.get(client_id=request.user)

    context = {
        'users': users,
        'profiles': profiles,
        'profile': profile,
        'orders_list': orders_list,
        'status1': status1,
        'status2': status2,
        'status3': status3,
        'status4': status4,
    }

    return render(request, 'crm/orders.html', context)


@server_error_decorator
@is_staff_decorator
def user_order_edit(request, order_id):
    cart = Cart(request)
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        message = 'Такого заказа не существует.'
        return render(request, 'dashboard/404.html', {'message': message})

    if request.method == "POST":
        form = OrderEdit(request.POST, instance=order)
        if form.is_valid():
            order_form = form.save(commit=False)
            order_form.save()
            # for prod in cart:
            #     prod['product'].is_stock = int(prod['product'].is_stock) - int(prod['quantity'])
            #     prod['product'].save()
            return HttpResponseRedirect(reverse('crm:orders'))
    else:
        form = OrderEdit(instance=order)

    serializer = OrderProducts(order, many=False)
    keys = serializer.data['product_list'].keys()
    get_keys = []
    amount = []
    for key in keys:
        get_keys.append(int(key))
        amount.append(int(serializer.data['product_list'].get(key)))
    order_products = Product.objects.filter(id__in=get_keys)

    profile = Profile.objects.get(client_id=request.user)
    title = order
    total = float(0)
    len = int(0)
    for product in order_products:
        total += product.get_sale() * amount[len]
        len += 1
    context = {
        'form': form,
        'keys': keys,
        'amount': amount,
        'order_products': order_products,
        'title': title,
        'profile': profile,
        'order': order,
        'cart': cart,
        'total': total,
    }
    return render(request, 'crm/order_edit.html', context)


@server_error_decorator
@is_superuser_decorator
def user_permissions(request):
        profile = Profile.objects.get(client_id=request.user)
        users = User.objects.all().order_by('-is_staff')

        context = {
            'profile': profile,
            'users': users,
        }

        return render(request, 'crm/user_permissions.html', context)


@server_error_decorator
@is_superuser_decorator
def make_user_client(request, user_id):
    target_user = User.objects.get(id=user_id)
    try:
        target_user.is_staff = False
        target_user.is_superuser = False
        target_user.save()
        return redirect('crm:permissions')
    except target_user.username == 'igor':
        return redirect('crm:permissions')


@server_error_decorator
@is_superuser_decorator
def make_user_manager(request, user_id):
    target_user = User.objects.get(id=user_id)
    try:
        target_user.is_staff = True
        target_user.is_superuser = False
        target_user.save()
        return redirect('crm:permissions')
    except target_user.username == 'igor':
        return redirect('crm:permissions')


@server_error_decorator
@is_superuser_decorator
def make_user_superuser(request, user_id):
    target_user = User.objects.get(id=user_id)
    try:
        target_user.is_staff = True
        target_user.is_superuser = True
        target_user.save()
        return redirect('crm:permissions')
    except target_user.username == 'igor':
        return redirect('crm:permissions')

