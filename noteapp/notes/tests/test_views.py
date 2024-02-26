import pytest
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from notes.models import Note  # Update this import
from notes.serializers import NoteCreateSerializer, NoteSerializer  

@pytest.mark.django_db
class NoteAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Log in the user and obtain the access token
        login_response = self.client.post('/login/', {'identifier': 'testuser', 'password': 'testpassword'})
        self.access_token = login_response.data['access']

        # Include the access token in the client's credentials
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Print the request and response
        

    def test_create_note(self):
        data = {'content': 'Test note content'}
        response = self.client.post('/notes/create/', data)
        print(f"Create Note Response: {response.data}")
        assert response.status_code == status.HTTP_201_CREATED
        assert Note.objects.count() == 1

    def test_create_note_invalid_data(self):
        data = {'content': ''}
        response = self.client.post('/notes/create/', data)
        print(f"Create Note Invalid Data Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_note(self):
        note = Note.objects.create(author=self.user, content='Test note content')
        response = self.client.get(f'/notes/{note.id}/')
        print(f"Get Note Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_unauthorized(self):
        other_user = User.objects.create_user(username='other_user', password='testpassword')
        note = Note.objects.create(author=other_user, content='Test note content')
        response = self.client.get(f'/notes/{note.id}/')
        print(f"Get Note Unauthorized Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_note(self):
        note = Note.objects.create(author=self.user, content='Original content')
        updated_data = {'content': 'Updated content'}
        response = self.client.put(f'/notes/{note.id}/', updated_data)
        print(f"Update Note Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(note.content, 'Updated content')

    def test_update_note_invalid_data(self):
        note = Note.objects.create(author=self.user, content='Original content')
        updated_data = {'content': ''}
        response = self.client.put(f'/notes/{note.id}/', updated_data)
        print(f"Update Note Invalid Data Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        note.refresh_from_db()
        self.assertEqual(note.content, 'Original content')
