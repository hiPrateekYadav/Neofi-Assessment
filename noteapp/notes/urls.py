from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import LoginView, SignupView, LogoutView, CreateNoteView, NoteView, ShareNoteView, NoteVersionHistoryView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('notes/create/', CreateNoteView.as_view(), name='create_note'),
    path('notes/<int:id>/', NoteView.as_view(), name='note'),
    path('notes/share/', ShareNoteView.as_view(), name='share_note'),
    path('notes/version-history/<int:id>/', NoteVersionHistoryView.as_view(), name='note_version'),
]