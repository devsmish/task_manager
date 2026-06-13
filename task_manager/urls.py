from django.urls import path
from .views import task_create, task_list, task_detail, task_statistics

urlpatterns = [
    path('tasks/create/', task_create, name='task-create'),
    path('tasks/', task_list, name='task-list'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),
    path('tasks/<int:pk>/', task_detail, name='task-detail'),
]
