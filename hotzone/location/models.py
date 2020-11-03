from django.db import models
from patient.models import Patient


class Location(models.Model):
    objects = models.Manager()
    location = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()

    def __str__(self):
        return self.location
