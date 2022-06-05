from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TaskViewSet, OrderViewSet, StatusViewSet, SystemViewSet, UserViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'status', StatusViewSet, basename='status')
router.register(r'moderation/system', SystemViewSet, basename='system_moder')

urlpatterns = [
    path('v1/', include(router.urls))
]
