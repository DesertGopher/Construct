from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = "api"

urlpatterns = [
    # Менеджмент
    path('', views.index, name='index'),
    path('lists/', views.lists, name='lists'),

    # Пользователи
    path('user/', views.Users.as_view(), name="user"),
    path('superusers/', views.IsUserAdmin.as_view(), name="superusers"),
    path('user-detail/<int:id>/', views.UserDetail.as_view(), name="user_detail"),

    # Продукты
    path('product/', views.Products.as_view(), name="product"),
    path('product-detail/<int:id>/', views.ProductDetail.as_view(), name="product_detail"),

    # Новости
    path('news/', views.NewsList.as_view(), name="news"),
    path('news-detail/<int:id>/', views.NewsDetail.as_view(), name="news_detail"),

    # Заказы
    path('orders/', views.Orders.as_view(), name="orders"),
    path('order-detail/<int:id>/', views.OrderDetail.as_view(), name="order_detail"),
]
