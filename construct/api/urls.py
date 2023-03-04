from django.urls import path
from . import views

app_name = "api"

# Рабочие моменты
manage_urls = [
    path('', views.index, name='index'),
    path('lists/', views.lists, name='lists'),
]

# Клиенты
user_urls = [
    path('user-detail/<int:id>/', views.UserDetail.as_view(), name="user_detail"),
]

# Товары
products_urls = [
    path('product/', views.Products.as_view(), name="product"),
    path('product-detail/<int:id>/', views.ProductDetail.as_view(), name="product_detail"),
]

# Новости
news_urls = [
    path('news/', views.NewsList.as_view(), name="news"),
    path('news-detail/<int:id>/', views.NewsDetail.as_view(), name="news_detail"),
]

# Заказы
orders_urls = [
    path('orders/', views.Orders.as_view(), name="orders"),
    path('order-detail/<int:id>/', views.OrderDetail.as_view(), name="order_detail"),
]

urlpatterns = [
    *manage_urls,
    *user_urls,
    *products_urls,
    *news_urls,
    *orders_urls,
]
