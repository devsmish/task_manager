from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings

from rest_framework import status, filters, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from drf_spectacular.utils import extend_schema

from task_manager.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
    UserRegisterSerializer,
)
from task_manager.models import Task, statuses, SubTask, Category
from task_manager.permissions import IsOwner


def greetings(request: HttpRequest) -> HttpResponse:
    username = 'Serhii'
    return HttpResponse(f"Hello, {username}!")


class TaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.all()

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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated, IsOwner]

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


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        responses={201: UserRegisterSerializer, 400: None},
        description="Endpoint for creating a new user account with secure password hashing."
    )
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully.", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Authenticates user and signs them in by setting access and refresh tokens via httpOnly cookies."
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            response.data = {"detail": "Login successful."}
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            )

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
            )

        return response


class TokenRefreshCookieView(TokenRefreshView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Refreshes access token automatically using the refresh token from httpOnly cookies."
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            )

            refresh_token_new = response.data.get('refresh')
            if refresh_token_new:
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token_new,
                    httponly=True,
                    secure=not settings.DEBUG,
                    samesite='Lax',
                    max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
                )

            response.data = {"detail": "Token refreshed successfully."}

        return response


class UserLogoutView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Logs out the user by blacklisting their refresh token and clearing authentication cookies."
    )
    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')

        return response
