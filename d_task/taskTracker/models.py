from django.db import models
from django.utils import timezone
import uuid


class Tasks(models.Model):
    STATUS_TYPES = (
        ('ADD', 'add task'),
        ('GET', 'get task'),
        ('FIN', 'finished task'),
    )
    key = models.CharField(max_length=40,unique=True)
    name = models.CharField(max_length=20)
    status = models.CharField(max_length=3,choices=STATUS_TYPES,default='ADD')
    user_id=models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True,null=True)
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True,null=True)


    def __str__(self):
        return self.name