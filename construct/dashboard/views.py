from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from api.models import News, UserCart, Product, Profile, Address, District, Order, OrderStatus, ProductCategory
from .forms import *
from .forms import UserCreationForm, AddAddress, UserUpdate, ProductEdit
from api.serializers import LoadCartSerializer, OrderProducts
from cart.cart import Cart
from shop.forms import OrderCreate, OrderEdit
from .exceptions import *


@server_error_decorator
def index(request):
    latest_news = News.objects.filter(is_active=True).order_by('-pub_date')[:3]
    last_news = News.objects.last().id
    context = {
        'latest_news': latest_news,
        'last_news': last_news,
    }
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        context['profile'] = profile

    return render(request, 'dashboard/about.html', context)


@server_error_decorator
def contact(request):
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        return render(request, 'dashboard/contact.html', {'profile': profile})
    else:
        return render(request, 'dashboard/contact.html')


@server_error_decorator
@is_active_decorator
def profile(request):

    user = User.objects.get(username=request.user)
    try:
        profile = Profile.objects.get(client_id=request.user)
    except:
        profile = Profile.objects.create(client_id=request.user)
    address_list = Address.objects.filter(client_id=request.user, is_active=True)

    try:
        product_list = UserCart.objects.get(client_id=request.user)
    except:
        product_list = UserCart.objects.create(client_id=request.user)
    serializer = LoadCartSerializer(product_list, many=False)
    keys = serializer.data['product_list'].keys()
    get_keys = []
    for key in keys:
        get_keys.append(int(key))
    cart_products = Product.objects.filter(id__in=get_keys)[:3]

    filter = str(request.GET.get('deleted'))
    if filter != 'None':
        if (isinstance(int(filter), int)):
            address = Address.objects.get(id=int(filter))
            address.is_active = False
            address.save()

    if request.method == "POST":
        form = AddAddress(request.POST)
        if form.is_valid():
            address_add = form.save(commit=False)
            address_add.client_id = request.user
            address_add.save()
            return render(request, 'dashboard/profile.html', {
                'form': form,
                'user': user,
                'profile': profile,
                'address_list': address_list,
                'cart_products': cart_products,
                      })
    form = AddAddress()

    context = {
        'form': form,
        'user': user,
        'profile': profile,
        'address_list': address_list,
        'cart_products': cart_products,
    }
    return render(request, 'dashboard/profile.html', context)


@server_error_decorator
def reg_form(request):
    assert isinstance(request, HttpRequest)
    regform = UserCreationForm(request.POST)
    if request.method == "POST":
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.is_active = True
            reg_f.save()

            reg_f.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, reg_f)

            cart = UserCart.objects.create(client_id=request.user)
            cart.save()

            prof = Profile.objects.create(client_id=request.user)
            prof.save()

            return redirect('dashboard:home')
    else:
        regform = UserCreationForm()
    return render(request, 'dashboard/registration.html', {
        'regform': regform,
    })


class Logout(LogoutView):
    template_name = 'dashboard/about.html'


class Login(LoginView):
    fields = ['username', 'password']
    template_name = 'dashboard/login.html'
    form_class = AuthUserForm


@server_error_decorator
@is_active_decorator
def update_profile(request):
    profile = get_object_or_404(Profile, client_id=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdate(request.POST, instance=request.user)
        if form.is_valid():
            prof_f = form.save(commit=False)
            prof_f.client_id = request.user
            prof_f.save()
            user_f = user_form.save(commit=False)
            user_f.save()
            return HttpResponseRedirect(reverse('dashboard:profile'))
    else:
        form = ProfileForm(instance=profile)
        user_form = UserUpdate(instance=request.user)
    return render(request, 'dashboard/update_profile.html', {'proform': form,
                                                             'profile': profile,
                                                             'user_form': user_form})


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

    return render(request, 'dashboard/orders.html', context)


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
            return HttpResponseRedirect(reverse('dashboard:orders'))
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
    return render(request, 'dashboard/order_edit.html', context)


@server_error_decorator
@is_superuser_decorator
def user_permissions(request):
        profile = Profile.objects.get(client_id=request.user)
        users = User.objects.all().order_by('-is_staff')

        context = {
            'profile': profile,
            'users': users,
        }

        return render(request, 'dashboard/user_permissions.html', context)


@server_error_decorator
@is_superuser_decorator
def make_user_client(request, user_id):
    target_user = User.objects.get(id=user_id)
    try:
        target_user.is_staff = False
        target_user.is_superuser = False
        target_user.save()
        return redirect('dashboard:permissions')
    except target_user.username == 'igor':
        return redirect('dashboard:permissions')


@server_error_decorator
@is_superuser_decorator
def make_user_manager(request, user_id):
    target_user = User.objects.get(id=user_id)
    try:
        target_user.is_staff = True
        target_user.is_superuser = False
        target_user.save()
        return redirect('dashboard:permissions')
    except target_user.username == 'igor':
        return redirect('dashboard:permissions')


@server_error_decorator
@is_superuser_decorator
def make_user_superuser(request, user_id):
    target_user = User.objects.get(id=user_id)
    try:
        target_user.is_staff = True
        target_user.is_superuser = True
        target_user.save()
        return redirect('dashboard:permissions')
    except target_user.username == 'igor':
        return redirect('dashboard:permissions')


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
            return render(request, 'dashboard/news_list.html', context)

    if restore != 'None':
        if (isinstance(int(restore), int)):
            new_to_restore = News.objects.get(id=int(restore))
            new_to_restore.is_active = True
            new_to_restore.save()
            return render(request, 'dashboard/news_list.html', context)

    return render(request, 'dashboard/news_list.html', context)


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
            return HttpResponseRedirect(reverse('dashboard:news_list'))
    else:
        form = NewsEdit(instance=new_item)
    return render(request, 'dashboard/news_edit.html', {'form': form,
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
            return render(request, 'dashboard/products_list.html', context)

    if restore != 'None':
        if (isinstance(int(restore), int)):
            product_to_restore = Product.objects.get(id=int(restore))
            product_to_restore.is_active = True
            product_to_restore.save()
            return render(request, 'dashboard/products_list.html', context)

    return render(request, 'dashboard/products_list.html', context)


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
            return HttpResponseRedirect(reverse('dashboard:products_list'))
    else:
        form = ProductEdit(instance=product_item)
    return render(request, 'dashboard/product_edit.html', {'form': form,
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
            return redirect('dashboard:news_list')
        else:
            form = NewsEdit()
    return render(request, 'dashboard/create_news.html', {
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
            return redirect('dashboard:products_list')
        else:
            form = ProductEdit()
    return render(request, 'dashboard/create_product.html', {
        'form': form,
        'profile': profile,
    })

