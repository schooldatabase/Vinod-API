from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


#-----------------------------
from .models import (
    MediaLibrary, Metadata, ThumbnailsTrailers, Search, Recommendations,
    CategoriesGenres, VideoPlayerIntegration, VideoEncoding, AdaptiveBitrateStreaming,
    Watchlist, RatingReviews, SocialSharing
)

class MediaLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLibrary
        fields = '__all__'

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = '__all__'

class ThumbnailsTrailersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailsTrailers
        fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = '__all__'

class RecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendations
        fields = '__all__'

class CategoriesGenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesGenres
        fields = '__all__'

class VideoPlayerIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPlayerIntegration
        fields = '__all__'

class VideoEncodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoEncoding
        fields = '__all__'

class AdaptiveBitrateStreamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdaptiveBitrateStreaming
        fields = '__all__'

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'

class RatingReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingReviews
        fields = '__all__'

class SocialSharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialSharing
        fields = '__all__'
