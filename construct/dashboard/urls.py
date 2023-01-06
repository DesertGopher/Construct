from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='home'),
    path('reg_form/', views.reg_form, name='reg_form'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('orders/', views.user_orders, name='orders'),
    path('order-edit/<int:order_id>/', views.user_order_edit, name='order_edit'),
    path('permissions/', views.user_permissions, name='permissions'),
    path('make-user-client/<int:user_id>/', views.make_user_client, name='make_user_client'),
    path('make-user-manager/<int:user_id>/', views.make_user_manager, name='make_user_manager'),
    path('make-user-superuser/<int:user_id>/', views.make_user_superuser, name='make_user_superuser'),
    path('news-list/', views.news_list, name='news_list'),
    path('news-edit/<int:news_id>/', views.news_edit, name='news_edit'),
    path('create-news/', views.create_news, name='create_news'),
    path('products-list/', views.products_list, name='products_list'),
    path('product-edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('create-product/', views.create_product, name='create_product'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
