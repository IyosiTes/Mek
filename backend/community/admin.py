from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Comment, CommentReaction

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'public_id',
        'short_content',
        'user_name',
        'anonymous_id',
        'is_admin_post',
        'is_deleted',
        'created_at'
    )

    list_filter = (
        'is_admin_post',
        'is_deleted',
        'created_at'
    )

    search_fields = (
        'content',
        'anonymous_id',
        'user_name'
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    actions = ['soft_delete_posts', 'restore_posts', 'mark_as_admin_post']

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = "Content"

    def soft_delete_posts(self, request, queryset):
        queryset.update(is_deleted=True)
    soft_delete_posts.short_description = "🚫 Soft delete selected posts"

    def restore_posts(self, request, queryset):
        queryset.update(is_deleted=False)
    restore_posts.short_description = "♻️ Restore deleted posts"

    def mark_as_admin_post(self, request, queryset):
        queryset.update(is_admin_post=True)
    mark_as_admin_post.short_description = "⭐ Mark as admin post"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'short_content',
        'anonymous_id',
        'created_at'
    )

    search_fields = (
        'content',
        'anonymous_id'
    )

    list_filter = (
        'created_at',
    )

    actions = ['delete_comments']

    def short_content(self, obj):
        return obj.content[:50]

    def delete_comments(self, request, queryset):
        queryset.delete()
    delete_comments.short_description = "🗑 Delete selected comments"