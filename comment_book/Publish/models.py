
from django.db import models

# Create your models here.


class Publisher(models.Model):
    id_num = models.CharField(max_length=30, primary_key=True, blank=False)
    passWord = models.CharField(max_length=100, blank=False)
    name = models.CharField(max_length=10, blank=False)
    tel = models.CharField(max_length=10, blank=False)
    emailAddr = models.EmailField(max_length=40, blank=False)
