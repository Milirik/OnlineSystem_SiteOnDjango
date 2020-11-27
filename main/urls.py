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


    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset_url'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done_url'),
    path('password/reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm_url'),
    path('password/change/', ForumPasswordChangeView.as_view(), name='password_change_url'),


    path('profile/', profile, name='profile_url'),
    path('profile/change/', ChangeStudentInfoView.as_view(), name='profile_change_url'),
    path('profile/delete/', DeleteStudentView.as_view(), name='profile_delete_url'),
]

