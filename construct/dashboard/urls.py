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
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
