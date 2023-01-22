from django.shortcuts import render
from api.models import News, UserCart, Product, Profile, Address, District, Order, OrderStatus, ProductCategory
from dashboard.exceptions import *

from django.conf import settings
from itertools import islice


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
    context = {
        'profile': profile,
        'api_logs': api_logs,
        'order_logs': order_logs,
        'server_logs': server_logs
    }
    if str(request.GET.get('name')) != 'None':
        context['name'] = str(request.GET.get('name'))
    return render(request, 'crm/index.html', context)
