from django.urls import path, include
from .views import *

app_name = 'testing_system'

urlpatterns = [
    path('', index, name='index_url'),

    path('course/all/', CoursesView.as_view(), name='courses_list_url'),
    path('course/user/', UserCoursesView.as_view(), name='user_courses_list_url'),
    path('course/detail/<int:pk>', DetailCourse.as_view(), name='detail_course_url'),
    path('course/create/', create_course, name='create_course_url'),
    path('course/control/', CourseControlView.as_view(), name='course_control_url'),
    path('course/control/tasks', course_control_tasks, name='course_control_tasks_url'),
    path('course/control/<int:pk>/task/create/', create_task, name='create_task_url'),

    path('task/user/', UserTasksView.as_view(), name='user_tasks_list_url'),
    path('task/detail/<int:pk>', DetailTask.as_view(), name='detail_task_url'),


]

