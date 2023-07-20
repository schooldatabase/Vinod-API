from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from .validation import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_picture', 'bio')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'user', 'contact_id')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message_content', 'timestamp', 'is_delivered', 'is_read', 'encrypted_content')

class GroupParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupParticipant
        fields = ('id', 'group', 'participant', 'is_admin')

class GroupSerializer(serializers.ModelSerializer):
    participants = GroupParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'creator', 'group_name', 'participants')

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
    photo_file = serializers.ImageField(validators=[validate_image])

    class Meta:
        model = Image
        fields = ['user', 'photo_file', 'timestamp']

class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.FileField(validators=[validate_video])

    class Meta:
        model = Video
        fields = ['user', 'video_file', 'timestamp']

class AudioSerializer(serializers.ModelSerializer):
    audio_file = serializers.FileField(validators=[validate_audio])

    class Meta:
        model = Audio
        fields = ['user', 'audio_file', 'timestamp']

class DocumentSerializer(serializers.ModelSerializer):
    document_file = serializers.FileField(validators=[validate_document])

    class Meta:
        model = Document
        fields = ['user', 'document_file', 'timestamp']
        
        
class VoiceCallSerializer(serializers.ModelSerializer):
    call_status = serializers.CharField(validators=[validate_call_status])
    call_encryption = serializers.BooleanField(validators=[validate_call_encryption])

    class Meta:
        model = VoiceCall
        fields = ('id', 'caller', 'receiver', 'initiated_at', 'call_status', 'call_encryption')

class VideoCallSerializer(serializers.ModelSerializer):
    call_status = serializers.CharField(validators=[validate_call_status])
    call_encryption = serializers.BooleanField(validators=[validate_call_encryption])

    class Meta:
        model = VideoCall
        fields = ('id', 'caller', 'receiver', 'initiated_at', 'call_status', 'call_encryption')