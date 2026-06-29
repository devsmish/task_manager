from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailUpdateDestroyView,
    task_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView
)

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailUpdateDestroyView.as_view(), name='task-detail-update-destroy'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]
