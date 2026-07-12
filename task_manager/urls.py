from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from task_manager.views import (
    TaskListCreateView,
    TaskDetailUpdateDestroyView,
    task_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    CategoryViewSet,
    UserRegisterView,
    UserLoginView,
    TokenRefreshCookieView,
    UserLogoutView,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/register/', UserRegisterView.as_view(), name='auth_register'),
    path('auth/login/', UserLoginView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshCookieView.as_view(), name='auth_refresh'),
    path('auth/logout/', UserLogoutView.as_view(), name='auth_logout'),

    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailUpdateDestroyView.as_view(), name='task-detail-update-destroy'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]

# feat(auth): implement user logout and token blacklisting