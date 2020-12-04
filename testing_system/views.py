from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse

from django.views.generic import FormView, DetailView, ListView, View, CreateView

import json


from main.models import Student
from .models import Task, StudentCodeModel, Course, CourseStudentAccess
from .forms import StudentCodeModelForm, TaskForm,  CourseForm, TestFormSet, Test


# Main page
def index(request):
    """Главная страница"""
    return render(request,
                  'testing_system/index.html',
                  context={
                  })


# Курсы
class CoursesView(ListView):
    """Выводит все возможные курсы"""
    template_name = 'testing_system/courses_list.html'
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(is_shown=True)


class UserCoursesView(LoginRequiredMixin, ListView):
    """Выводит курсы, которые принадлежат текущему пользователю"""
    template_name = 'testing_system/user_courses_list.html'
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(Q(coursestudentaccess__student=self.request.user)&
                                     Q(is_shown=True))


class CourseControlView(LoginRequiredMixin, ListView):
    """Контроль курсов. Выводит все курсы и их описание"""
    template_name = 'testing_system/course_control.html'
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)


class CourseControlMembersView(LoginRequiredMixin, ListView):
    """Контроль курсов. Выводит список участников у всех созданных курсов"""
    template_name = 'testing_system/course_control_members.html'
    context_object_name = "courses"

    def post(self, request, *args, **kwargs):
        access_model = CourseStudentAccess.objects.filter(
            Q(student=request.POST.get('student_')) &
            Q(course=request.POST.get('course_'))
        ).first()
        access_model.access = True
        access_model.save()

        return redirect('testing_system:course_control_members_url')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['access_list'] = CourseStudentAccess.objects.all()
        return data

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)


class DetailCourse(DetailView):
    """ Описание курса"""
    model = Course
    template_name = 'testing_system/detail_course.html'
    crumbs = [('My Test Breadcrumb', reverse_lazy('main:index_url'))]

    def post(self, request, *args, **kwargs):
        new_access = CourseStudentAccess()
        new_access.student = self.request.user
        new_access.course = Course.objects.get(pk=self.kwargs.get('pk'))
        new_access.access = True if new_access.course.availability == "true" else False
        new_access.save()
        return redirect('testing_system:detail_course_url', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_active:
            access_model = CourseStudentAccess.objects.filter(Q(student=self.request.user) & Q(course=self.kwargs['pk'])).first()
            data['access_model'] = access_model
        return data


@login_required
def create_course(request):
    """ Создание нового курса """
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            new_access = CourseStudentAccess()
            new_access.student = request.user
            new_access.course = course
            new_access.access = True
            new_access.save()
            return redirect('testing_system:detail_course_url', pk=course.pk)
            # formset = TaskFormSet(request.POST, instance=course)
            # if formset.is_valid():
            #     formset.save()
    else:
        form = CourseForm(initial={'teacher': request.user.pk})
        # formset = TaskFormSet(initial=[
        #     {'teacher': request.user.pk},
        #     {'teacher':  request.user.pk}]
        # )
    context = {
        "form": form,
        # "formset": formset
    }
    return render(request, 'testing_system/create_course.html', context=context)


# При изменении доступности, менять все доступы у учеников
# Доделать formset
@login_required()
def change_course(request, pk):
    """ Изменение данных в курсе """
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            for csa in CourseStudentAccess.objects.filter(course=course):
                csa.access = True
                csa.save()
            return redirect('testing_system:course_control_url')
    else:
        form = CourseForm(initial={
            'teacher': course.teacher,
        },
            instance=course
        )
    context = {'form': form}
    return render(request, 'testing_system/change_course.html', context)


@login_required
def course_control_tasks(request):
    """ Управление заданиями в курсах """
    context = {
        "courses": Course.objects.filter(teacher=request.user)
    }
    return render(request, 'testing_system/control_course_tasks.html', context=context)


# Задания
class UserTasksView(LoginRequiredMixin, ListView):
    """ Вывод всех доступных задач для юзера """
    template_name = 'testing_system/user_tasks_list.html'
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(Q(course__coursestudentaccess__student=self.request.user) &
                                  Q(course__coursestudentaccess__access=True))


class DetailTask(LoginRequiredMixin, FormView):
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
        data['is_solved'] = True if StudentCodeModel.objects.filter(student=self.request.user.pk) else False
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
        return reverse_lazy('testing_system:detail_task_url', kwargs={'pk': self.kwargs['pk']})


@login_required
def create_task(request, pk):
    """ Создает новое задание"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            formset = TestFormSet(request.POST, instance=task)
            if formset.is_valid():
                formset.save()
                return redirect('testing_system:course_control_tasks_url')
    else:
        form = TaskForm(
            initial={
                'teacher': request.user.pk,
                'course': Course.objects.get(pk=pk)
            },
        )
    tests_formset = TestFormSet()

    context = {
        'form': form,
        'formset': tests_formset
    }
    return render(request, 'testing_system/create_task.html', context=context)


# Доделать formset
@login_required()
def change_task(request, pk, pk_task):
    """ Изменение данных в задание """
    task = get_object_or_404(Task, pk=pk_task)
    tests = Test.objects.filter(task=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            formset = TestFormSet(request.POST, request.FILES, instance=task)
            if formset.is_valid():
                formset.save()
                return redirect('testing_system:course_control_tasks_url')
    else:
        form = TaskForm(initial={
                'teacher': task.teacher,
                'course': task.course
            },
            instance=task
        )
    formset = TestFormSet(instance=task)
    context = {'form': form, 'formset': formset}
    return render(request, 'testing_system/change_task.html', context)
