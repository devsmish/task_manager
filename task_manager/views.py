from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count

from task_manager.serializers import TaskCreateSerializer, TaskListSerializer
from task_manager.models import Task, statuses

def greetings(request: HttpRequest) -> HttpResponse:
    username = 'Serhii'
    return HttpResponse(f"Hello, {username}!")

@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskListSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def task_detail(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskListSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def task_statistics(request):
    total_tasks = Task.objects.count()

    status_counts = {
        'new': Task.objects.filter(status='new').count(),
        'in_progress': Task.objects.filter(status='in_progress').count(),
        'pending': Task.objects.filter(status='pending').count(),
        'blocked': Task.objects.filter(status='blocked').count(),
        'done': Task.objects.filter(status='done').count(),
    }

    current_time = timezone.now()
    overdue_tasks = Task.objects.filter(
        deadline__lt=current_time
    ).exclude(
        status='done'
    ).count()

    statistics_data = {
        'total_tasks': total_tasks,
        'status_breakdown': status_counts,
        'overdue_tasks': overdue_tasks
    }

    return Response(statistics_data, status=status.HTTP_200_OK)


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
