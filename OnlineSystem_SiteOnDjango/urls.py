from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='')),
    path('test_system/', include('testing_system.urls', namespace='')),
]
