from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    MediaLibraryViewSet, MetadataViewSet, ThumbnailsTrailersViewSet, SearchViewSet,
    RecommendationsViewSet, CategoriesGenresViewSet, VideoPlayerIntegrationViewSet,
    VideoEncodingViewSet, AdaptiveBitrateStreamingViewSet, WatchlistViewSet,
    RatingReviewsViewSet, SocialSharingViewSet
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'medialibraries', MediaLibraryViewSet, basename='medialibraries')
router.register(r'metadata', MetadataViewSet, basename='metadata')
router.register(r'thumbnailstrailers', ThumbnailsTrailersViewSet, basename='thumbnailstrailers')
router.register(r'search', SearchViewSet, basename='search')
router.register(r'recommendations', RecommendationsViewSet, basename='recommendations')
router.register(r'categoriesgenres', CategoriesGenresViewSet, basename='categoriesgenres')
router.register(r'videoplayerintegration', VideoPlayerIntegrationViewSet, basename='videoplayerintegration')
router.register(r'videoencoding', VideoEncodingViewSet, basename='videoencoding')
router.register(r'adaptivebitratestreaming', AdaptiveBitrateStreamingViewSet, basename='adaptivebitratestreaming')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'ratingreviews', RatingReviewsViewSet, basename='ratingreviews')
router.register(r'socialsharing', SocialSharingViewSet, basename='socialsharing')

urlpatterns = [
    path('', include(router.urls)),
]
