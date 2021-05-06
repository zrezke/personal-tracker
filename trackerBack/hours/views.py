from django.shortcuts import render
from trackerBack import settings
from rest_framework.response import Response
from .models import Hours
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .serializers import HoursSerializer
from projects.models import Project
from projects.serializers import ProjectSerializer
import datetime
# Create your views here.


class HoursCRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Hours.objects.all()
    serializer_class = HoursSerializer
    
    def get_queryset(self, **kwargs):
        pk = self.kwargs.get("pk")
        project = self.kwargs.get("id")
        if pk:
            return Hours.objects.filter(pk=pk)
        if project:
            return Hours.objects.filter(project=project)
        else:
            return Hours.objects.all()

    def get(self, request, *args, **kwargs):
            hours = self.get_queryset()
            if len(hours) == 0:
                return Response({}, 204)
            data = {"hours": []}
            for hour in hours:
                data["hours"].append(HoursSerializer(hour).data)
            return Response(data, status=200)

    def post(self, request, id):
        project = Project.objects.get(pk=id)
        Hours.objects.create(
            start_time=datetime.datetime.now().isoformat(), project=project)
        hours = self.get_queryset()
        last_hour = hours.last()
        serializer = HoursSerializer(last_hour)
        return Response(serializer.data, status=201)

    def patch(self, request, pk):
        queryset = Hours.objects.filter(pk=pk)
        if queryset:
            queryset.update(end_time=datetime.datetime.now().isoformat())
            return Response({}, 204)
        return Response({"Make sure you entered a valid id", 400})
