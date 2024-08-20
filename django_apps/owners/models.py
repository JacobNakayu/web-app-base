from django.db import models, connection

import datetime

class Owner(models.Model):
    username = models.CharField(max_length=50, unique=True)