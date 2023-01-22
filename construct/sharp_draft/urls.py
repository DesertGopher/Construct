from django.urls import path
from . import views

app_name = 'sharp_draft'
urlpatterns = [
    path('', views.index, name='home'),
]
