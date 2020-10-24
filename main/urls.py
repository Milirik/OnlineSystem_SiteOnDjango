from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', index, name='index_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url')
]
