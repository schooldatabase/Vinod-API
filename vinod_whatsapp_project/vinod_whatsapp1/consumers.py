
import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# User = get_user_model()

###################      user profile           ####################


class UserProfileConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.scope["user"].is_authenticated:
            self.close()
            print("Connection message reject , plese login")
        else:
            user_id = self.scope["user"].id
            self.room_name = f"user_{user_id}"
            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            self.accept()
            self.send_user_profile_update(self.scope["user"], "online")
           
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        try:
            user = self.scope["user"]
            self.send_user_profile_update(user, "offline")
            self.close()
        except:
            self.close()

    def receive_json(self, content, **kwargs):
        try:
                
            user = self.scope['user']

            # Update the user's profile and notification settings
            profile, created = UserProfile.objects.get_or_create(user=user)

            profile.language = content.get('language', profile.language)
            profile.app_theme = content.get('app_theme', profile.app_theme)
            profile.privacy_enabled = content.get('privacy_enabled', profile.privacy_enabled)
            profile.message_notifications_enabled = content.get('message_notifications_enabled', profile.message_notifications_enabled)
            profile.call_notifications_enabled = content.get('call_notifications_enabled', profile.call_notifications_enabled)
            profile.status_update_notifications_enabled = content.get('status_update_notifications_enabled', profile.status_update_notifications_enabled)

            # Handle the optional upload of chat wallpaper
            chat_wallpaper = content.get('chat_wallpaper')
            if chat_wallpaper:
                profile.chat_wallpaper = chat_wallpaper
            profile.save()

            # Send a response back to the WebSocket
            self.send_user_profile_update(profile)
        except:
            self.close()

    def send_user_profile_update(self, profile):
        # Send the updated user profile and notification settings to the WebSocket
        data = {
            "language": profile.language,
            "app_theme": profile.app_theme,
            "privacy_enabled": profile.privacy_enabled,
            "message_notifications_enabled": profile.message_notifications_enabled,
            "call_notifications_enabled": profile.call_notifications_enabled,
            "status_update_notifications_enabled": profile.status_update_notifications_enabled,
            "chat_wallpaper": profile.chat_wallpaper.url if profile.chat_wallpaper else None,
        }
        self.send_json(data)


###################      user profile           ####################


###################      contact           ####################

class ContactConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.scope["user"].is_authenticated:
            self.close()
            print("Connection message reject , plese login")
        else:
            user_id = self.scope["user"].id
            self.room_name = f"user_{user_id}"
            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            self.accept()
            self.send_contact_update(self.scope["user"], "online")
           
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        try:
            user = self.scope["user"]
            self.send_contact_update(user, "offline")
            self.close()
        except:
            self.close()

    def receive_json(self, content, **kwargs):
        try:
            user = self.scope['user']
            name = content.get('name', None)
            country_code = content.get('country_code', '+91')
            phone_number = content.get('phone_number', None)
            email = content.get('email', None)

            # Create or update the user's contact
            contact, created = Contact.objects.get_or_create(user=user, phone_number=phone_number)

            contact.name = name
            contact.country_code = country_code
            contact.email = email

            # Validate the Indian phone number
            if country_code == '+91':
                india_phone_regex = RegexValidator(
                    regex=r'^\+91[1-9][0-9]{9}$',
                    message="Indian phone number must be in the format: '+91XXXXXXXXXX' (10 digits after the country code)."
                )
                india_phone_regex(phone_number)

            contact.save()

            # Send a response back to the WebSocket
            self.send_contact_update(contact)
        except:
            self.close()

    def send_contact_update(self, contact):
        # Send the updated contact information to the WebSocket
        data = {
            "name": contact.name,
            "country_code": contact.country_code,
            "phone_number": contact.phone_number,
            "email": contact.email,
        }
        self.send_json(data)


###################      contact           ####################


###################      messager of user           ####################

class MessageConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.scope["user"].is_authenticated:
            self.close()
            print("Connection message reject , plese login")
        else:
            user_id = self.scope["user"].id
            self.room_name = f"user_{user_id}"
            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            self.accept()
            self.chat_message(self.scope["user"], "online")
           
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        try:
            user = self.scope["user"]
            self.chat_message(user, "offline")
            self.close()
        except:
            self.close()

    def receive_json(self, content, **kwargs):
        # Get the message content from the WebSocket

        # Save the message to the database
        # Create a Message object and set its fields
        try:
            message = content['message']
            message_obj = Message.objects.create(
                sender=self.scope['user'],
                receiver=User.objects.get(username=self.room_name),  # Replace with your user lookup logic
                # receiver=User.objects.get(pk=message['receiver_id']),
                message_content=message,
                is_delivered=False,  # Set other fields like 'is_delivered' and 'is_read'
                is_read=False
            )
            message_obj.save()
            # Set is_delivered to True for the sender (optional if you want to handle delivery status)
            message_obj.is_delivered = True
            message_obj.save()
            
            # Send the message to the room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                }
            )
        except:
            self.close()
            
    def chat_message(self, event):
        self.send_json(event["message"])
    
    # def chat_message(self, event):
        
    #     message_content = event['message']
    #       await self.send_json({
    #           "message": message_content
    #       })



###################      messager of user           ####################


###################      status            ####################

class StatusConsumer(JsonWebsocketConsumer):      
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.scope["user"].is_authenticated:
            self.close()
            print("Connection reject , plese login")
        else:
            user_id = self.scope["user"].id
            self.room_name = f"user_{user_id}_statuses"
            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            self.accept()
            self.update_user_status(self.scope["user"], "online")
           
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        try:
            user = self.scope["user"]
            self.update_user_status(user, "offline")
            self.close()
        except:
            self.close()


    def receive_json(self, content, **kwargs):
        user = self.scope['user']
        # Create a new status and save it to the database
        # content = content['content']
        if not self.scope["user"].is_authenticated:
            print("receiver login")
            self.close()
        else:
                
            status = Status(
                user=user,
                content=content,
                # content=content['content'],
            )
            status.save()
        # You can send the status update to the room so that other users can see it
            self.send_group_status(status)

    def send_group_status(self, status):
        group_name = self.room_name
        async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                "type": "status.update",
                "status": {
                    "user_id": status.user.id,
                    "content": status.content,
                    # "content": status.content['content'],
                    "created_at": status.created_at.isoformat(),
                },
            },
        )

    def update_user_status(self, event):
        # Send the status update to the WebSocket
        self.send_json(event["status"])
        
        
        
        
    # def receive_json(self, content):
    #     # Handle incoming WebSocket status updates
    #     status_content = content.get("status_content")
    #     user = self.scope["user"]

    #     if status_content:
    #         self.create_status(user, status_content)


    # def update_user_status(self, user, status):
    #     """
    #     Update the user's status in the database.
    #     `status` can be one of the following status: 'online', 'offline', or 'away'.
    #     """
    #     UserProfile.objects.filter(pk=user.profile.pk).update(status=status)


    # def create_status(self, user, status_content):
    #     """
    #     Create a new status and save it to the database.
    #     """
    #     expires_at = datetime.now() + timedelta(hours=24)  # Adjust the expiration as needed
    #     status = Status(user=user, content=status_content, expires_at=expires_at)
    #     status.save()

  
    # def get_user_statuses(self, user):
    #     """
    #     Retrieve the statuses of all users.
    #     Modify this method to suit your status retrieval needs.
    #     """
    #     return Status.objects.all().filter(expires_at__gte=datetime.now()).order_by('-created_at')[:10]

 
 
    # def update_user_status(self, user, status):
    #   #Update the user's status and trigger the custom signal
    #     user_status_updated.send(sender=self.__class__, user=user, status=status)
    
    # def create_status(self, user, status_content):
    #   # Create a new status and trigger the custom signal
    #     status_created.send(sender=self.__class__, user=user, status_content=status_content)

###################      status            ####################




###################      call : voice call , video call           ####################


class CallConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.scope["user"].is_authenticated:
            self.close()
            print("Connection reject , plese login")
        else:
            user_id = self.scope["user"].id
            self.room_name = f"user_{user_id}_statuses"
            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            self.accept()
            self.send_call_update(self.scope["user"], "online")
           
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        try:
            user = self.scope["user"]
            self.send_call_update(user, "offline")
            self.close()
        except:
            self.close()

    def receive_json(self, content, **kwargs):
        try:
            call_type = content['call_type']
            user = self.scope['user']

            if call_type == 'audio':
                # Handle audio call
                call = Call(
                    caller=user,
                    recipient=User.objects.get(id=content['recipient_id']),
                    call_type=call_type,
                    start_time=content['start_time'],
                    end_time=content['end_time'],
                )
                call.save()

                voice_call = VoiceCall(
                    voice_caller=call,
                    initiated_at=content['initiated_at'],
                    call_status='outgoing',  # Adjust the call status based on your logic
                )
                voice_call.save()

            elif call_type == 'video':
                # Handle video call
                call = Call(
                    caller=user,
                    recipient=User.objects.get(id=content['recipient_id']),
                    call_type=call_type,
                    start_time=content['start_time'],
                    end_time=content['end_time'],
                )
                call.save()

                video_call = VideoCall(
                    video_caller=call,
                    initiated_at=content['initiated_at'],
                    call_status='outgoing',  # Adjust the call status based on your logic
                )
                video_call.save()

            # You can send call updates to the WebSocket
            self.send_call_update(call)
        except:
            self.close()

    def send_call_update(self, call):
        # Send the call update to the WebSocket
        call_type = call.call_type
        if call_type == 'audio':
            voice_call = VoiceCall.objects.get(voice_caller=call)
            data = {
                "call_id": call.id,
                "call_type": call_type,
                "start_time": call.start_time.isoformat(),
                "end_time": call.end_time.isoformat(),
                "call_status": voice_call.call_status,
            }
        elif call_type == 'video':
            video_call = VideoCall.objects.get(video_caller=call)
            data = {
                "call_id": call.id,
                "call_type": call_type,
                "start_time": call.start_time.isoformat(),
                "end_time": call.end_time.isoformat(),
                "call_status": video_call.call_status,
            }
        self.send_json(data)


###################      call : voice call , video call           ####################


###################      notification          ####################

class NotificationSettingsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if not self.scope["user"].is_authenticated:
            self.close()
            print("Connection reject , plese login")
        else:
            user_id = self.scope["user"].id
            self.room_name = f"user_{user_id}_statuses"
            async_to_sync(self.channel_layer.group_add)(
                self.room_name,
                self.channel_name
            )
            self.accept()
            self.send_notification_settings_update(self.scope["user"], "online")
           
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        try:
            user = self.scope["user"]
            self.send_notification_settings_update(user, "offline")
            self.close()
        except:
            self.close()

    def receive_json(self, content, **kwargs):
        try:   
            user = self.scope['user']
            enable_push_notifications = content['enable_push_notifications']
            enable_message_notifications = content['enable_message_notifications']
            enable_call_notifications = content['enable_call_notifications']
            enable_status_update_notifications = content['enable_status_update_notifications']
            quiet_hours_start = content['quiet_hours_start']
            quiet_hours_end = content['quiet_hours_end']
            notification_sound = content['notification_sound']
            notification_vibration = content['notification_vibration']

            # Update the user's notification settings
            notification_settings, created = NotificationSettings.objects.get_or_create(user=user)

            notification_settings.enable_push_notifications = enable_push_notifications
            notification_settings.enable_message_notifications = enable_message_notifications
            notification_settings.enable_call_notifications = enable_call_notifications
            notification_settings.enable_status_update_notifications = enable_status_update_notifications
            notification_settings.quiet_hours_start = quiet_hours_start
            notification_settings.quiet_hours_end = quiet_hours_end
            notification_settings.notification_sound = notification_sound
            notification_settings.notification_vibration = notification_vibration

            notification_settings.save()

            # You can send a response back to the WebSocket
            self.send_notification_settings_update(notification_settings)
        except:
            self.close()

    def send_notification_settings_update(self, notification_settings):
        # Send the updated notification settings to the WebSocket
        data = {
            "enable_push_notifications": notification_settings.enable_push_notifications,
            "enable_message_notifications": notification_settings.enable_message_notifications,
            "enable_call_notifications": notification_settings.enable_call_notifications,
            "enable_status_update_notifications": notification_settings.enable_status_update_notifications,
            "quiet_hours_start": notification_settings.quiet_hours_start.strftime("%H:%M:%S") if notification_settings.quiet_hours_start else None,
            "quiet_hours_end": notification_settings.quiet_hours_end.strftime("%H:%M:%S") if notification_settings.quiet_hours_end else None,
            "notification_sound": notification_settings.notification_sound,
            "notification_vibration": notification_settings.notification_vibration,
        }
        self.send_json(data)

###################      notification          ####################








