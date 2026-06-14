from rest_framework import serializers
from django.utils.timesince import timesince
from .models import CommunityUser, Post, Comment, Vote, Notification


def get_community_user(context):
    """
    Central helper — gets current CommunityUser from
    request context. Returns None for anonymous users.
    Used across all serializers for user_vote, is_author etc.
    """
    request = context.get("request")
    if not request:
        return None
    return getattr(request, "community_user", None)


class CommunityUserSerializer(serializers.ModelSerializer):
    """
    Minimal — embedded inside Post/Comment responses.
    Never expose django_user, is_banned, etc here.
    """
    class Meta:
        model = CommunityUser
        fields = ["uuid", "display_name", "avatar", "is_verified"]
        read_only_fields = fields

class PostFeedSerializer(serializers.ModelSerializer):
    """
    Used in the main feed list — lightweight, no comments.
    comment_count and vote_score must be annotated in the view:

    Post.objects.annotate(
        comment_count=Count("comments", filter=Q(comments__is_deleted=False)),
        vote_score=Coalesce(Sum("votes__value"), 0)
    )
    """
    author_name = serializers.CharField(
        source="author.display_name",
        read_only=True
    )
    author_avatar = serializers.CharField(
        source="author.avatar",
        read_only=True
    )
    # These come from queryset annotation in the view
    comment_count = serializers.IntegerField(read_only=True, default=0)
    vote_score = serializers.IntegerField(read_only=True, default=0)
    
    user_vote = serializers.IntegerField(
    read_only=True,
    default=0
    )
    is_author = serializers.BooleanField(read_only=True)
   
   

    class Meta:
        model = Post
        fields = [
            "public_id",
            "author_name",
            "author_avatar",
            "content",
            "image_url",
            "is_admin_post",
            "is_pinned",
            "is_author",
            "comment_count",
            "vote_score",
            "user_vote",
            "created_at",
        ]

   
class PostCreateSerializer(serializers.ModelSerializer):
    """
    Separate serializer just for POST /posts/
    Keep create and read serializers separate — cleaner.
    """
    class Meta:
        model = Post
        fields = ["content", "image_url"]

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Post cannot be empty."
            )
        if len(value) > 3000:
            raise serializers.ValidationError(
                f"Post too long: {len(value)}/3000 characters."
            )
        return value
    
class PostUpdateSerializer(
    serializers.ModelSerializer
    ):
     class Meta:
        model = Post
        fields = ["content", "image_url"]




class PostDetailSerializer(serializers.ModelSerializer):
    """
    Used on single post page — includes full author object.
    Comments are loaded separately via /posts/{id}/comments/
    Never load comments inside post serializer —
    a post can have 10,000 comments, that would kill your server.
    """
    author = CommunityUserSerializer(read_only=True)
    vote_score = serializers.IntegerField(read_only=True, default=0)
    comment_count = serializers.IntegerField(read_only=True, default=0)
    user_vote = serializers.IntegerField(
    read_only=True,
    default=0
)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "public_id",
            "author",
            "content",
            "image_url",
            "is_admin_post",
            "is_pinned",
            #"is_deleted",
            "vote_score",
            "comment_count",
            "user_vote",
            "is_author",
            "created_at",
            "updated_at",
        ]

   

    def get_is_author(self, obj):
        # Correctly checks if REQUEST USER is post author
        community_user = get_community_user(self.context)
        if not community_user:
            return False
        return obj.author_id == community_user.id



class CommentSerializer(serializers.ModelSerializer):
    """
    Handles both top-level comments AND replies.
    Reply shows parent_preview — the 80-char quote
    displayed above the reply text like in your Telegram screenshot.

    Replies are loaded flat — NOT nested inside comments.
    Frontend groups them by parent_id client-side.
    This is how Reddit, Telegram, Instagram all do it —
    avoids recursive DB queries.
    """
    author_name = serializers.CharField(
        source="author.display_name",
        read_only=True
    )
    author_avatar = serializers.CharField(
        source="author.avatar",
        read_only=True
    )
    post = serializers.IntegerField(
    source="post_id",
    read_only=True
    )

    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        required=False,
        allow_null=True
    )

    vote_score = serializers.IntegerField(read_only=True, default=0)

    user_vote = serializers.IntegerField(
    read_only=True,
    default=0
)
    is_author = serializers.BooleanField(
        read_only=True
    )
   
    # The Telegram-style quote preview above a reply
    reply_preview = serializers.CharField(
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "content",
            "parent",       #null for top-level comments, else parent comment ID
            "author_name",
            "author_avatar",
            "vote_score",
            "user_vote",
            "is_author",
            "reply_preview",    # non-null only when parent exists
            "created_at",
            "is_deleted",
        ]
        read_only_fields = [
            "id", "post", "is_deleted", "created_at"
        ]

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Comment cannot be empty."
            )
        if len(value) > 1500:
            raise serializers.ValidationError(
                f"Comment too long: {len(value)}/1500 characters."
            )
        return value
    
class CommentUpdateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ["content"]

   


class VoteRequestSerializer(
    serializers.Serializer
   ):

    post_id = serializers.IntegerField(
        required=False
    )

    comment_id = serializers.IntegerField(
        required=False
    )

    value = serializers.ChoiceField(
        choices=[-1, 0, 1]
    )

    def validate(self, attrs):

        post_id = attrs.get("post_id")
        comment_id = attrs.get("comment_id")

        if bool(post_id) == bool(comment_id):
            raise serializers.ValidationError(
                "Provide exactly one target."
            )

        return attrs


class NotificationSerializer(serializers.ModelSerializer):
    """
    Includes post_id and comment_id so frontend can
    navigate directly to the right content on tap.
    """
    actor_name = serializers.CharField(
        source="actor.display_name",
        read_only=True
    )
    actor_avatar = serializers.CharField(
        source="actor.avatar",
        read_only=True
    )
    # Navigation targets
    post_id = serializers.IntegerField(
        source="post.public_id",
        read_only=True,
        allow_null=True
    )
    comment_id = serializers.IntegerField(
        source="comment.id",
        read_only=True,
        allow_null=True
    )
    message = serializers.SerializerMethodField()
   

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "actor_name",
            "actor_avatar",
            "message",
            "post_id",
            "comment_id",
            "is_read",
            "created_at",
        ]
        read_only_fields = fields

    def get_message(self, obj):
        name = obj.actor.display_name if obj.actor else "Someone"
        return {
            "comment_on_post":    f"{name} commented on your post",
            "reply_on_comment":   f"{name} replied to your comment",
            "admin_announcement": "New announcement from Mekwerab",
        }.get(obj.notification_type, "New notification")

   