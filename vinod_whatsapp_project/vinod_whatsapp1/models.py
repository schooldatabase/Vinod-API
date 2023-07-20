from django.db import models
from django.contrib.auth.models import User
from .validation import *
# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
#     bio = models.TextField(blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, default='en', validators=[validate_language])
    chat_wallpaper = models.ImageField(upload_to='chat_wallpapers/', null=True, blank=True)
    app_theme = models.CharField(max_length=20, default='light', validators=[validate_app_theme])
    privacy_enabled = models.BooleanField(default=True, validators=[validate_privacy_enabled])
    
    # New Notification Fields
    message_notifications_enabled = models.BooleanField(default=True)
    call_notifications_enabled = models.BooleanField(default=True)
    status_update_notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"User: {self.user.username}, Language: {self.language}, App Theme: {self.app_theme}"


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    contact_id = models.PositiveIntegerField()
    
    def __str__(self):
        return f"User: {self.user}, Contact ID: {self.contact_id}"


class Group(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    group_name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, through='GroupParticipant')
    
    def __str__(self):
        return self.group_name
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages', null=True, blank=True)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    encrypted_content = models.TextField(blank=True)
    # audio_file = models.FileField(upload_to='voice_messages/', null=True, blank=True)
    
    def __str__(self):
        return f"Sender: {self.sender}, Receiver: {self.receiver}, Content: {self.message_content[:20]}..."



class GroupParticipant(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Group: {self.group}, Participant: {self.participant}, Admin: {self.is_admin}"

class Call(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_calls')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls')
    timestamp = models.DateTimeField(auto_now_add=True)
    call_status = models.CharField(max_length=10)
    
    def __str__(self):
        return f"Caller: {self.caller}, Receiver: {self.receiver}, Status: {self.call_status}"

class GroupChat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_messages')
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    encrypted_content = models.TextField(blank=True)
    
    def __str__(self):
        return f"Group: {self.group}, Sender: {self.sender}, Content: {self.message_content[:20]}..."

# Add other models as needed (e.g., Photo, Video, Audio, Document, etc.) for media sharing.
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Image: {self.image_file}"


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Video: {self.video_file}"

class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audios/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Audio: {self.audio_file}"

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='documents/%Y/%m/%d/')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Document: {self.document_file}"


# Voice and Video Calls
class VoiceCall(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_calls_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_calls_received')
    initiated_at = models.DateTimeField(auto_now_add=True)
    call_status = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')])
    
    def __str__(self):
        return f"Caller: {self.caller}, Receiver: {self.receiver}, Status: {self.call_status}"

class VideoCall(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_calls_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_calls_received')
    initiated_at = models.DateTimeField(auto_now_add=True)
    call_status = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')])
    
    def __str__(self):
        return f"Caller: {self.caller}, Receiver: {self.receiver}, Status: {self.call_status}"


class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enable_push_notifications = models.BooleanField(default=True)
    enable_message_notifications = models.BooleanField(default=True)
    enable_call_notifications = models.BooleanField(default=True)
    enable_status_update_notifications = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(blank=True, null=True)
    quiet_hours_end = models.TimeField(blank=True, null=True)
    notification_sound = models.CharField(max_length=100, blank=True, null=True)
    notification_vibration = models.BooleanField(default=True)