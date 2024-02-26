from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    shared_with = models.ManyToManyField(User, related_name='shared_notes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)