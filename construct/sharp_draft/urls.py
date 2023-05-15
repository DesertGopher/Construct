from django.urls import path
from . import views

app_name = 'sharp_draft'
urlpatterns = [
    path('', views.index, name='home'),
    path('create-plate', views.create_plate, name='create_plate'),
    path('xml-encode', views.xml_encode, name='xml_encode'),
]
