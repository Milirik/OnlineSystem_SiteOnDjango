from abc import ABC

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import FormView, DetailView, ListView, View

import json


from main.models import Student
from .models import Task, StudentCodeModel, Course, CourseStudentAccess
from .forms import StudentCodeModelForm, TaskForm, TestFormSet


# Create your views here.
def index(request):
    return render(request,
                  'testing_system/index.html',
                  context={
                  })


# Курсы
class CoursesView(ListView):
    template_name = 'testing_system/courses_list.html'
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.all()


class DetailCourse(DetailView):
    model = Course
    template_name = 'testing_system/detail_course.html'
    crumbs = [('My Test Breadcrumb', reverse_lazy('main:index_url'))]

# Задания
class TasksView(ListView):
    template_name = 'testing_system/tasks_list.html'
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.all()


class DetailTask(FormView):
    """ Описывает задание и отправляет ответ """
    form_class = StudentCodeModelForm
    template_name = 'testing_system/detail_task.html'

    def get(self, request, pk):
        # print("Гет")
        return self.render_to_response(self.get_context_data())

    def get_initial(self, initial=None):
        """Return the initial data to use for forms on this view."""
        initial = {'code_text': Task.objects.get(pk=self.kwargs['pk']).required_form}
        return initial

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = Task.objects.get(pk=self.kwargs['pk'])
        answers = StudentCodeModel.objects.filter(task=data['task'].pk, student=self.request.user.pk)
        items = []
        for answer in answers:
            items.append(
                {
                    "file": f"{answer.file}",
                    "dispatch_time": f"{answer.dispatch_time}",
                    "status": f"{answer.status}",
                }
            )
        data['answers'] = json.dumps(items)
        return data

    def form_valid(self, form):
        # if user.is_authenticated(): - Сделать проверку на авторизацию
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('testing_system:detail_url', kwargs={'pk': self.kwargs['pk']})


class CreateTask(LoginRequiredMixin, FormView):
    """Создает новое задание"""
    form_class = TaskForm
    template_name = 'testing_system/create_task.html'

    def get(self, request):
        # tasks = list(Task.objects.values())
        # if request.is_ajax():
        #     return JsonResponse({'tasks': tasks}, status=200)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['tests_formset'] = TestFormSet(self.request.POST)
        else:
            data['tests_formset'] = TestFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tests = context['tests_formset']
        with transaction.atomic():
            self.object = form.save()

            if tests.is_valid():
                tests.instance = self.object
                tests.save()
        return super(CreateTask, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('testing_system:index_url')
