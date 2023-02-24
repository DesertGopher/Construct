from django.shortcuts import render
from api.models import News, UserCart, Product, Profile, Address, District, Order, OrderStatus, ProductCategory
from modules.exceptions import *


@server_error_decorator
@is_staff_decorator
def index(request):
    profile = Profile.objects.get(client_id=request.user)
    return render(request, 'sharp_draft/index.html', {'profile': profile})
