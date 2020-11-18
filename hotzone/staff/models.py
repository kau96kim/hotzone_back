from django.db import models


class Staff(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    CHP_staff_number = models.CharField(max_length=7, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email_address = models.CharField(max_length=30, unique=True)

    token = models.CharField(max_length=64,null=True,blank=True)

    def __str__(self):
        return self.username
