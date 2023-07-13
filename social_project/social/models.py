from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
# from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# class User(AbstractUser):
#     profile_picture = models.ImageField(upload_to='profile_pictures/')
#     bio = models.CharField(max_length=200, blank=True)
#     website = models.URLField(blank=True)

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/',null=True, blank=True)
    caption = models.CharField(max_length=255,null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Post by {self.user.username}"
    
class Reel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reels')
    video = models.FileField(upload_to='reel_videos/',null=True, blank=True)
    caption = models.TextField(validators=[MinLengthValidator(4)],max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Real {self.id} by {self.user.username}"

class Live(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lives')
    title = models.CharField(max_length=100,null=True, blank=True)
    scheduled_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.scheduled_time <= timezone.now():
            raise ValidationError("Scheduled time must be in the future.")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Live {self.id} by {self.user.username}"

class Guide(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guides')
    title = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Guide {self.id} by {self.user.username}"

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='story_images/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_highlight = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        get_latest_by = 'created_at'

    def save(self, *args, **kwargs):
        if self.is_highlight and self.user.stories.filter(is_highlight=True).count() >= 5:
            raise ValidationError("You can only have up to 5 story highlights.")
        super().save(*args, **kwargs)
        
class StoryHighlight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class StoryHighlightItem(models.Model):
    highlight = models.ForeignKey(StoryHighlight, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.story.created_at < timezone.now() - timezone.timedelta(hours=24):
            raise ValidationError("Cannot add a story to a highlight older than 24 hours.")

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    # @classmethod
    # def has_liked(cls, user, post):
    #     return cls.objects.filter(user=user, post=post).exists()

    # def save(self, *args, **kwargs):
    #     created = not self.pk
    #     super(Like, self).save(*args, **kwargs)
    #     if created:
    #         self.post.likes_count += 1 # Increment likes count
    #     else:
    #         self.post.likes_count -= 1
    #     self.post.save()

    # def delete(self, *args, **kwargs):
    #     super(Like, self).delete(*args, **kwargs)
    #     self.post.likes_count -= 1  # Decrement likes count
    #     self.post.save()
        
    def __str__(self):
        return f"{self.user.username} liked {self.post}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}: {self.message}"