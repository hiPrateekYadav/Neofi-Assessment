from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, NoteVersion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class NoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    shared_with = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'author', 'content', 'shared_with', 'created_at']

class NoteVersionSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = NoteVersion
        fields = ['note', 'content', 'updated_at', 'updated_by']

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['content', 'shared_with']
        extra_kwargs = {'shared_with': {'write_only': True, 'required': False}}

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['content']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value
