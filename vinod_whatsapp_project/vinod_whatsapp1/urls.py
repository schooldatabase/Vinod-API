from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-settings', UserProfileViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'calls', CallViewSet)
router.register(r'group-chats', GroupChatViewSet)

router.register(r'image', PhotoViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'audios', AudioViewSet)
router.register(r'documents', DocumentViewSet)

router.register(r'voice-calls', VoiceCallViewSet)
router.register(r'video-calls', VideoCallViewSet)
router.register(r'notification-settings', NotificationSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Add other app URLs as needed.
