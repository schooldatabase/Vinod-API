from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# serializers class generated
class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    ])

    def validate(self, data):
        image = data.get('image')

        if image:
            # Perform your class-level validation here
            if not self.is_valid_image_size(image):
                raise serializers.ValidationError("Invalid image size.")

        return data

    def is_valid_image_size(self, image):
        # Example image size validation
        max_size = 5 * 1024 * 1024  # Maximum image size in bytes (5 MB)
        return image.size <= max_size

    class Meta:
        model = Post
        fields = '__all__'
        
class ReelSerializer(serializers.ModelSerializer):
    video = serializers.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'mov'])
    ])

    def validate(self, data):
        video = data.get('video')

        if video:
            # Perform your class-level validation here
            if not self.is_valid_video_size(video):
                raise serializers.ValidationError("Invalid video size.")

        return data

    def is_valid_video_size(self, video):
        # Example image size validation
        max_size = 40 * 1024 * 1024  # Maximum image size in bytes (40 MB)
        return video.size <= max_size

    class Meta:
        model = Reel
        fields = '__all__'

class StorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    ])

    def validate(self, data):
        image = data.get('image')
        if image:
            # Perform your class-level validation here
            if not self.is_valid_image_size(image):
                raise serializers.ValidationError("Invalid image size.")
        return data

    def is_valid_image_size(self, image):
        max_size = 5 * 1024 * 1024  # Maximum image size in bytes (5 MB)
        return image.size <= max_size

    class Meta:
        model = Story
        fields = '__all__'
        
class StoryHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryHighlight
        fields = '_all_'

class StoryHighlightItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryHighlightItem
        fields = '_all_'
        
class LiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Live
        fields = '__all__'

class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(write_only=True, required=False)  # Field to indicate liking or unliking

    class Meta:
        model = Post
        fields = '__all__'

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     post = validated_data.pop('post')
    #     like = validated_data.pop('like', False)

    #     instance = super(PostSerializer, self).create(validated_data)

    #     if like:
    #         Like.objects.create(user=request.user, post=instance)

    #     return instance

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     post = validated_data.pop('post')
    #     like = validated_data.pop('like', False)

    #     instance = super(PostSerializer, self).update(instance, validated_data)

    #     if like and not Like.has_liked(request.user, post):
    #         Like.objects.create(user=request.user, post=instance)
    #     elif not like and Like.has_liked(request.user, post):
    #         Like.objects.filter(user=request.user, post=instance).delete()

    #     return instance

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = '__all__'