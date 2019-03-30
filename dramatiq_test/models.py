from django.db import models

# Create your models here.

class AModel(models.Model):
    a_field = models.CharField(max_length=200)