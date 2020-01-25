from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.home, name='yanggang-home'),
    path('success', views.success, name='success'),
    path('canceled', views.canceled, name='canceled'),
    path('api/messages/<str:sender>/<str:receiver>', views.MessageList.as_view(), name='message-detail'),
    path('api/messages', views.MessageList.as_view(), name='message-list'),
    path('api/user/<str:username>', views.UserQuery.as_view(), name='user-list'),
    path('api/login', views.Index.as_view(), name='login'),
    path('api/create_user', views.create_user, name='create_user'),
    path('api/token-auth', obtain_auth_token, name='api_token_auth'),
]