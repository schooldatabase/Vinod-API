# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# import json

# notification implatmation 

# @receiver(post_save, sender=MessageNotification)
# def send_message_notification(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     notification = {
#         'type': 'send_message_notification',
#         'notification': {
#             'user': instance.user.username,
#             'message': instance.message.message_content,
#             'timestamp': instance.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#         }
#     }
#     channel_layer.group_send('notifications', notification)

# @receiver(post_save, sender=CallNotification)
# def send_call_notification(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     notification = {
#         'type': 'send_call_notification',
#         'notification': {
#             'user': instance.user.username,
#             'call': f"{instance.call.caller} - {instance.call.receiver}",
#             'status': instance.call.call_status,
#             'timestamp': instance.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#         }
#     }
#     channel_layer.group_send('notifications', notification)

# @receiver(post_save, sender=StatusUpdateNotification)
# def send_status_update_notification(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     notification = {
#         'type': 'send_status_update_notification',
#         'notification': {
#             'user': instance.user.username,
#             'status_update': instance.status_update.status_content,
#             'timestamp': instance.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#         }
#     }
#     channel_layer.group_send('notifications', notification)









# ---------------------------------------------------------------



# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .models import Message, Call, StatusUpdate
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# channel_layer = get_channel_layer()

# @receiver(post_save, sender=Message)
# def send_message_notification(sender, instance, **kwargs):
#     # Triggered when a new message is created
#     message = instance.message_content
#     async_to_sync(channel_layer.group_send)("notifications", {
#         'type': 'send_message_notification',
#         'message': message,
#     })

# @receiver(post_save, sender=Call)
# def send_call_notification(sender, instance, **kwargs):
#     # Triggered when a new call is created
#     call_info = {
#         'caller': instance.caller.username,
#         'receiver': instance.receiver.username,
#         'call_status': instance.call_status,
#     }
#     async_to_sync(channel_layer.group_send)("notifications", {
#         'type': 'send_call_notification',
#         'call_info': call_info,
#     })

# @receiver(post_save, sender=StatusUpdate)
# def send_status_update_notification(sender, instance, **kwargs):
#     # Triggered when a new status update is created
#     status_update = instance.status_content
#     async_to_sync(channel_layer.group_send)("notifications", {
#         'type': 'send_status_update_notification',
#         'status_update': status_update,
#     })





















#--------------JsonAsyncWebsocketConsumer-------###############################______________________________________

# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .models import Message, Call, StatusUpdate
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# channel_layer = get_channel_layer()

# @receiver(post_save, sender=Message)
# def send_message_notification(sender, instance, **kwargs):
#     # Triggered when a new message is created
#     message = instance.message_content
#     async_to_sync(channel_layer.group_send)("notifications", {
#         'type': 'send_message_notification',
#         'message': message,
#     })

# @receiver(post_save, sender=Call)
# def send_call_notification(sender, instance, **kwargs):
#     # Triggered when a new call is created
#     call_info = {
#         'caller': instance.caller.username,
#         'receiver': instance.receiver.username,
#         'call_status': instance.call_status,
#     }
#     async_to_sync(channel_layer.group_send)("notifications", {
#         'type': 'send_call_notification',
#         'call_info': call_info,
#     })

# @receiver(post_save, sender=StatusUpdate)
# def send_status_update_notification(sender, instance, **kwargs):
#     # Triggered when a new status update is created
#     status_update = instance.status_content
#     async_to_sync(channel_layer.group_send)("notifications", {
#         'type': 'send_status_update_notification',
#         'status_update': status_update,
#     })
