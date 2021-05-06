from django.db import models
import datetime
# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=255, verbose_name="Project name", null=False, blank=False, default="")

    @property
    def get_total_project_time(self):
        def make_time(string):
            splite_time = string.split(":")
            total_time = datetime.timedelta(hours=float(splite_time[0]), minutes=float(splite_time[1]), seconds=float(splite_time[2]))
            return total_time
        
        from hours.models import Hours
        queryset = Hours.objects.filter(project=self.pk)
        total_hours = None
        for index, hour_obj in enumerate(queryset):
            total_time = hour_obj.get_total_time
            if not total_hours:
                if total_time:
                    total_time = make_time(total_time)
                total_hours = total_time
            else:
                if total_time:
                    total_hours += make_time(total_time)
    
        hours, remainder = divmod(total_hours.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
