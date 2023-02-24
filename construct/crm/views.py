from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User

from api.models import News, UserCart, Product, Profile, Address, District, Order, OrderStatus, ProductCategory
from modules.exceptions import *
from .forms import SearchForm


# @server_error_decorator
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

