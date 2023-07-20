from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
# from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class MediaLibrary(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=255)
    release_year = models.IntegerField()
    description = models.TextField()
    total_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def clean(self):
        if self.release_year < 1800 or self.release_year > 2100:
            raise ValidationError("Invalid release year.")
    
    def __str__(self):
        return self.title

class Metadata(models.Model):
    media_library = models.OneToOneField(MediaLibrary, on_delete=models.CASCADE)
    cast = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    average_rating = models.FloatField(null=True,blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0),]
    )
    def save(self, *args, **kwargs):
        # Increment the movie's total_views field when a user watches the movie
        self.media_library.total_views += 1
        self.media_library.save()
        super().save(*args, **kwargs)
        
    def clean(self):
        if self.duration > 300:
            raise ValidationError("Duration must be less than or equal to 300.")
    
    def __str__(self):
        return f'{self.media_library.title} - Metadata'

class ThumbnailsTrailers(models.Model):
    media_library = models.OneToOneField(MediaLibrary, on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(upload_to='thumbnails/')
    trailer_video = models.FileField(upload_to='trailers/')

    def clean(self):
        if self.thumbnail_image.size > 10 * 1024 * 1024:
            raise ValidationError("Thumbnail image size should be less than 10MB.")
        if self.trailer_video.size > 100 * 1024 * 1024:
            raise ValidationError("Trailer video size should be less than 100MB.")
    
    def __str__(self):
        return f'{self.media_library.title} - Thumbnails and Trailers'

class Search(models.Model):
    search_query = models.CharField(max_length=255)
    
    def __str__(self):
        return self.search_query

class Recommendations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username} - Recommendation'

class CategoriesGenres(models.Model):
    genre_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.genre_name

class VideoPlayerIntegration(models.Model):
    media_library = models.OneToOneField(MediaLibrary, on_delete=models.CASCADE)
    video_url = models.URLField()
    
    def __str__(self):
        return self.media_library

class VideoEncoding(models.Model):
    video_player_integration = models.ForeignKey(VideoPlayerIntegration, on_delete=models.CASCADE)
    encoded_video_files = models.FileField()
    
    def __str__(self):
        return f'{self.user.username}'

class AdaptiveBitrateStreaming(models.Model):
    video_encoding = models.ForeignKey(VideoEncoding, on_delete=models.CASCADE)
    video_quality = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.user.username}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_library = models.ForeignKey(MediaLibrary, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username}'

class RatingReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_library = models.ForeignKey(MediaLibrary, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating should be between 1 and 5.")

class SocialSharing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media_library = models.ForeignKey(MediaLibrary, on_delete=models.CASCADE)
    social_media_platform = models.CharField(max_length=100)
