from django.db import models


class Virus(models.Model):
    objects = models.Manager()
    virus_name = models.CharField(max_length=20, unique=True)
    disease = models.CharField(max_length=20, unique=True)
    max_infectious_period = models.IntegerField()

    def __str__(self):
        return self.virus_name
