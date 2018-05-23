from django.db import models
from django.utils import timezone


class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=40)
    name = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    user_id=models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True,null=True)
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, blank=True,null=True)


    def __str__(self):
        return self.name