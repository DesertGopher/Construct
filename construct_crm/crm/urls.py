from django.urls import path
from . import views

app_name = 'crm'
urlpatterns = [
    path('', views.index, name='home'),
    # Заказы
    path('orders/', views.user_orders, name='orders'),
    path('order-edit/<int:order_id>/', views.user_order_edit, name='order_edit'),


    path('permissions/', views.user_permissions, name='permissions'),
    path('make-user-client/<int:user_id>/', views.make_user_client, name='make_user_client'),
    path('make-user-manager/<int:user_id>/', views.make_user_manager, name='make_user_manager'),
    path('make-user-superuser/<int:user_id>/', views.make_user_superuser, name='make_user_superuser'),

    # Новости
    path('news-list/', views.news_list, name='news_list'),
    path('news-edit/<int:news_id>/', views.news_edit, name='news_edit'),
    path('create-news/', views.create_news, name='create_news'),
    path('news-detail/<int:news_id>/', views.news_detail, name='news_detail'),

    # Товары
    path('products-list/', views.products_list, name='products_list'),
    path('product-edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('create-product/', views.create_product, name='create_product'),
    path('product-detail/<int:product_id>/', views.product_detail, name='product_detail'),

    # Тех. поддержка
    path('support-list/', views.support_list, name='support_list'),
]
