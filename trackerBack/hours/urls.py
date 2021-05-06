from django.conf.urls import url

from .views import HoursCRUDAPIView

urlpatterns = [
    url(r"^$", HoursCRUDAPIView.as_view()),
    url(r"^(?P<pk>\d+)/$", HoursCRUDAPIView.as_view()),
    url(r"^project/(?P<id>\d+)/$", HoursCRUDAPIView.as_view())
]