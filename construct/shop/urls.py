from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:product_id>/", views.detail, name="detail"),
    path("category/", views.category, name="category_lstk"),
    path("create-order/", views.create_order, name="create_order"),
    path("orders/", views.orders, name="orders"),
    path("order-detail/<int:order_id>/", views.order_detail, name="order_detail"),
]
