from django.shortcuts import render
from api.models import News, UserCart, Product, Profile, Address, District, Order, OrderStatus, ProductCategory
from dashboard.exceptions import *

from django.conf import settings
from itertools import islice


@server_error_decorator
@is_staff_decorator
def index(request):
    profile = Profile.objects.get(client_id=request.user)
    with open(settings.PATH_LOG / "api_view_logs.txt", encoding="utf-8") as file:
        strings = file.read()
    return render(request, 'crm/index.html', {'profile': profile, 'strings': strings})
