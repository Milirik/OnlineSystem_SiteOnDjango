from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy


# Create your views here.


def index(request):
    """Main page"""
    return render(request, 'main/index.html', context={})


# Views for Users
class LoginView(LoginView):
    """Вход"""
    template_name = 'auth/login.html'
    success_url = reverse_lazy('main:index_url')


class LogoutView(LoginRequiredMixin, LogoutView):
    """Выход"""
    success_url = reverse_lazy('main:index_url')