from django.urls import path
from . import views

app_name = 'sharp_draft'
urlpatterns = [
    path('', views.index, name='home'),
    path('create-plate', views.create_plate, name='create_plate'),
    path('templates', views.templates, name='templates'),
    path('create-template', views.create_template, name='create_template'),
    path('xml-encode', views.xml_encode, name='xml_encode'),
]
