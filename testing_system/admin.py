from django.contrib import admin
from .models import Task, StudentCodeModel, Test, Course


class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'teacher', 'date_publish')


class StudentCodeModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'student', 'task', 'status')


# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(StudentCodeModel, StudentCodeModelAdmin)
admin.site.register(Course)
admin.site.register(Test)
