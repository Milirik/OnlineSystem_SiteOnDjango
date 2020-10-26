from django.shortcuts import render
from .models import Task


# Create your views here.
def index(request):
    """All tasks"""
    tasks = Task.objects.all()
    return render(request,
                  'testing_system/index.html',
                  context={
                      'tasks': tasks,
                  })
