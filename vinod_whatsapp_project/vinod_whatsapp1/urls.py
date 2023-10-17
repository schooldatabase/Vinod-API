from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
# router.register(r'users', UserViewSet)
router.register(r'user-settings', UserProfileViewSet) # true
router.register(r'contact', ContactViewSet) # true
router.register(r'groups', GroupViewSet)
router.register(r'gparticipant', GroupParticipantViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'calls', CallViewSet)
router.register(r'group-chats', GroupChatViewSet)

router.register(r'image', PhotoViewSet) # true
router.register(r'videos', VideoViewSet) # true
router.register(r'audios', AudioViewSet) # true
router.register(r'documents', DocumentViewSet) # true

router.register(r'voice-calls', VoiceCallViewSet)
router.register(r'video-calls', VideoCallViewSet)
router.register(r'notification-settings', NotificationSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Add other app URLs as needed.
