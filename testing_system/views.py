from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from main.models import Student
from .models import Task
from .forms import StudentCodeModelForm


# Create your views here.
def index(request):
    """All tasks"""
    tasks = Task.objects.all()
    return render(request,
                  'testing_system/index.html',
                  context={
                      'tasks': tasks,
                  })


class DetailTask(FormView):
    form_class = StudentCodeModelForm
    # initial = {'student': request.user.pk, 'task': task}
    template_name = 'testing_system/detail_task.html'
    success_url = reverse_lazy('testing_system:index_url')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['task'] = Task.objects.get(pk=self.kwargs['pk'])
        return data

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)