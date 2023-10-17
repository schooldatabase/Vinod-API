from django.contrib import admin
from .models import UserProfile, Contact, Group, Message, GroupParticipant, Call, GroupChat, VoiceCall, VideoCall, Image, Video, Audio, Document

# Register models to make them accessible in the Django admin interface
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'privacy_enabled')
    list_filter = ('user',)
    search_fields = ('user__username',)
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # list_display = ('user','name', 'country_code', 'phone_number', 'email')
    list_display = ('user','name', 'country_code', 'phone_number')
    list_filter = ('user',)
    search_fields = ('user__username',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'creator', )
    list_filter = ('creator',)
    search_fields = ('group_name', 'creator__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'group', 'message_content', 'timestamp', 'is_delivered', 'is_read')
    list_filter = ('sender', 'receiver', 'group', 'timestamp', 'is_delivered', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'message_content')

@admin.register(GroupParticipant)
class GroupParticipantAdmin(admin.ModelAdmin):
    list_display = ('group', 'participant',)
    list_filter = ('group', 'participant',)
    search_fields = ('group__group_name', 'participant__username')

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('caller', 'receiver', 'timestamp', 'call_status')
    list_filter = ('caller', 'receiver', 'timestamp', 'call_status')
    search_fields = ('caller__username', 'receiver__username', 'call_status')

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('group', 'sender', 'message_content', 'timestamp', 'encrypted_content')
    list_filter = ('group', 'sender', 'timestamp')
    search_fields = ('group__group_name', 'sender__username', 'message_content')

# Register other media sharing models as needed
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image_file', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'image_file')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_file', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'video_file')

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio_file', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'audio_file')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_file', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'document_file')

@admin.register(VoiceCall)
class VoiceCallAdmin(admin.ModelAdmin):
    list_display = ('caller', 'receiver', 'initiated_at', 'call_status')
    list_filter = ('caller', 'receiver', 'initiated_at', 'call_status')
    search_fields = ('caller__username', 'receiver__username', 'call_status')

@admin.register(VideoCall)
class VideoCallAdmin(admin.ModelAdmin):
    list_display = ('caller', 'receiver', 'initiated_at', 'call_status')
    list_filter = ('caller', 'receiver', 'initiated_at', 'call_status')
    search_fields = ('caller__username', 'receiver__username', 'call_status')
