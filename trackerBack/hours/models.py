from django.db import models
from projects.models import Project
# Create your models here.

class Hours(models.Model):
    start_time = models.DateTimeField(verbose_name="Start time", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="End time", null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    @property
    def get_total_time(self):
        if self.end_time:
            time = self.end_time - self.start_time
            hours, remainder = divmod(time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            
        else:
            return None