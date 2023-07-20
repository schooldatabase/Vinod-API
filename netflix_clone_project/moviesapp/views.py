from rest_framework import viewsets, status
from .models import *
from .serializers import * 
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    MediaLibrary, Metadata, ThumbnailsTrailers, Search, Recommendations,
    CategoriesGenres, VideoPlayerIntegration, VideoEncoding, AdaptiveBitrateStreaming,
    Watchlist, RatingReviews, SocialSharing
)
from .serializers import (
    MediaLibrarySerializer, MetadataSerializer, ThumbnailsTrailersSerializer,
    SearchSerializer, RecommendationsSerializer, CategoriesGenresSerializer,
    VideoPlayerIntegrationSerializer, VideoEncodingSerializer,
    AdaptiveBitrateStreamingSerializer, WatchlistSerializer, RatingReviewsSerializer,
    SocialSharingSerializer
)

class MediaLibraryViewSet(viewsets.ModelViewSet):
    queryset = MediaLibrary.objects.all()
    serializer_class = MediaLibrarySerializer

class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

class ThumbnailsTrailersViewSet(viewsets.ModelViewSet):
    queryset = ThumbnailsTrailers.objects.all()
    serializer_class = ThumbnailsTrailersSerializer

class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer

class RecommendationsViewSet(viewsets.ModelViewSet):
    queryset = Recommendations.objects.all()
    serializer_class = RecommendationsSerializer

class CategoriesGenresViewSet(viewsets.ModelViewSet):
    queryset = CategoriesGenres.objects.all()
    serializer_class = CategoriesGenresSerializer

class VideoPlayerIntegrationViewSet(viewsets.ModelViewSet):
    queryset = VideoPlayerIntegration.objects.all()
    serializer_class = VideoPlayerIntegrationSerializer

class VideoEncodingViewSet(viewsets.ModelViewSet):
    queryset = VideoEncoding.objects.all()
    serializer_class = VideoEncodingSerializer

class AdaptiveBitrateStreamingViewSet(viewsets.ModelViewSet):
    queryset = AdaptiveBitrateStreaming.objects.all()
    serializer_class = AdaptiveBitrateStreamingSerializer

class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer

class RatingReviewsViewSet(viewsets.ModelViewSet):
    queryset = RatingReviews.objects.all()
    serializer_class = RatingReviewsSerializer

class SocialSharingViewSet(viewsets.ModelViewSet):
    queryset = SocialSharing.objects.all()
    serializer_class = SocialSharingSerializer
