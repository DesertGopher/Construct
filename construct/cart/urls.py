from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("update_cart", views.update_cart, name="update_cart"),
    path("load_cart", views.load_cart, name="load_cart"),
    path("clear_cart", views.clear_cart, name="clear_cart"),
    path("reduce/<int:product_id>/", views.cart_reduce, name="cart_reduce"),
]
