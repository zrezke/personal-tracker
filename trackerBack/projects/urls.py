from django.conf.urls import url

from .views import ProjectsListCreateAPIView

urlpatterns = [
    url(r"^$", ProjectsListCreateAPIView.as_view()),
    url(r"^(?P<pk>\d+)/$", ProjectsListCreateAPIView.as_view()),
]