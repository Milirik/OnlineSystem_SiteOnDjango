from django.shortcuts import render

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


def detail_task(request, pk):
    """Выводит информацию о задании"""
    if request.method == 'POST':
        pass
    else:
        task = Task.objects.get(pk=pk)
        ans = StudentCodeModelForm()
        return render(request,
                      'testing_system/detail_task.html',
                      context={'task': task,
                               'ans': ans,
                               })
