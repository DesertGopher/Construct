from django.shortcuts import render
from django.conf import settings
from django.db.models import Q

from api.models import News, UserCart, Product, Profile, Address, District, Order, OrderStatus, ProductCategory
from dashboard.exceptions import *
from .forms import SearchForm


@server_error_decorator
@is_staff_decorator
def index(request):
    profile = Profile.objects.get(client_id=request.user)
    with open(settings.PATH_LOG / f"api_view_logs.txt", encoding="utf-8") as file:
        api_logs = file.read()
    with open(settings.PATH_LOG / f"orders_logs.txt", encoding="utf-8") as file:
        order_logs = file.read()
    with open(settings.PATH_LOG / f"server_logs.txt", encoding="utf-8") as file:
        server_logs = file.read()

    params = {
        'profile': profile,
        'api_logs': api_logs,
        'order_logs': order_logs,
        'server_logs': server_logs
    }

    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = Product.objects.filter(Q(name__icontains=cd['query']))
            # count total results
            total_results = results.count()
            context = {
                **params,
                'form': form,
                'cd': cd,
                'results': results,
                'total_results': total_results
            }
            return render(request, 'crm/index.html', context)

    context = {
        **params,
        'form': form
    }
    if str(request.GET.get('name')) != 'None':
        context['name'] = str(request.GET.get('name'))
    return render(request, 'crm/index.html', context)

