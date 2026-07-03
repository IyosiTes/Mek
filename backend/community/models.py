from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.validators import MaxLengthValidator

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    public_name = models.CharField(
        max_length=50,
        default="ምእመን",
        db_index=True,
    )

    bio = models.TextField(
        blank=True,
        default=""
    )

    avatar = models.URLField(
        blank=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.public_name
class Post(models.Model):
    public_id = models.BigAutoField(
        primary_key=True
        )
    
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="community_posts",
)
    content = models.TextField(
    validators=[
        MaxLengthValidator(3000)
    ]
)
    
    image_url = models.URLField(blank=True,null=True)
    is_admin_post = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=["is_deleted", "-created_at"]
         ),
        ]
    
    def __str__(self):
        return f"Post #{self.public_id}"

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='comments', 
        db_index=True)
    
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="community_comments",
)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE,
        db_index=True
    )

    content = models.TextField(
        validators = [
            MaxLengthValidator(1500)
        ]
    )

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["created_at"]
        
        indexes = [
            models.Index(
                fields=["post", "parent"]
                ),
        ]
    def __str__(self):
        return f"Comment {self.id}"
    
class Vote(models.Model):

    UPVOTE = 1
    DOWNVOTE = -1

    VOTE_CHOICES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote")
    )

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="community_votes",
)
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="votes"
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="votes",
        null=True,
        blank=True
    )

    value = models.SmallIntegerField(
        choices=VOTE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
     indexes = [
    models.Index(
        fields=["post", "user"]
    ),
    models.Index(
        fields=["comment", "user"]
    ),
    ]
    
    constraints = [

        models.UniqueConstraint(
            fields=["user", "post"],
            condition=Q(post__isnull=False),
            name="unique_post_vote"
        ),

        models.UniqueConstraint(
            fields=["user", "comment"],
            condition=Q(comment__isnull=False),
            name="unique_comment_vote"
        ),

        models.CheckConstraint(
            condition=Q(value__in=[1, -1]),
            name="valid_vote_value"
        ),

        models.CheckConstraint(
            condition=(
                (
                    Q(post__isnull=False)
                    &
                    Q(comment__isnull=True)
                )
                |
                (
                    Q(post__isnull=True)
                    &
                    Q(comment__isnull=False)
                )
            ),
            name="vote_has_exactly_one_target"
        )
    ]

class Notification(models.Model):

    COMMENT_ON_POST = "comment_on_post"
    REPLY_ON_COMMENT = "reply_on_comment"
    ADMIN_ANNOUNCEMENT = "admin_announcement"

    NOTIFICATION_TYPES = [
        (COMMENT_ON_POST, "Comment on Post"),
        (REPLY_ON_COMMENT, "Reply on Comment"),
        (ADMIN_ANNOUNCEMENT, "Admin Announcement")

    ]

    recipient = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="community_notifications",
)

    actor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="community_generated_notifications",
    null=True,
    blank=True,
)

    post = models.ForeignKey(
        Post,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        db_index=True
    )

    is_read = models.BooleanField(
        default=False,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
    models.Index(
        fields=["recipient", "is_read"]
    )
]