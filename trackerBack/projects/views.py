from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Project
from .serializers import ProjectSerializer
from trackerBack import settings
from rest_framework.response import Response

# Create your views here.
class ProjectsListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def delete(self, request, pk):
        project = Project.objects.filter(pk=pk)
        project.delete()
        return Response({}, 204)