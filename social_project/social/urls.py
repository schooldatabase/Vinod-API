from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'reels', views.ReelViewSet)
router.register(r'lives', views.LiveViewSet)
router.register(r'guides', views.GuideViewSet)
router.register(r'stories', views.StoryViewSet)
router.register(r'likes', views.LikeViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'follows', views.FollowerViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'direct-messages', views.DirectMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),

]