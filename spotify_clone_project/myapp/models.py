# from django.db import models
# from django.contrib.auth.models import User

# class Artist(models.Model):
#     name = models.CharField(max_length=100)
#     performed_by = models.CharField(max_length=100)
#     written_by = models.CharField(max_length=100)
#     produced_by = models.CharField(max_length=100)
#     followers = models.ManyToManyField(User, related_name='following_artists')

# class Song(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
#     audio_url = models.URLField()
#     video_url = models.URLField()
#     likes = models.PositiveIntegerField(default=0)
#     downloads = models.PositiveIntegerField(default=0)

# class Podcast(models.Model):
#     title = models.CharField(max_length=100)
#     audio_url = models.URLField()
#     video_url = models.URLField()
#     watching_choices = models.CharField(max_length=10, choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High')])

# VISIBILITY_CHOICES = {
#     'Public':'Public',
#     'Private':'Private',
# }
# class Playlist(models.Model):
#     title = models.CharField(max_length=100)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     songs = models.ManyToManyField(Song, related_name='playlists')
#     is_public = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='Public')
#     # is_public = models.BooleanField(default=True)
#     enhanced = models.BooleanField(default=False)

# class Album(models.Model):
#     title = models.CharField(max_length=100)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     songs = models.ManyToManyField(Song, related_name='albums')

# class Blend(models.Model):
#     title = models.CharField(max_length=100)
#     users = models.ManyToManyField(User)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

# class PremiumPlan(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     months = models.PositiveIntegerField(choices=[(1, '1 Month'), (2, '2 Months'), (3, '3 Months')])

# # Add more fields and functionalities as needed
