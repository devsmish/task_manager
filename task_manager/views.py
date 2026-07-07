from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, filters, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
)
from task_manager.models import Task, statuses, SubTask, Category


def greetings(request: HttpRequest) -> HttpResponse:
    username = 'Serhii'
    return HttpResponse(f"Hello, {username}!")


class TaskListCreateView(ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']

    # Изменяем queryset: отдаем только задачи текущего пользователя
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer

    # Автоматически сохраняем текущего пользователя как владельца
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

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


class SubTaskListCreateView(ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        task_count = category.task_set.count()
        return Response({
            'category': category.name,
            'task_count': task_count
        })
