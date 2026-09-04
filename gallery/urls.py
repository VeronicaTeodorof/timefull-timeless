# gallery/urls.py
from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
     path('', views.gallery, name='gallery'),
     path('add_sculpture/', views.add_sculpture, name='add-sculpture'),
     path('sculpture/<slug:slug>/',
          views.sculpture_detail,
          name='sculpture-detail'),
     path('theme/<slug:slug>/edit/',
          views.edit_theme,
          name='edit-theme'),
     path('sculpture/<slug:slug>/edit/',
          views.edit_sculpture,
          name='edit-sculpture'),
     path('sculpture/<slug:slug>/delete/',
          views.delete_sculpture,
          name='delete-sculpture'),
     path('theme/<slug:slug>/', views.theme_detail, name='theme-detail'),
]
