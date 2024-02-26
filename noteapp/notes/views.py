from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .models import Note, NoteVersion
from .serializers import NoteCreateSerializer, NoteSerializer, NoteVersionSerializer, NoteUpdateSerializer
from rest_framework import serializers

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get('identifier')  # Accepts either email or username
        password = request.data.get('password')

        # Check if the identifier is a valid username or email
        user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()

        if user is not None and user.check_password(password):
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not (username and email and password):
            return Response({'message': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return Response({'success': True, 'message': 'Signup successful'}, status=status.HTTP_201_CREATED)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'success': True, 'message': 'Logout successful'}, status=status.HTTP_200_OK)


class RefreshTokenView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        refresh = RefreshToken(refresh_token)

        return Response({
                'success': True,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)


class CreateNoteView(views.APIView):
    serializer_class = NoteCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content', None)

        modified_data = {'content': content}

        # Create an instance of the serializer with the modified data
        serializer = self.serializer_class(data=modified_data)

        try:
            # Validate and save the serializer
            serializer.is_valid(raise_exception=True)
            note = serializer.save(author=request.user)

            response_data = {
                'success': True,
                'message': 'Note created successfully',
                'note_id': note.id,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:
            # Handle validation errors and return a custom error response
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle other exceptions and return an appropriate error response
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NoteView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Retrieve the note by ID
            note = Note.objects.get(id=id)

            # Check if the requesting user is the owner or one of the shared users
            if request.user == note.author or request.user in note.shared_with.all():
                # Serialize the note content
                serializer = NoteSerializer(note)
                return Response({'success': True, 'note': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Unauthorized access to the note'}, status=status.HTTP_403_FORBIDDEN)

        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, id):
        try:
            # Retrieve the note by ID
            note = Note.objects.get(id=id)

            # Check if the requesting user is the owner or a shared user of the note
            if request.user == note.author or request.user in note.shared_with.all():
                # Get the updated content from the request data
                updated_content = request.data.get('content', None)

                # Use the NoteUpdateSerializer for validation
                serializer = NoteUpdateSerializer(data={'content': updated_content})
                serializer.is_valid(raise_exception=True)

                # Save the current content as a new version
                NoteVersion.objects.create(note=note, content=note.content, updated_at=timezone.now(), updated_by=request.user)

                # Update the note content
                note.content = updated_content
                note.save()

                # Serialize the updated note data
                serializer_note = NoteSerializer(note)
                return Response({'success': True, 'message': 'Note updated successfully', 'note': serializer_note.data}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Unauthorized access to update the note'}, status=status.HTTP_403_FORBIDDEN)

        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)


class ShareNoteView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get note_id and shared_with from the request data
            note_id = request.data.get('note_id')
            shared_with_usernames = request.data.get('shared_with_usernames')

            # Check if shared_with_usernames is not None
            if shared_with_usernames is not None:
                # Retrieve the note by ID
                note = Note.objects.get(id=note_id)

                # Check if the requesting user is the owner of the note
                if request.user == note.author:
                    # Get User instances for the provided usernames
                    shared_with_users = User.objects.filter(username__in=shared_with_usernames)

                    # Share the note with the specified users
                    note.shared_with.set(shared_with_users)

                    # Serialize the updated note data
                    serializer = NoteSerializer(note)
                    return Response({'success': True, 'message': 'Note shared successfully'}, status=status.HTTP_200_OK)

                else:
                    return Response({'error': 'Unauthorized access to share the note'}, status=status.HTTP_403_FORBIDDEN)

            else:
                return Response({'error': 'shared_with_usernames is required'}, status=status.HTTP_400_BAD_REQUEST)

        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)


class NoteVersionHistoryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            # Retrieve the note by ID
            note = Note.objects.get(id=id)

            # Check if the requesting user is the owner or a shared user of the note
            if request.user == note.author or request.user in note.shared_with.all():
                # Retrieve the current version of the note
                current_version = NoteSerializer(note).data

                # Retrieve the version history of the note
                version_history = NoteVersion.objects.filter(note=note).order_by('-updated_at')

                # Serialize the data
                version_history = NoteVersionSerializer(version_history, many=True).data

                return Response({'success': True, 'data': {"current_version": current_version, "history": version_history}}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Unauthorized access to view version history'}, status=status.HTTP_403_FORBIDDEN)

        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)