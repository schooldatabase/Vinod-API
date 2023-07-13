from django.contrib import admin
from .models import *

# Register your models here.
Post, Like, Comment, Follower, Notification, DirectMessage
admin.site.register(Post)
admin.site.register(Reel)
admin.site.register(Live)
admin.site.register(Guide)
admin.site.register(Story)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follower)
admin.site.register(Notification)
admin.site.register(DirectMessage)
