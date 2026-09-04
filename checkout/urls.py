# pages/urls.py
from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('order-history/', views.order_history, name='order_history'),
    path('terms/<slug:sculpture_slug>/', views.terms_view, name='terms'),

]
