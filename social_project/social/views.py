from rest_framework import viewsets, status
from .models import *
from .serializers import * 
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ReelViewSet(viewsets.ModelViewSet):
    queryset = Reel.objects.all()
    serializer_class = ReelSerializer

class LiveViewSet(viewsets.ModelViewSet):
    queryset = Live.objects.all()
    serializer_class = LiveSerializer

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def create(self, request, *args, **kwargs):
        if request.user.stories.filter(created_at__gte=timezone.now() - timezone.timedelta(hours=24)).count() >= 24:
            return Response({"message": "You have reached the maximum number of stories for the last 24 hours."}, status=400)
        return super().create(request, *args, **kwargs)
    
class StoryHighlightViewSet(viewsets.ModelViewSet):
    queryset = StoryHighlight.objects.all()
    serializer_class = StoryHighlightSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StoryHighlightItemViewSet(viewsets.ModelViewSet):
    queryset = StoryHighlightItem.objects.all()
    serializer_class = StoryHighlightItemSerializer

    def perform_create(self, serializer):
        serializer.save()

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()

        # Check if the user has already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform additional validation if needed, e.g., like count, like size, etc.
        # ...

        # Create the like
        like = Like.objects.create(user=request.user, post=post)
        serializer = LikeSerializer(like)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        post = self.get_object()

        # Check if the user has liked the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        return Response({'detail': 'Post unliked.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def create_post_like(self, request):
        post_link = request.data.get('post_link')

        # Check if the user has already liked the post with the given link
        post = Post.objects.filter(user=request.user, link=post_link).first()
        if post:
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Perform additional validation if needed, e.g., like count, like size, etc.
        # ...

        # Create a new post with the given link
        post = Post.objects.create(user=request.user, link=post_link)
        serializer = PostSerializer(post)

        # Create the like for the new post
        like = Like.objects.create(user=request.user, post=post)
        like_serializer = LikeSerializer(like)

        return Response({'post': serializer.data, 'like': like_serializer.data}, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    
    def create(self, request, *args, **kwargs):
        follower = request.user
        following_id = request.data.get('following')

        if following_id:
            try:
                following = User.objects.get(id=following_id)
            except User.DoesNotExist:

                return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

            if follower == following:
                return Response({"error": "A user cannot follow themselves"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(follower=follower, following=following)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "Missing 'following' parameter"}, status=status.HTTP_400_BAD_REQUEST)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class DirectMessageViewSet(viewsets.ModelViewSet):
    queryset = DirectMessage.objects.all()
    serializer_class = DirectMessageSerializer
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Additional custom validation logic if required
        serializer.save(sender=request.user)
        return Response(serializer.data)