from django.db import models


class Environment(models.Model):
    ipaddress = models.GenericIPAddressField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

# Create your models here.
