from rest_framework import serializers
from .models import CommentReaction, Post, Comment
from django.utils.timesince import timesince


class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'username', 
            'created_at',
            'time_ago',
            'like_count', 
            'dislike_count', 
            'replies'
            ]

    def get_like_count(self, obj):
     return getattr(obj, 'like_count', 0)

    def get_dislike_count(self, obj):
     return getattr(obj, 'dislike_count', 0)

    def get_replies(self, obj):
     replies = getattr(obj, 'replies', None)

     if replies is None:
        return []

     return CommentSerializer(replies.all()[:5], many=True).data
    
    def get_time_ago(self, obj):
        return timesince(obj.created_at) + "ago"


class CommentReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReaction
        fields = ['reaction_type']      



class PostSerializer(serializers.ModelSerializer):
    is_admin_post = serializers.BooleanField(read_only=True)
    time_ago = serializers.SerializerMethodField()
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'public_id',
            'content',
            'user_name',
            'created_at',
            'time_ago',
            'is_admin_post',
            'comment_count'
        ]

    def get_time_ago(self, obj):
        return timesince(obj.created_at) + " ago"