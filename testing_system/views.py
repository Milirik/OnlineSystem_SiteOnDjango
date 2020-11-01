from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from main.models import Student
from .models import Task, StudentCodeModel
from .forms import StudentCodeModelForm, TaskForm


# Create your views here.
def index(request):
    """All tasks"""
    tasks = Task.objects.all()
    return render(request,
                  'testing_system/index.html',
                  context={
                      'tasks': tasks,
                  })


# Задания
class DetailTask(FormView):
    form_class = StudentCodeModelForm
    # initial = {'student': request.user.pk, 'task': task}
    template_name = 'testing_system/detail_task.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = Task.objects.get(pk=self.kwargs['pk'])
        data['answers'] = StudentCodeModel.objects.filter(task=data['task'].pk, student=self.request.user.pk)
        return data

    def form_valid(self, form):
        # if user.is_authenticated(): - Сделать проверку на авторизацию
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('testing_system:detail_url', kwargs={'pk': self.kwargs['pk']})


class CreateTask(FormView):
    """Создает новое задание"""
    form_class = TaskForm
    template_name = 'testing_system/create_task.html'

    def form_valid(self, form):
        # if user.is_authenticated(): - Сделать проверку на авторизацию
        print(self.request)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('testing_system:index_url')
