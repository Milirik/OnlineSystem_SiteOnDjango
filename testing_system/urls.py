from django.urls import path, include
from .views import *

app_name = 'testing_system'

urlpatterns = [
    path('', index, name='index_url'),
    path('task/all/', TasksView.as_view(), name='tasks_list_url'),
    path('task/detail/<int:pk>', DetailTask.as_view(), name='detail_task_url'),
    path('task/create/', CreateTask.as_view(), name='create_url'),

    path('course/all/', CoursesView.as_view(), name='courses_list_url'),
    path('course/detail/<int:pk>', DetailCourse.as_view(), name='detail_course_url'),
]

