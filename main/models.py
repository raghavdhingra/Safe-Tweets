from django.db import models
from django.contrib.postgres.fields import JSONField , ArrayField ,DateTimeRangeField
from django.utils import timezone

# Create your models here.
class SuspectList(models.Model):
    name = models.CharField(max_length = 200, blank=True, null=True,default='raghav')
    suspect_list = ArrayField(models.CharField(max_length=300),default=list,null=True,blank=True)

    def publish(self):
        self.time = timezone.now()
        self.save()

    def __str__(self):
        return self.name