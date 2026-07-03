from rest_framework import serializers
from .models import  Post, Comment, Vote, Notification, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "public_name",
            "avatar",
            "bio",
            "is_verified",
        ]
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
        source="author.profile.public_name",
        read_only=True
    )
    author_avatar = serializers.CharField(
        source="author.profile.avatar",
        read_only=True,
        allow_blank=True,
        default=""
    )
    # These come from queryset annotation in the view
    comment_count = serializers.IntegerField(read_only=True, default=0)
    upvote_count = serializers.IntegerField(read_only=True, default=0)
    downvote_count = serializers.IntegerField(read_only=True, default=0)
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
            "upvote_count",
            "downvote_count",
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
    author = ProfileSerializer(
    source="author.profile",
    read_only=True
)  
    upvote_count = serializers.IntegerField(read_only=True, default=0)
    downvote_count = serializers.IntegerField(read_only=True, default=0)
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
            "upvote_count",
            "downvote_count",
            "vote_score",
            "comment_count",
            "user_vote",
            "is_author",
            "created_at",
            "updated_at",
        ]

   

    def get_is_author(self, obj):
     request = self.context.get("request")

     if (
        not request
        or not request.user.is_authenticated
    ):
        return False

     return obj.author_id == request.user.id



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
        source="author.profile.public_name",
        read_only=True
    )
    author_avatar = serializers.CharField(
        source="author.profile.avatar",
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

    is_post_creator = serializers.BooleanField(read_only=True)

    upvote_count = serializers.IntegerField(read_only=True, default=0)
    downvote_count = serializers.IntegerField(read_only=True, default=0)

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
            "is_post_creator",
            "author_name",
            "author_avatar",
            "upvote_count",
            "downvote_count",
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
        source="actor.profile.public_name",
        read_only=True,
    )

    actor_avatar = serializers.CharField(
        source="actor.profile.avatar",
        read_only=True,
    )

    post_id = serializers.IntegerField(
        source="post.public_id",
        read_only=True,
        allow_null=True,
    )

    comment_id = serializers.IntegerField(
        source="comment.id",
        read_only=True,
        allow_null=True,
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
        name = obj.actor.username if obj.actor else "Someone"

        messages = {
            "comment_on_post": f"{name} commented on your post",
            "reply_on_comment": f"{name} replied to your comment",
            "admin_announcement": "New announcement from Mekwerab",
        }

        return messages.get(obj.notification_type, "New notification")