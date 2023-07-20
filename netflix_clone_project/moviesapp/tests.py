from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import (
    MediaLibrary, Metadata, ThumbnailsTrailers, Search, Recommendations,
    CategoriesGenres, VideoPlayerIntegration, VideoEncoding, AdaptiveBitrateStreaming,
    Watchlist, RatingReviews, SocialSharing
)
from .serializers import (
    MediaLibrarySerializer, MetadataSerializer, ThumbnailsTrailersSerializer,
    SearchSerializer, RecommendationsSerializer, CategoriesGenresSerializer,
    VideoPlayerIntegrationSerializer, VideoEncodingSerializer, AdaptiveBitrateStreamingSerializer,
    WatchlistSerializer, RatingReviewsSerializer, SocialSharingSerializer
)

class MediaLibraryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_media_library(self):
        url = reverse('medialibrary-list')
        data = {
            'title': 'Avengers: Endgame',
            'genre': 'Action',
            'director': 'Anthony Russo, Joe Russo',
            'release_year': 2019,
            'description': 'The epic conclusion to the Marvel Cinematic Universe.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MediaLibrary.objects.count(), 1)
        self.assertEqual(MediaLibrary.objects.get().title, 'Avengers: Endgame')

    # Add more test cases for other API endpoints and models as needed

class MetadataAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_metadata(self):
        media_library = MediaLibrary.objects.create(
            title='Avengers: Endgame',
            genre='Action',
            director='Anthony Russo, Joe Russo',
            release_year=2019,
            description='The epic conclusion to the Marvel Cinematic Universe.'
        )
        url = reverse('metadata-list')
        data = {
            'media_library': media_library.id,
            'cast': 'Robert Downey Jr., Chris Evans, Scarlett Johansson',
            'duration': 181,
            'average_rating': 8.4
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Metadata.objects.count(), 1)
        self.assertEqual(Metadata.objects.get().cast, 'Robert Downey Jr., Chris Evans, Scarlett Johansson')

    # Add more test cases for other API endpoints and models as needed

# Add more test classes for other models and API endpoints as needed

