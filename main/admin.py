from pprint import pprint
from django.contrib import admin
from django.db.models import F

from .models import Student, Teacher


def gives_the_role_of_teacher(modeladmin, request, queryset):
    pprint(queryset.all())
    for new_teacher in queryset:
        if not new_teacher.has_perm('testing_system.add_task'):
            print(new_teacher)
            tmp = {
                'username': new_teacher.username,
                'first_name': new_teacher.first_name,
                'last_name': new_teacher.last_name,
                'email': new_teacher.email,
                'password': new_teacher.password,
                'date_joined': new_teacher.date_joined,
            }
            new_teacher.delete()
            Teacher.objects.create(**tmp)


gives_the_role_of_teacher.short_description = 'Сделать студента учителем'


class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'username', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'),
              ('password'),
              ('first_name', 'last_name'),
              ('is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 'groups', 'user_permissions',
              ('last_login', 'date_joined')
              )
    readonly_fields = ('last_login', 'date_joined')
    actions = (gives_the_role_of_teacher,)

    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request).exclude(teacher__in=Teacher.objects.all())
        return qs


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'username', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'),
              ('password'),
              ('first_name', 'last_name'),
              ('is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 'groups', 'user_permissions',
              ('last_login', 'date_joined')
              )
    readonly_fields = ('last_login', 'date_joined')


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
