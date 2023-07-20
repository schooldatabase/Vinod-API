from django.contrib import admin
from .models import (
    MediaLibrary, Metadata, ThumbnailsTrailers, Search, Recommendations,
    CategoriesGenres, VideoPlayerIntegration, VideoEncoding, AdaptiveBitrateStreaming,
    Watchlist, RatingReviews, SocialSharing
)

@admin.register(MediaLibrary)
class MediaLibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'director', 'release_year')

@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = ('media_library', 'cast', 'duration', 'average_rating')

@admin.register(ThumbnailsTrailers)
class ThumbnailsTrailersAdmin(admin.ModelAdmin):
    list_display = ('media_library', 'thumbnail_image', 'trailer_video')

@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('search_query',)

@admin.register(Recommendations)
class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'search')

@admin.register(CategoriesGenres)
class CategoriesGenresAdmin(admin.ModelAdmin):
    list_display = ('genre_name',)

@admin.register(VideoPlayerIntegration)
class VideoPlayerIntegrationAdmin(admin.ModelAdmin):
    list_display = ('media_library', 'video_url')

@admin.register(VideoEncoding)
class VideoEncodingAdmin(admin.ModelAdmin):
    list_display = ('video_player_integration', 'encoded_video_files')

@admin.register(AdaptiveBitrateStreaming)
class AdaptiveBitrateStreamingAdmin(admin.ModelAdmin):
    list_display = ('video_encoding', 'video_quality')

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_library')

@admin.register(RatingReviews)
class RatingReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_library', 'rating', 'review')

@admin.register(SocialSharing)
class SocialSharingAdmin(admin.ModelAdmin):
    list_display = ('user', 'media_library', 'social_media_platform')
