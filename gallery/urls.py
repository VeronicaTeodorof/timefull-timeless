# gallery/urls.py
from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('add_sculpture/', views.add_sculpture, name='add-sculpture'),
]
