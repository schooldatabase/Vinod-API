# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# import json

from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *


# @receiver(post_save, sender=Group)
# def group_created(sender, instance, created, **kwargs):
    
    
    # group = instance.creator
    # participants = instance.participants

    # # Check if the participant is already in the group
    
        
    # if created:
        
    #     existing_participants = Group.objects.filter(creator=instance.creator, participant=instance.participants)

    # if existing_participants.count() > 1:
    #     # If there are duplicate entries, remove the duplicates
    #     duplicate_entries = existing_participants.exclude(pk=instance.pk)
    #     GroupParticipant(duplicate_entries.delete())
        # pass
        # Handle actions when a new group is created
        # For example, you can send notifications to participants or update statistics

        # Replace this with your actual logic
        # Example: Sending notifications
        # participants = instance.participants.all()
        # for participant in participants:
        #     send_notification(participant, f'You have been added to the group: {instance.group_name}')
        


# @receiver(post_save, sender=GroupParticipant)
# def participant_added(sender, instance, created, **kwargs):
#     pass
#     # if created:
#     #     # Handle actions when a participant is added to a group
#     #     # For example, you can update the group's member count

#     #     # Replace this with your actual logic
#         # group = instance.group
#         # participant = instance.participant
    
#     #     group.participants_count = group.groupparticipant_set.count()
#     #     group.save()



# @receiver(pre_delete, sender=GroupParticipant)
# def participant_removed(sender, instance, **kwargs):
#     pass
#     # Handle actions when a participant is removed from a group
#     # For example, you can update the group's member count

#     # Replace this with your actual logic
#     # group = instance.group
#     # group.participants_count = group.groupparticipant_set.count() - 1  # Decrease count
#     # group.save()




# Signal handler for when a new save is added
# @receiver(post_save, sender=Group)
# def update_group_save_count_on_save(sender, instance, created, **kwargs):
#     print("----------------------------------------------------")
#     print("==== instance =", instance.__dict__)
#     print("----------------------------------------------------")
#     print("==== sender =", sender)
#     print("----------------------------------------------------")
#     print("==== createrd =", created)
#     print("----------------------------------------------------")
#     print("==== instance kwargs =", *kwargs)
    
    # if created:
    #     # Handle the case when a new save is added to the group
    #     instance.group.participants += 1
    #     instance.save()

# Signal handler for when a save is removed
# @receiver(post_delete, sender=Group)
# def update_group_save_count_on_delete(sender, instance, **kwargs):
#     # Handle the case when a save is removed from the group
#     if instance.group.GroupParticipant > 1:
#         instance.group.GroupParticipant -= 1
#         instance.save()















@receiver(pre_delete, sender=Group)
def remove_duplicate_participants(sender, instance, **kwargs):
    group = instance.group
    participant = instance.participant

    # Check if the participant is already in the group
    existing_participants = Group.objects.filter(group=instance.group, participant=instance.participant)

    # if existing_participants.exists():
        # If there are duplicate entries, remove the duplicates
    print("pre ----------------------",existing_participants)
    existing_participants.delete()
        # duplicate_entries = existing_participants.exclude(pk=instance.participant)
        # duplicate_entries.delete()
        
@receiver(post_delete, sender=Group)
def remove_duplicate_participants(sender, instance, **kwargs):
    # group = instance.group
    # participant = instance.participant
    
    # Check if the participant is already in the group
    existing_participants = Group.objects.filter(group=instance.group, participant=instance.participant)

    if existing_participants.exists():
        # If there are duplicate entries, remove the duplicates

        print("post ---------------------------",existing_participants.__dir__)
        # duplicate_entries = existing_participants.exclude(pk=instance.participant)
        # duplicate_entries.delete()
        
        



  

  
          
###############################################################################    
##################################     status recent  of data             #############################################    
        
        
@receiver(m2m_changed, sender=Status.StatusRecent.through)
def status_viewers_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            viewer = User.objects.get(pk=user_id)
            print(f"Status '{instance.text}' viewed by user: {viewer.username}")
    elif action == "post_remove":
        for user_id in pk_set:
            unviewer = User.objects.get(pk=user_id)
            print(f"Status '{instance.text}' unviewed by user: {unviewer.username}")        

        
        
        
        
##################################     status recent of data             #############################################       
###############################################################################    
        
 ###############################################################################    
##################################     call recent  of data             #############################################    
        
        
@receiver(m2m_changed, sender=Call.CallRecent.through)
def call_viewers_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            viewer = User.objects.get(pk=user_id)
            print(f"Call from '{instance.caller.username}' viewed by user: {viewer.username}")
    elif action == "post_remove":
        for user_id in pk_set:
            unviewer = User.objects.get(pk=user_id)
            print(f"Call from '{instance.caller.username}' unviewed by user: {unviewer.username}")       

        
        
        
        
##################################     call recent of data             #############################################       
###############################################################################          
        
        
        
        
###############################################################################    
##################################     history of data             #############################################    
        
        
        

        
        
        
        
        
        
        
        
        
        
        
##################################     history of data             #############################################       
###############################################################################    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# @receiver(post_delete, sender=GroupParticipant)
# def remove_duplicate_participants(sender, instance, **kwargs):
#     group = instance.group
#     participant = instance.participant

#     # Check if the participant is already in the group
#     existing_participants = GroupParticipant.objects.filter(group=group, participant=participant)

#     if existing_participants.count() > 1:
#         # If there are duplicate entries, remove the duplicates
#         duplicate_entries = existing_participants.exclude(pk=instance.pk)
#         duplicate_entries.delete()  
# ##############  group       #######################
# # Signal handler for when a new save is added
# # @receiver(post_save, sender=Group)
# # def update_group_save_count_on_save(sender, instance, created, **kwargs):
# #     if created:
#         # Handle the case when a new save is added to the group
#         instance.group.participants += 1
#         instance.save()

# # Signal handler for when a save is removed
# @receiver(post_delete, sender=Group)
# def update_group_save_count_on_delete(sender, instance, **kwargs):
#     # Handle the case when a save is removed from the group
#     if instance.group.participants > 0:
#         instance.group.participants -= 1
#         instance.save()

##############   group      #######################

# # Signal handler for adding a save
# @receiver(post_save, sender=Contact)
# def update_contact_save_count_on_save(sender, instance, **kwargs):
#     # Increment the save_count when a new save is added
#     if instance.email:
#         instance.email.save_count += 1
#         instance.email.save()

# # Signal handler for removing a save
# @receiver(post_delete, sender=Contact)
# def update_contact_save_count_on_delete(sender, instance, **kwargs):
#     # Decrement the save_count when a save is removed
#     if instance.email:
#         instance.email.save_count -= 1
#         instance.email.save()

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
