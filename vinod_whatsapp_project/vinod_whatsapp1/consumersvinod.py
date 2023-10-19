# # consumers.py
# import json
# from django.contrib.auth.models import User
# from channels.generic.websocket import JsonAsyncWebsocketConsumer
# from .models import Message


# class ChatConsumer(JsonAsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         if not self.user.is_authenticated:
#             await self.close()
#         else:
#             self.room_name = f"chat_{self.user.id}"
#             await self.channel_layer.group_add(
#                 self.room_name,
#                 self.channel_name
#             )
#             await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_name,
#             self.channel_name
#         )

#     async def receive_json(self, content, **kwargs):
#         message = content.get('message', None)
#         if message:
#             await self.save_message(message)
#             await self.forward_message(message)
            
#         # if self.scope['user'].is_authenticated:
#         #     if message:
#         #         await self.save_message(message)
#         #         await self.forward_message(message)
#         # else:
#         #     self.send_json({
#         #         'message': 'Login Required'
#         #     })

#     async def save_message(self, message_content):
#         # Extract necessary information from message_content (e.g., sender, receiver, group, etc.)
#         # Save the message in the database using Django models
#         # Example implementation:
#         # from .models import Message
#         message = Message(
#             sender=self.user,  # Assuming the authenticated user is the sender
#             receiver=User.objects.get(pk=message_content['receiver_id']),  # Assuming 'receiver_id' is sent in the message_content
#             message_content=message_content['content'],  # Assuming 'content' field contains the message content
#         )
#         message.save()

#         # Set is_delivered to True for the sender (optional if you want to handle delivery status)
#         message.is_delivered = True
#         message.save()

#     async def forward_message(self, message_content):
#         # Assuming you have already defined a WebSocket group for each user
#         receiver_group_name = f"chat_{message_content['receiver_id']}"

#         # Send the message to the receiver's WebSocket group
#         await self.channel_layer.group_send(
#             receiver_group_name,
#             {
#                 "type": "chat.message",
#                 "message": message_content
#             }
#         )
    

#     async def chat_message(self, event):
#         # Send the received message to the WebSocket
#         message_content = event['message']
#         await self.send_json({
#             "message": message_content
#         })


#     async def send_call_notification(self, event):
#         # Send call notification to the connected client
#         call_info = event['call_info']
#         await self.send_json({
#             'type': 'call_notification',
#             'call_info': call_info,
#         })

#     async def send_status_update_notification(self, event):
#         # Send status update notification to the connected client
#         status_update = event['status_update']
#         await self.send_json({
#             'type': 'status_update_notification',
#             'status_update': status_update,
#         })



############################################################# models file content ################################################################################

# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages', null=True, blank=True)
#     message_content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_delivered = models.BooleanField(default=False)
#     is_read = models.BooleanField(default=False)
#     encrypted_content = models.TextField(blank=True)

# drf whatsapp clone with channels JsonWebSocketConsumerall fields  save database  explain code wise only consumers file full details with example

############################################################# models file content ################################################################################


####################################################################################




# import json
# from channels.generic.websocket import JsonWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# from .models import Message

# User = get_user_model()

# class ChatConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         # WebSocket connection authentication
#         if self.scope["user"].is_anonymous:
#             self.close()
#         else:
#             # Join a room, which can be based on user IDs or group IDs
#             user_id = self.scope["user"].id
#             self.room_name = f"user_{user_id}"
#             async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
#             self.accept()

#     def disconnect(self, close_code):
#         # WebSocket disconnect
#         async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

#     def receive_json(self, content, **kwargs):
#         # Handle incoming WebSocket messages
#         message_content = content['message']
#         user = self.scope['user']
#         # Handle and process the message here
#         # Save the message to the database
#         message = Message(
#             sender=user,
#             receiver=User.objects.get(id=content['receiver_id']),  # Adjust this to your needs
#             message_content=message_content,
#         )
#         message.save()

#         # You can send the message to the room so that other users can see it
#         self.send_group_message(message)

#     def send_group_message(self, message):
#         group_name = f"user_{message.receiver.id}"
#         async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
#         async_to_sync(self.channel_layer.group_send)(
#             group_name,
#             {
#                 "type": "chat.message",
#                 "message": {
#                     "sender_id": message.sender.id,
#                     "message_content": message.message_content,
#                     "timestamp": message.timestamp,
#                 },
#             },
#         )

#     def chat_message(self, event):
#         # Send the message to the WebSocket
#         self.send_json(event["message"])


############################################################# models file content status ################################################################################

# class Status(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statuses')
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()
# drf whatsapp clone with channels JsonWebSocketConsumerall fields  save database  explain code wise only consumers file full details with example


############################################################# models file content ################################################################################
####################################################################################


# import json
# from channels.generic.websocket import JsonWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# from .models import Status

# User = get_user_model()

# class StatusConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         # WebSocket connection authentication
#         if self.scope["user"].is_anonymous:
#             self.close()
#         else:
#             # Join a room, which can be based on user IDs or group IDs
#             user_id = self.scope["user"].id
#             self.room_name = f"user_{user_id}_statuses"
#             async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
#             self.accept()

#     def disconnect(self, close_code):
#         # WebSocket disconnect
#         async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

#     def receive_json(self, content, **kwargs):
#         # Handle incoming WebSocket status updates
#         status_content = content['content']
#         user = self.scope['user']

#         # Create a new status and save it to the database
#         status = Status(
#             user=user,
#             content=status_content,
#         )
#         status.save()

#         # You can send the status update to the room so that other users can see it
#         self.send_group_status(status)

#     def send_group_status(self, status):
#         group_name = self.room_name
#         async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
#         async_to_sync(self.channel_layer.group_send)(
#             group_name,
#             {
#                 "type": "status.update",
#                 "status": {
#                     "user_id": status.user.id,
#                     "content": status.content,
#                     "created_at": status.created_at.isoformat(),
#                 },
#             },
#         )

#     def status_update(self, event):
#         # Send the status update to the WebSocket
#         self.send_json(event["status"])





############################################################# models file content call : voice and video ###############################################################

# class Call(models.Model):
#     caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_calls')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_calls')
#     call_type = models.CharField(max_length=10)  # 'audio' or 'video'
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
# # Voice and Video Calls
# class VoiceCall(models.Model):
#     voice_caller = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='voice_calls_made')

#     initiated_at = models.DateTimeField(auto_now_add=True)
#     call_status = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')])
   

# class VideoCall(models.Model):
#   video_caller = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='voice_calls_made')
#     initiated_at = models.DateTimeField(auto_now_add=True)
#     call_status = models.CharField(max_length=20, choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')])
    
#     drf whatsapp clone with channels JsonWebSocketConsumerall fields  save database  explain code wise only consumers file full details with example


############################################################# models file content ################################################################################

# ####################################################################################


# import json
# from channels.generic.websocket import JsonWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# from .models import Call, VoiceCall, VideoCall

# User = get_user_model()

# class CallConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         # WebSocket connection authentication
#         if self.scope["user"].is_anonymous:
#             self.close()
#         else:
#             self.accept()

#     def disconnect(self, close_code):
#         # WebSocket disconnect
#         self.close()

#     def receive_json(self, content, **kwargs):
#         call_type = content['call_type']
#         user = self.scope['user']

#         if call_type == 'audio':
#             # Handle audio call
#             call = Call(
#                 caller=user,
#                 recipient=User.objects.get(id=content['recipient_id']),
#                 call_type=call_type,
#                 start_time=content['start_time'],
#                 end_time=content['end_time'],
#             )
#             call.save()

#             voice_call = VoiceCall(
#                 voice_caller=call,
#                 initiated_at=content['initiated_at'],
#                 call_status='outgoing',  # Adjust the call status based on your logic
#             )
#             voice_call.save()
#         elif call_type == 'video':
#             # Handle video call
#             call = Call(
#                 caller=user,
#                 recipient=User.objects.get(id=content['recipient_id']),
#                 call_type=call_type,
#                 start_time=content['start_time'],
#                 end_time=content['end_time'],
#             )
#             call.save()

#             video_call = VideoCall(
#                 video_caller=call,
#                 initiated_at=content['initiated_at'],
#                 call_status='outgoing',  # Adjust the call status based on your logic
#             )
#             video_call.save()

#         # You can send call updates to the WebSocket
#         self.send_call_update(call)

#     def send_call_update(self, call):
#         # Send the call update to the WebSocket
#         call_type = call.call_type
#         if call_type == 'audio':
#             voice_call = VoiceCall.objects.get(voice_caller=call)
#             data = {
#                 "call_id": call.id,
#                 "call_type": call_type,
#                 "start_time": call.start_time.isoformat(),
#                 "end_time": call.end_time.isoformat(),
#                 "call_status": voice_call.call_status,
#             }
#         elif call_type == 'video':
#             video_call = VideoCall.objects.get(video_caller=call)
#             data = {
#                 "call_id": call.id,
#                 "call_type": call_type,
#                 "start_time": call.start_time.isoformat(),
#                 "end_time": call.end_time.isoformat(),
#                 "call_status": video_call.call_status,
#             }
#         self.send_json(data)


############################################################# models file content notification ##########################################################################

# class NotificationSettings(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     enable_push_notifications = models.BooleanField(default=True)
#     enable_message_notifications = models.BooleanField(default=True)
#     enable_call_notifications = models.BooleanField(default=True)
#     enable_status_update_notifications = models.BooleanField(default=True)
#     quiet_hours_start = models.TimeField(blank=True, null=True)
#     quiet_hours_end = models.TimeField(blank=True, null=True)
#     notification_sound = models.CharField(max_length=100, blank=True, null=True)
#     notification_vibration = models.BooleanField(default=True)
    
#  drf whatsapp clone with channels JsonWebSocketConsumerall fields  save database  explain code wise only consumers file full details with example


############################################################# models file content ################################################################################
# ####################################################################################

# import json
# from channels.generic.websocket import JsonWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# from .models import NotificationSettings

# User = get_user_model()

# class NotificationSettingsConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         # WebSocket connection authentication
#         if self.scope["user"].is_anonymous:
#             self.close()
#         else:
#             self.accept()

#     def disconnect(self, close_code):
#         # WebSocket disconnect
#         self.close()

#     def receive_json(self, content, **kwargs):
#         user = self.scope['user']
#         enable_push_notifications = content['enable_push_notifications']
#         enable_message_notifications = content['enable_message_notifications']
#         enable_call_notifications = content['enable_call_notifications']
#         enable_status_update_notifications = content['enable_status_update_notifications']
#         quiet_hours_start = content['quiet_hours_start']
#         quiet_hours_end = content['quiet_hours_end']
#         notification_sound = content['notification_sound']
#         notification_vibration = content['notification_vibration']

#         # Update the user's notification settings
#         notification_settings, created = NotificationSettings.objects.get_or_create(user=user)

#         notification_settings.enable_push_notifications = enable_push_notifications
#         notification_settings.enable_message_notifications = enable_message_notifications
#         notification_settings.enable_call_notifications = enable_call_notifications
#         notification_settings.enable_status_update_notifications = enable_status_update_notifications
#         notification_settings.quiet_hours_start = quiet_hours_start
#         notification_settings.quiet_hours_end = quiet_hours_end
#         notification_settings.notification_sound = notification_sound
#         notification_settings.notification_vibration = notification_vibration

#         notification_settings.save()

#         # You can send a response back to the WebSocket
#         self.send_notification_settings_update(notification_settings)

#     def send_notification_settings_update(self, notification_settings):
#         # Send the updated notification settings to the WebSocket
#         data = {
#             "enable_push_notifications": notification_settings.enable_push_notifications,
#             "enable_message_notifications": notification_settings.enable_message_notifications,
#             "enable_call_notifications": notification_settings.enable_call_notifications,
#             "enable_status_update_notifications": notification_settings.enable_status_update_notifications,
#             "quiet_hours_start": notification_settings.quiet_hours_start.strftime("%H:%M:%S") if notification_settings.quiet_hours_start else None,
#             "quiet_hours_end": notification_settings.quiet_hours_end.strftime("%H:%M:%S") if notification_settings.quiet_hours_end else None,
#             "notification_sound": notification_settings.notification_sound,
#             "notification_vibration": notification_settings.notification_vibration,
#         }
#         self.send_json(data)



# ####################################################################################


# ################################ UserProfile ####################################################

# import json
# from channels.generic.websocket import JsonWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# from .models import UserProfile

# User = get_user_model()

# class UserProfileConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         # WebSocket connection authentication
#         if self.scope["user"].is_anonymous:
#             self.close()
#         else:
#             self.accept()

#     def disconnect(self, close_code):
#         # WebSocket disconnect
#         self.close()

#     def receive_json(self, content, **kwargs):
#         user = self.scope['user']

#         # Update the user's profile and notification settings
#         profile, created = UserProfile.objects.get_or_create(user=user)

#         profile.language = content.get('language', profile.language)
#         profile.app_theme = content.get('app_theme', profile.app_theme)
#         profile.privacy_enabled = content.get('privacy_enabled', profile.privacy_enabled)
#         profile.message_notifications_enabled = content.get('message_notifications_enabled', profile.message_notifications_enabled)
#         profile.call_notifications_enabled = content.get('call_notifications_enabled', profile.call_notifications_enabled)
#         profile.status_update_notifications_enabled = content.get('status_update_notifications_enabled', profile.status_update_notifications_enabled)

#         # Handle the optional upload of chat wallpaper
#         chat_wallpaper = content.get('chat_wallpaper')
#         if chat_wallpaper:
#             profile.chat_wallpaper = chat_wallpaper
#         profile.save()

#         # Send a response back to the WebSocket
#         self.send_user_profile_update(profile)

#     def send_user_profile_update(self, profile):
#         # Send the updated user profile and notification settings to the WebSocket
#         data = {
#             "language": profile.language,
#             "app_theme": profile.app_theme,
#             "privacy_enabled": profile.privacy_enabled,
#             "message_notifications_enabled": profile.message_notifications_enabled,
#             "call_notifications_enabled": profile.call_notifications_enabled,
#             "status_update_notifications_enabled": profile.status_update_notifications_enabled,
#             "chat_wallpaper": profile.chat_wallpaper.url if profile.chat_wallpaper else None,
#         }
#         self.send_json(data)


# # ####################################################################################

# # ###############################    contact #####################################################

# import json
# from channels.generic.websocket import JsonWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# from django.core.validators import RegexValidator
# from .models import Contact

# User = get_user_model()

# class ContactConsumer(JsonWebsocketConsumer):
#     def connect(self):
#         # WebSocket connection authentication
#         if self.scope["user"].is_anonymous:
#             self.close()
#         else:
#             self.accept()

#     def disconnect(self, close_code):
#         # WebSocket disconnect
#         self.close()

#     def receive_json(self, content, **kwargs):
#         user = self.scope['user']
#         name = content.get('name', None)
#         country_code = content.get('country_code', '+91')
#         phone_number = content.get('phone_number', None)
#         email = content.get('email', None)

#         # Create or update the user's contact
#         contact, created = Contact.objects.get_or_create(user=user, phone_number=phone_number)

#         contact.name = name
#         contact.country_code = country_code
#         contact.email = email

#         # Validate the Indian phone number
#         if country_code == '+91':
#             india_phone_regex = RegexValidator(
#                 regex=r'^\+91[1-9][0-9]{9}$',
#                 message="Indian phone number must be in the format: '+91XXXXXXXXXX' (10 digits after the country code)."
#             )
#             india_phone_regex(phone_number)

#         contact.save()

#         # Send a response back to the WebSocket
#         self.send_contact_update(contact)

#     def send_contact_update(self, contact):
#         # Send the updated contact information to the WebSocket
#         data = {
#             "name": contact.name,
#             "country_code": contact.country_code,
#             "phone_number": contact.phone_number,
#             "email": contact.email,
#         }
#         self.send_json(data)


# # ####################################################################################

