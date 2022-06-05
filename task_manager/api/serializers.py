from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MaxValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tasks.models import Task, Order, Status, System

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    priority = serializers.IntegerField(validators=(MaxValueValidator(100),))

    class Meta:
        model = Task
        fields = ('id', 'path', 'params', 'num_threads', 'priority')


class OrderSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('task', 'order_number')


class StatusSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Status
        fields = ('task', 'status')

    def get_status(self, status):
        return status.get_status_display()


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_password(self, password):
        encrypted_password = make_password(password)
        checkpassword = check_password(password, encrypted_password)
        if checkpassword:
            return encrypted_password
        raise ValidationError('Не кодируемый пароль')
