from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .utils import reorder_queue
from .serializers import (
    TaskSerializer, OrderSerializer, StatusSerializer, SystemSerializer,
    UserSerializer
)
from tasks.models import Task, Order, Status, System

User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return Task.objects.filter(
                id=self.kwargs.get('pk'), user=self.request.user
            )
        return Task.objects.filter(
            user=self.request.user
        ).order_by('-priority')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        Order.objects.create(task_id=serializer.data['id'], order_number=1)
        Status.objects.create(task_id=serializer.data['id'])
        reorder_queue()

    def perform_update(self, serializer):
        serializer.save()
        if serializer.data.get('priority'):
            reorder_queue()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=["post"], detail=True, url_path="execute",
            url_name="execute_task")
    def execute_task(self, request, pk=None):
        current_status = Status.objects.get(task_id=pk)
        if current_status.status == 'running':
            return Response(data={'error': 'Эта задача уже запущена'},
                            status=status.HTTP_400_BAD_REQUEST)
        if current_status.status == 'deleted':
            return Response(data={
                'error': 'Невозможно изменить удалённую задачу'
            }, status=status.HTTP_400_BAD_REQUEST)
        task = Task.objects.get(id=pk)
        available_system = System.objects.filter(
            active=True, available_threads__gte=task.num_threads
        ).first()
        if available_system:
            available_system.available_threads -= task.num_threads
            task.running_on = available_system
            task.save()
            current_status.status = 'running'
            current_status.save()
            return Response(data={
                'info': 'Ваша задача запущена на выполнение'
            })
        return Response(data={
            'info': 'На данный момент нет свободных машин, попробуйте позже'
        })

    @action(methods=["post"], detail=True, url_path="pause",
            url_name="pause_task")
    def pause_task(self, request, pk=None):
        current_status = Status.objects.get(task_id=pk)
        if current_status.status == 'stopped':
            return Response(data={'error': 'Эта задача уже приостановлена'},
                            status=status.HTTP_400_BAD_REQUEST)
        if current_status.status == 'deleted':
            return Response(data={
                'error': 'Невозможно изменить удалённую задачу'
            }, status=status.HTTP_400_BAD_REQUEST)
        if current_status.status == 'in_queue':
            return Response(data={
                'error': 'Невозможно приостановить не запущенную задачу'
            }, status=status.HTTP_400_BAD_REQUEST)
        task = Task.objects.get(id=pk)
        current_system = System.objects.get(id=task.running_on.id)
        current_system.available_threads += task.num_threads
        task.running_on = None
        current_status.status = 'stopped'
        current_status.save()
        return Response(data={'info': 'Ваша задача приостановлена'})

    @action(methods=["post"], detail=True, url_path="resume",
            url_name="resume_task")
    def resume_task(self, request, pk=None):
        current_status = Status.objects.get(task_id=pk)
        if current_status.status == 'running':
            return Response(data={'error': 'Эта задача уже выполняется'},
                            status=status.HTTP_400_BAD_REQUEST)
        if current_status.status == 'deleted':
            return Response(data={
                'error': 'Невозможно изменить удалённую задачу'
            }, status=status.HTTP_400_BAD_REQUEST)
        task = Task.objects.get(id=pk)
        available_system = System.objects.filter(
            active=True, available_threads__gte=task.num_threads
        ).first()
        if available_system:
            available_system.available_threads -= task.num_threads
            task.running_on = available_system
            task.save()
            current_status.status = 'running'
            current_status.save()
            return Response(data={'info': 'Ваша задача возобновлена'})
        return Response(data={
            'info': 'На данный момент нет свободных машин, попробуйте позже'
        })

    @action(methods=["post"], detail=True, url_path="delete",
            url_name="delete_task")
    def delete_task(self, request, pk=None):
        order = Order.objects.order_by('-order_number').all()
        current_task_order = Order.objects.get(task_id=pk).order_number
        Task.objects.get(id=pk).delete()
        for task in order:
            if task.order_number > current_task_order:
                task.order_number -= 1
        return Response(data={'info': 'Ваша задача удалена'})


class OrderViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            task__user=self.request.user
        ).order_by('order_number')


class StatusViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = StatusSerializer

    def get_queryset(self):
        return Status.objects.filter(
            task__user=self.request.user
        ).order_by('task')


class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    permission_classes = IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = AllowAny

    @action(methods=["post"], detail=False, url_path="login",
            url_name="login")
    def login(self, request):
        if not (request.data.get('password') and request.data.get('username')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(
            User,
            username=request.data.get('username')
        )
        if check_password(request.data.get('password'), user.password):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
