from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.
class Watchlist(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=250)
    asset_links = ArrayField(models.URLField(), blank=True, size=100)

    def __str__(self):
        return self.name

