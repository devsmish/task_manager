from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer
)
from task_manager.models import Task, statuses, SubTask
from rest_framework.pagination import PageNumberPagination


def greetings(request: HttpRequest) -> HttpResponse:
    username = 'Serhii'
    return HttpResponse(f"Hello, {username}!")


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer


class TaskDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateSerializer
        return TaskDetailSerializer


@api_view(['GET'])
def task_statistics(request):
    total_tasks = Task.objects.count()

    aggregated_status = Task.objects.values('status').annotate(count_items=Count('id'))
    status_counts = {status_key: 0 for status_key, _ in statuses}
    for item in aggregated_status:
        status_field = item['status']
        if status_field in status_counts:
            status_counts[status_field] = item['count_items']

    current_time = timezone.now()
    overdue_tasks = Task.objects.filter(deadline__lt=current_time).exclude(status='done').count()

    statistics_data = {
        'total_tasks': total_tasks,
        'status_breakdown': status_counts,
        'overdue_tasks': overdue_tasks
    }

    return Response(statistics_data, status=status.HTTP_200_OK)


class SubTaskPagination(PageNumberPagination):
    page_size = 5


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    pagination_class = SubTaskPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer
