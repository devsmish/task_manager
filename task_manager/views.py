from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from task_manager.serializers import TaskCreateSerializer

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
