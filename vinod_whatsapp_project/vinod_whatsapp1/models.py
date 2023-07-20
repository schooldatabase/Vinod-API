# my_app/models.py
from django.db import models
from django.contrib.auth.models import User

# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
#     bio = models.TextField(blank=True)

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact_id = models.PositiveIntegerField()

class Group(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    group_name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, through='GroupParticipant')
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages', null=True, blank=True)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    encrypted_content = models.TextField(blank=True)


class GroupParticipant(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

class Call(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_calls')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_status = models.CharField(max_length=10)

class GroupChat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_messages')
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    encrypted_content = models.TextField(blank=True)

# Add other models as needed (e.g., Photo, Video, Audio, Document, etc.) for media sharing.
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)

class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audios/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='documents/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)


# Voice and Video Calls
class VoiceCall(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_calls_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_calls_received')
    initiated_at = models.DateTimeField(auto_now_add=True)
    call_status = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')])

class VideoCall(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_calls_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_calls_received')
    initiated_at = models.DateTimeField(auto_now_add=True)
    call_status = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')])
