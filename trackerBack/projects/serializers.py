from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    get_total_project_time = serializers.ReadOnlyField()
    class Meta:
        model = Project
        fields = '__all__'
