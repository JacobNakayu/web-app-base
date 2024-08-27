from django.db import models, connection

import datetime

class User(models.Model):
    a_number = models.CharField(primary_key=True, max_length=9)
    name = models.CharField(max_length=60)
    service_now_id = models.CharField(max_length=64, null=True)
    
    statusChoices = [
        ('DISABLED', 'Disabled'),
        ('ACTIVE', 'Active'),
        ('ADMIN', 'Active Admin')
    ]

    status = models.CharField(max_length=8, choices=statusChoices)