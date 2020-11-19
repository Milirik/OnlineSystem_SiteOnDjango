from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView
from django.core.paginator import Paginator
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from testing_system.models import Task, StudentCodeModel
from .models import Student
from .forms import RegisterStudentForm, ChangeStudentInfoForm
from .utilities import signer

from OnlineSystem_SiteOnDjango.receiver import AMQPConsuming


def start():
    """ Переделать обязательно """
    if not AMQPConsuming.flag:
        AMQPConsuming.flag = True
        consumer = AMQPConsuming()
        consumer.daemon = True
        consumer.start()


# Pages
def index(request):
    """Main page"""
    start()
    return render(request, 'main/index.html', context={})


# Views for Users
class LoginView(LoginView):
    """Login"""
    template_name = 'auth/login.html'
    success_url = reverse_lazy('main:profile_url')


class LogoutView(LoginRequiredMixin, LogoutView):
    """Logout"""
    success_url = reverse_lazy('main:index_url')


@login_required
def profile(request):
    """Профиль пользователя"""
    tasks = Task.objects.filter(teacher=request.user)
    submitted_solutions = StudentCodeModel.objects.filter(student=request.user)

    paginator = Paginator(submitted_solutions, 3)
    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)
    print(page.object_list)
    is_paginated = page.has_other_pages()
    prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

    context = {'page_object': page,
               'is_paginated': is_paginated,
               'next_url': next_url,
               'prev_url': prev_url,
               'page': page,
               'tasks': tasks,
               }

    return render(request, 'main/profile.html', context=context)


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


# Восстановление пароля и его изменение
class ForumPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_user_data/password_change.html'
    success_url = reverse_lazy('main:profile_url')
    # success_message = 'Пароль пользователя изменен'


class UserPasswordResetView(PasswordResetView):
    template_name = 'change_user_data/reset_password.html'
    subject_template_name = 'email/reset_password_letter_subject.txt'
    email_template_name = 'email/reset_password_letter_body.txt'
    success_url = reverse_lazy('main:password_reset_done_url')
    # success_message = 'Письмо для восстановления пароля успешно отправлено на почту'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "change_user_data/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'change_user_data/resetconfirm_password.html'
    # post_reset_login = True
    success_url = reverse_lazy('main:index_url')
    # success_message = 'Пароль успешно изменен'


class ChangeStudentInfoView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'change_user_data/change_user_info.html'
    form_class = ChangeStudentInfoForm
    success_url = reverse_lazy('main:profile_url')
    # success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class DeleteStudentView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'change_user_data/delete_user.html'
    success_url = reverse_lazy('main:index_url')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        # messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
