from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.payment_callback, name='payment_callback'),
    path('', views.payment_page, name='payment_page'),
]
