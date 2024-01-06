import re
from django.db import models
from django.contrib.auth.models import User
from .validation import *
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver



# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
#     bio = models.TextField(blank=True)
APP_THEME_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('purple', 'Purple'),
        ('custom', 'Custom'), 
        # Add more themes as needed
    )
LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('fr', 'French'),
        ('es', 'Spanish'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('ja', 'Japanese'),
        ('zh', 'Chinese'),
        # Add more languages as needed
    )
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language =models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    chat_wallpaper = models.ImageField(upload_to='chat_wallpapers/', null=True, blank=True)
    app_theme = models.CharField(max_length=10, choices=APP_THEME_CHOICES, default='light')
    privacy_enabled = models.BooleanField(default=True, validators=[validate_privacy_enabled])
    
    # New Notification Fields
    message_notifications_enabled = models.BooleanField(default=True)
    call_notifications_enabled = models.BooleanField(default=True)
    status_update_notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"User: {self.user.username}, Language: {self.language}, App Theme: {self.app_theme}"

        
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100, null=True,blank=True)
    COUNTRY_CODE_CHOICES = (
        ('+91', 'India'),
        ('+1', 'United States'),
        ('+44', 'United Kingdom'),
        ('+33', 'France'),
        ('+49', 'Germany'),
        ('+34', 'Spain'),
        # Add more countries and codes as needed
    )
    country_code = models.CharField(max_length=5, choices=COUNTRY_CODE_CHOICES, default='+91')
    
   # Define a regex validator specific to Indian phone numbers
    india_phone_regex = RegexValidator(
        regex=r'^\+91[1-9][0-9]{9}$',
        message="Indian phone number must be in the format: '+91XXXXXXXXXX' (10 digits after the country code)."
    )
    phone_number = models.CharField(max_length=15, validators=[india_phone_regex], unique=True)   
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"User: {self.user}"
        
class Group(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    group_name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, through='GroupParticipant')

    
    def __str__(self):
        return self.group_name
    
class GroupParticipant(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"group: {self.group}, participant: {self.participant}"
    
class GroupChat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_messages')
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    encrypted_content = models.TextField(blank=True)
    
    def __str__(self):
        return f"Group: {self.group}, Sender: {self.sender}, Content: {self.message_content[:20]}..."
    
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


# class Call(models.Model):
#     caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_calls')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls')
#     timestamp = models.DateTimeField(auto_now_add=True)
#     call_status = models.CharField(max_length=10)
    
#     def __str__(self):
#         return f"Caller: {self.caller}, Receiver: {self.receiver}, Status: {self.call_status}"


# Add other models as needed (e.g., Photo, Video, Audio, Document, etc.) for media sharing.
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/', validators=[validate_image_extension, validate_image_size])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Image: {self.image_file}"


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/', validators=[validate_video_extension, validate_video_size])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Video: {self.video_file}"
    
class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio/', validators=[validate_audio_extension, validate_audio_size])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Audio: {self.audio_file}"

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='documents/', validators=[validate_document_extension, validate_document_size])
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user}, Document: {self.document_file}"

class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statuses')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

class Call(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_calls')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls')
    call_type = models.CharField(max_length=10)  # 'audio' or 'video'
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_answered = models.BooleanField(default=False)


# Voice and Video Calls
class VoiceCall(models.Model):
    voice_caller = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='voice_calls_made')
    initiated_at = models.DateTimeField(auto_now_add=True)
    call_status = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')])
    
    def __str__(self):
        return f"Caller: {self.caller}, Receiver: {self.receiver}, Status: {self.call_status}"

class VideoCall(models.Model):
    video_caller = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='video_calls_made')
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
    
############### recent history ################
    
 
class StatusRecent(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)
 
class CallRecent(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)  
    
    
############### recent history ################

############### history ################

class ContactHistory(models.Model):
    history = models.TextField(default="{}")
    
class GroupHistory(models.Model):
    history = models.TextField(default="{}")
    
class GroupParticipantHistory(models.Model):
    history = models.TextField(default="{}")
    
class GroupChatHistory(models.Model):
    history = models.TextField(default="{}")
    
class  MessageHistory(models.Model):
    history = models.TextField(default="{}")
    
class CallStatusHistory(models.Model):
    history = models.TextField(default="{}")
    
class VoiceCallHistory(models.Model):
    history = models.TextField(default="{}")
    
class VideoCallHistory(models.Model):
    history = models.TextField(default="{}")
    
class NotificationHistory(models.Model):
    history = models.TextField(default="{}")
    
    
############### history ################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    