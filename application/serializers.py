from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
class StudentApplicationSerializer(ModelSerializer):
    class Meta:
        model = StudentApplicationModel
        fields = "__all__"

class NotificationApplicationSerializer(ModelSerializer):
    class Meta:
        model = NotificationApplicationModel
        fields = "__all__"