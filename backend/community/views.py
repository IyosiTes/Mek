from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CommentReaction, Post, Comment
from .pagination import  PostPagination, CommentPagination
from .serializers import PostSerializer, CommentSerializer
from django.utils import timezone
from datetime import timedelta
# Create your views here.

from rest_framework.generics import ListCreateAPIView, ListAPIView
from django.db.models import Count, Q, Prefetch

    
   

class PostListCreate(ListCreateAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
     return Post.objects.filter(is_deleted=False)\
        .annotate(comment_count=Count('comments'))\
        .order_by('-created_at')
    
    def post(self, request):
        content = request.data.get('content')
        anon_id = request.data.get('anonymous_id')
        user_name = request.data.get("user_name") or "ምእመን"

        if not anon_id:
            return Response({"error": "Missing anonymous_id"}, status=400)

        if not content or len(content) > 500:
            return Response({"error": "Invalid content"}, status=400)

        # rate limit
        recent_posts = Post.objects.filter(
            anonymous_id=anon_id,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        ).count()

        if recent_posts >= 3:
            return Response({"error": "Too many posts"}, status=429)

        post = Post.objects.create(
            content=content,
            anonymous_id=anon_id,
            user_name=user_name
        )

        return Response(PostSerializer(post).data, status=201)
    
class CommentCreate(APIView):

    def post(self, request, post_id):
        content = request.data.get('content')
        anon_id = request.data.get('anonymous_id')
        parent_id = request.data.get('parent_id')

        if not anon_id:
            return Response({"error": "Missing anonymous_id"}, status=400)

        if not content or len(content) > 300:
            return Response({"error": "Invalid comment"}, status=400)

        try:
            post = Post.objects.get(public_id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)

        parent = None
        if parent_id:
            parent = Comment.objects.filter(id=parent_id).first()

        comment = Comment.objects.create(
            post=post,
            content=content,
            anonymous_id=anon_id,
            parent=parent
        )

        return Response(CommentSerializer(comment).data, status=201)

class CommentReactionCreate(APIView):

    def post(self, request, comment_id):
        reaction_type = request.data.get('reaction_type')
        anon_id = request.data.get('anonymous_id')

        if not anon_id:
         return Response({"error": "Missing anonymous_id"}, status=400)

        if reaction_type not in ['like', 'dislike']:
            return Response({"error": "Invalid reaction"}, status=400)

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=404)

        anon_id = request.data.get('anonymous_id')

        reaction, created = CommentReaction.objects.get_or_create(
                    comment=comment,
                    anonymous_id=anon_id,
                    defaults={"reaction_type": reaction_type}
                )

        if not created:
                    reaction.reaction_type = reaction_type
                    reaction.save()

        return Response({"message": "Reaction added"})


class CommentList(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    
    def get_queryset(self):
        post_id = self.kwargs['post_id']

        return Comment.objects.filter(
            post__public_id=post_id,
            parent__isnull=True
        ).annotate(
            like_count=Count('reactions', filter=Q(reactions__reaction_type='like')),
            dislike_count=Count('reactions', filter=Q(reactions__reaction_type='dislike'))
        ).prefetch_related(
            Prefetch(
                'replies',
                queryset=Comment.objects.annotate(
                    like_count=Count('reactions', filter=Q(reactions__reaction_type='like')),
                    dislike_count=Count('reactions', filter=Q(reactions__reaction_type='dislike'))
                )
            )
        ).order_by('created_at')