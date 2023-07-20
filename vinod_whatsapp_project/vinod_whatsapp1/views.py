from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import *
from .serializers import *
# from .models import User, Message, Group, GroupParticipant, Call, GroupChat, VoiceCall, VideoCall
# from .serializers import UserSerializer, MessageSerializer, GroupSerializer, GroupParticipantSerializer, CallSerializer, GroupChatSerializer, VoiceCallSerializer, VideoCallSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        # Example implementation for user registration
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def login(self, request):
        # Example implementation for user login
        username_email = request.data.get('username_email')
        password = request.data.get('password')
        user = User.objects.filter(Q(username=username_email) | Q(email=username_email)).first()
        if user and user.check_password(password):
            # Perform successful login actions (e.g., create a token, return user data, etc.)
            return Response({'message': 'Login successful!'})
        return Response({'message': 'Invalid credentials'}, status=401)

    @action(detail=True, methods=['patch'])
    def profile(self, request, pk=None):
        # Example implementation for user profile management
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # Implement other actions for group management as needed.
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # Add message delivery and read receipts logic
        message_serializer = self.get_serializer(data=request.data)
        message_serializer.is_valid(raise_exception=True)
        self.perform_create(message_serializer)

        # Update message delivery and read status
        sender = request.user
        receiver = message_serializer.validated_data['receiver']

        # Set is_delivered to True for the sender
        message_serializer.validated_data['is_delivered'] = True
        self.perform_update(message_serializer)

        # Send read receipt to the receiver
        message_queryset = self.queryset.filter(sender=sender, receiver=receiver, is_read=False)
        for message in message_queryset:
            message.is_read = True
            message.save()

        headers = self.get_success_headers(message_serializer.data)
        return Response(message_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # Implement other actions for messaging as needed.

class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    # Implement other actions for voice/video calls as needed.

class GroupChatViewSet(viewsets.ModelViewSet):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer

    # Implement other actions for group chats as needed.

# Add other ViewSets for other models (e.g., Photo, Video, Audio, Document, etc.).
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = PhotoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class VoiceCallViewSet(viewsets.ModelViewSet):
    queryset = VoiceCall.objects.all()
    serializer_class = VoiceCallSerializer

class VideoCallViewSet(viewsets.ModelViewSet):
    queryset = VideoCall.objects.all()
    serializer_class = VideoCallSerializer