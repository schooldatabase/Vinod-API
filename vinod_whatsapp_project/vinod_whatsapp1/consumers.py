# consumers.py
import json
from django.contrib.auth.models import User
from channels.generic.websocket import JsonAsyncWebsocketConsumer
from .models import Message


class ChatConsumer(JsonAsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
        else:
            self.room_name = f"chat_{self.user.id}"
            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        message = content.get('message', None)
        if message:
            await self.save_message(message)
            await self.forward_message(message)

    async def save_message(self, message_content):
        # Extract necessary information from message_content (e.g., sender, receiver, group, etc.)
        # Save the message in the database using Django models
        # Example implementation:
        # from .models import Message
        message = Message(
            sender=self.user,  # Assuming the authenticated user is the sender
            receiver=User.objects.get(pk=message_content['receiver_id']),  # Assuming 'receiver_id' is sent in the message_content
            message_content=message_content['content'],  # Assuming 'content' field contains the message content
        )
        message.save()

        # Set is_delivered to True for the sender (optional if you want to handle delivery status)
        message.is_delivered = True
        message.save()

    async def forward_message(self, message_content):
        # Assuming you have already defined a WebSocket group for each user
        receiver_group_name = f"chat_{message_content['receiver_id']}"

        # Send the message to the receiver's WebSocket group
        await self.channel_layer.group_send(
            receiver_group_name,
            {
                "type": "chat.message",
                "message": message_content
            }
        )
    

    async def chat_message(self, event):
        # Send the received message to the WebSocket
        message_content = event['message']
        await self.send_json({
            "message": message_content
        })


    async def send_call_notification(self, event):
        # Send call notification to the connected client
        call_info = event['call_info']
        await self.send_json({
            'type': 'call_notification',
            'call_info': call_info,
        })

    async def send_status_update_notification(self, event):
        # Send status update notification to the connected client
        status_update = event['status_update']
        await self.send_json({
            'type': 'status_update_notification',
            'status_update': status_update,
        })