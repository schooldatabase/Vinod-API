from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from .validation import *


        
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = ('id', 'username', 'email', 'profile_picture', 'bio')
#         # fields = ('id', 'username', 'email')
#         fields = '__all__'
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message_content', 'timestamp', 'is_delivered', 'is_read', 'encrypted_content')

class GroupParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupParticipant
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    participant = GroupParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class CallSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Call
        fields = ('id', 'caller', 'receiver', 'timestamp', 'call_status')

class GroupChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GroupChat
        fields = ('id', 'group', 'sender', 'message_content', 'timestamp', 'encrypted_content')

# Add other serializers for other models (e.g., Photo, Video, Audio, Document, etc.).
class PhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ['user', 'image_file', 'timestamp']

class VideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ['user', 'video_file', 'timestamp']

class AudioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Audio
        fields = ['user', 'audio_file', 'timestamp']

class DocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Document
        fields = ['user', 'document_file', 'timestamp']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        
        
class VoiceCallSerializer(serializers.ModelSerializer):
    # call_status = serializers.CharField(validators=[validate_call_status])
    # call_encryption = serializers.BooleanField(validators=[validate_call_encryption])

    class Meta:
        model = VoiceCall
        fields = ('id', 'caller', 'receiver', 'initiated_at', 'call_status', 'call_encryption')

class VideoCallSerializer(serializers.ModelSerializer):
    # call_status = serializers.CharField(validators=[validate_call_status])
    # call_encryption = serializers.BooleanField(validators=[validate_call_encryption])

    class Meta:
        model = VideoCall
        fields = ('id', 'caller', 'receiver', 'initiated_at', 'call_status', 'call_encryption')
        
class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = '__all__'