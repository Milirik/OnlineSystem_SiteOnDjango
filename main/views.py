from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .models import Student
from .forms import RegisterStudentForm
from .utilities import signer


# Pages
def index(request):
    """Main page"""
    return render(request, 'main/index.html', context={})


# Views for Users
class LoginView(LoginView):
    """Login"""
    template_name = 'auth/login.html'
    success_url = reverse_lazy('main:index_url')


class LogoutView(LoginRequiredMixin, LogoutView):
    """Logout"""
    success_url = reverse_lazy('main:index_url')


class RegisterUserView(CreateView):
    """Register new users"""
    model = Student
    template_name = 'auth/register_user.html'
    form_class = RegisterStudentForm
    success_url = reverse_lazy('main:registration_done_url')


class RegisterUserDoneView(TemplateView):
    """Registration done"""
    template_name = 'auth/register_done.html'


def user_activate(request, sign):
    """Check the user who came from the mail by the link"""
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'auth/bad_signature.html')
    user = get_object_or_404(Student, username=username)
    if user.is_activated:
        template = 'auth/user_is_activated.html'
    else:
        template = 'auth/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)
