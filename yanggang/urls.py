from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='yanggang-home'),
    path('success', views.success, name='success'),
    path('canceled', views.canceled, name='canceled'),
]