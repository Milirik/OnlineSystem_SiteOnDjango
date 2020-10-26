from django.urls import path, include
from .views import *

app_name = 'main'

urlpatterns = [
    path('', index, name='index_url'),
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),


    path('registration/', RegisterUserView.as_view(), name='registration_url'),
    path('register/done/', RegisterUserDoneView.as_view(), name='registration_done_url'),
    path('registration/activate/<str:sign>/', user_activate, name='registration_activate_url'),


]

