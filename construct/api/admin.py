from django.contrib import admin
from api.models import Product
from api.models import ProductCategory
from api.models import News
from api.models import Review
from api.models import Profile
from api.models import UserCart
from api.models import OrderStatus
from api.models import OrderPayment
from api.models import District
from api.models import Address
from api.models import Order
from api.models import Measure


admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(News)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(UserCart)
admin.site.register(OrderStatus)
admin.site.register(OrderPayment)
admin.site.register(District)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Measure)

