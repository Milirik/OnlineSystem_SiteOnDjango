from django.urls import path, include
from .views import *

app_name = 'testing_system'

urlpatterns = [
    path('', index, name='index_url'),
    path('task/detail/<int:pk>', detail_task, name='detail_url'),
]

