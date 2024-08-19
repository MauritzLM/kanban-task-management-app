from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

import uuid

# board model
class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('board-detail', args=[str(self.id)])
    
    # rewrite save() method to return object
    def save(self, *args, **kwargs):
        # call real save method
        super().save(*args, **kwargs)
        return self
    
# column model
class Column(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    col_name = models.CharField(max_length=50)
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.CASCADE)

    def __str__(self):
        return self.col_name

# task model
class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    column = models.ForeignKey(Column, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # rewrite save() method to return object
    def save(self, *args, **kwargs):
        # call real save method
        super().save(*args, **kwargs)
        return self    

# subtask model
class SubTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sub_name = models.CharField(max_length=50)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_name
