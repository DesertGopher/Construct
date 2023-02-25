from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse

from api.models import News, UserCart, Product, Profile, Address, Order, OrderStatus, ProductCategory
from .forms import *
from .forms import UserCreationForm, AddAddress, UserUpdate
from modules.serializers import LoadCartSerializer, OrderProducts
from modules.exceptions import *


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
def terms_of_service(request):
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        return render(request, 'dashboard/terms_of_service.html', {'profile': profile})
    else:
        return render(request, 'dashboard/terms_of_service.html')


@server_error_decorator
def privacy_policy(request):
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        return render(request, 'dashboard/privacy_policy.html', {'profile': profile})
    else:
        return render(request, 'dashboard/privacy_policy.html')


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






