import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
from django.contrib.auth.models import User



class MessageConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        # Get the message content from the WebSocket
        message = content['message']

        # Save the message to the database
        # Create a Message object and set its fields
        message_obj = Message.objects.create(
            sender=self.scope['user'],
            receiver=User.objects.get(username=self.room_name),  # Replace with your user lookup logic
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

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))