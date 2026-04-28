from django.db import models

# Create your models here.
class Post(models.Model):
    public_id = models.AutoField(primary_key=True)
    content = models.TextField()
    anonymous_id = models.CharField(max_length=100, db_index=True)
    user_name = models.CharField(
        max_length=50,
        default="ምእመን"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_admin_post = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Post #{self.public_id}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, db_index=True)
    
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE,
        db_index=True
    )

    username = models.CharField(
        max_length=50,
        default="ምእመን"
    )
    anonymous_id = models.CharField(max_length=100, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


    def __str__(self):
        return f"Comment #{self.post.public_id}"
    
class CommentReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    anonymous_id = models.CharField(max_length=100, db_index=True)
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='reactions',
        db_index=True
    )

    reaction_type = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anonymous_id' , 'comment')