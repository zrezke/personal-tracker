from django.contrib.auth.models import User, Group
from .models import Hours
from projects.serializers import ProjectSerializer
from rest_framework import serializers


class HoursSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    get_total_time = serializers.ReadOnlyField()
    class Meta:
        model = Hours
        fields = "__all__"

    def create(self, validated_data):
        return Hours.objects.create(**validated_data)
