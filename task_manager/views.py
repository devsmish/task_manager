from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView

from task_manager.serializers import (TaskCreateSerializer,
                                      TaskListSerializer,
                                      SubTaskSerializer,
                                      SubTaskCreateSerializer)
from task_manager.models import Task, statuses, SubTask, WeekDay
from django.db.models.functions import ExtractWeekDay
from rest_framework.pagination import PageNumberPagination

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

    day_param = request.query_params.get('day')

    if day_param:
        day_upper = day_param.upper()

        try:
            day_value = WeekDay[day_upper].value
            tasks = tasks.annotate(
                day_of_week=ExtractWeekDay('created_at')
            ).filter(day_of_week=day_value)

        except KeyError:
            valid_days = ", ".join([member.name.lower() for member in WeekDay])
            return Response(
                {"error": f"Invalid day '{day_param}'. Valid options are: {valid_days}."},
                status=status.HTTP_400_BAD_REQUEST
            )

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


# @api_view(['GET'])
# def task_statistics(request):
#     total_tasks = Task.objects.count()
#
#     status_counts = {
#         'new': Task.objects.filter(status='new').count(),
#         'in_progress': Task.objects.filter(status='in_progress').count(),
#         'pending': Task.objects.filter(status='pending').count(),
#         'blocked': Task.objects.filter(status='blocked').count(),
#         'done': Task.objects.filter(status='done').count(),
#     }
#
#     current_time = timezone.now()
#     overdue_tasks = Task.objects.filter(
#         deadline__lt=current_time
#     ).exclude(
#         status='done'
#     ).count()
#
#     statistics_data = {
#         'total_tasks': total_tasks,
#         'status_breakdown': status_counts,
#         'overdue_tasks': overdue_tasks
#     }
#
#     return Response(statistics_data, status=status.HTTP_200_OK)


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


class SubTaskListCreateView(APIView):

    def get(self, request):
        subtasks = SubTask.objects.all().order_by('-created_at')

        task_name = request.query_params.get('task_name')
        status_param = request.query_params.get('status')

        if task_name:
            subtasks = subtasks.filter(task__title__icontains=task_name)

        if status_param:
            subtasks = subtasks.filter(status=status_param)

        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(subtasks, request)

        if page is not None:
            serializer = SubTaskSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):

    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if subtask is None:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if subtask is None:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if subtask is None:
            return Response({"error": "SubTask not found"}, status=status.HTTP_404_NOT_FOUND)

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
