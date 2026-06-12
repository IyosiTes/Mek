from django.contrib import admin
from .models import CommunityUser, Post, Comment, Notification


@admin.register(CommunityUser)
class CommunityUserAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "display_name",
        "is_verified",
        "is_registered",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "is_registered",
    )

    search_fields = (
        "display_name",
        "uuid",
    )

    readonly_fields = (
        "uuid",
        "created_at",
        "updated_at",
    )

    actions = ["verify_users", "unverify_users"]

    @admin.action(description="Verify selected users")
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Remove verification")
    def unverify_users(self, request, queryset):
        queryset.update(is_verified=False)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "public_id",
        "author",
        "short_content",
        "is_pinned",
        "is_admin_post",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "is_pinned",
        "is_admin_post",
        "is_deleted",
        "created_at",
    )

    search_fields = (
        "content",
        "author__display_name",
    )

    list_select_related = ("author",)

    actions = [
        "pin_posts",
        "unpin_posts",
        "soft_delete_posts",
        "restore_posts",
    ]

    def short_content(self, obj):
        return obj.content[:60]
    short_content.short_description = "Content"

    @admin.action(description="Pin posts")
    def pin_posts(self, request, queryset):
        queryset.update(is_pinned=True)

    @admin.action(description="Unpin posts")
    def unpin_posts(self, request, queryset):
        queryset.update(is_pinned=False)

    @admin.action(description="Soft delete posts")
    def soft_delete_posts(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore posts")
    def restore_posts(self, request, queryset):
        queryset.update(is_deleted=False)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "author",
        "post",
        "parent",
        "short_content",
        "is_deleted",
        "created_at",
    )

    list_filter = ("is_deleted", "created_at")

    search_fields = ("content", "author__display_name")

    list_select_related = ("author", "post", "parent")

    actions = ["soft_delete", "restore"]

    def short_content(self, obj):
        return obj.content[:60]

    @admin.action(description="Soft delete comments")
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore comments")
    def restore(self, request, queryset):
        queryset.update(is_deleted=False)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "recipient",
        "actor",
        "notification_type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
    )

    search_fields = (
        "recipient__display_name",
        "actor__display_name",
    )

    readonly_fields = (
        "recipient",
        "actor",
        "post",
        "comment",
        "notification_type",
        "created_at",
    )

    actions = ["mark_read", "mark_unread"]

    @admin.action(description="Mark as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark as unread")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)

        