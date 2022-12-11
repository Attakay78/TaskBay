from django.db import models
from authentication_app.models import AppUser

class Task(models.Model):
    description = models.TextField(null=False)
    task_uploader = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='task_uploader')
    task_taker = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='task_taker')

    def __str__(self):
        return f'Tasker Uploader by {self.task_uploader} and performed by {self.task_taker}'

    __repr__ = __str__
