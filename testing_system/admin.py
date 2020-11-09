from django.contrib import admin
from .models import Task, StudentCodeModel, Test

# Register your models here.
admin.site.register(Task)
admin.site.register(StudentCodeModel)
admin.site.register(Test)
