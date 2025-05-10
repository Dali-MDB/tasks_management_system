from rest_framework import serializers
from .models import Task, Project, ContributorRequest

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ContributorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContributorRequest
        fields = '__all__'
