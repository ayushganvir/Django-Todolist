from django.db import models
from django.contrib.auth.models import User


# CHANGES SHOULD ALWAYS BE MIGRATED
from django import forms

from todolist.validator import dash_validator


class Todo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    tagged_users = models.ManyToManyField(User, related_name='tagged_todos')
    title = models.CharField(max_length=200, validators=[dash_validator])
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}) {}".format(self.id, self.title)

