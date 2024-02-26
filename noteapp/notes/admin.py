from django.contrib import admin
from .models import Note, NoteVersion
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(Note)
admin.site.register(NoteVersion)
admin.site.register(Token)