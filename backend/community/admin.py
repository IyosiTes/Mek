from django.contrib import admin
from .models import (
    Profile,
    Post,
    Comment,
    Vote,
    Notification,
)


# ==========================================================
# Profile
# ==========================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "display_name",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "created_at",
    )

    search_fields = (
        "display_name",
        "user__username",
        "user__email",
    )

    list_select_related = (
        "user",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    actions = (
        "verify_profiles",
        "unverify_profiles",
    )

    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "user",
                    "display_name",
                    "bio",
                    "avatar",
                    "is_verified",
                )
            },
        ),
        (
            "Dates",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.action(description="Verify selected profiles")
    def verify_profiles(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Remove verification")
    def unverify_profiles(self, request, queryset):
        queryset.update(is_verified=False)


# ==========================================================
# Posts
# ==========================================================

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
        "author__username",
        "author__profile__display_name",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "author",
        "author__profile",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    actions = (
        "pin_posts",
        "unpin_posts",
        "mark_admin_posts",
        "unmark_admin_posts",
        "soft_delete_posts",
        "restore_posts",
    )

    fieldsets = (
        (
            "Post",
            {
                "fields": (
                    "author",
                    "content",
                    "image_url",
                )
            },
        ),
        (
            "Moderation",
            {
                "fields": (
                    "is_pinned",
                    "is_admin_post",
                    "is_deleted",
                )
            },
        ),
        (
            "Dates",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def short_content(self, obj):
        return obj.content[:70]

    short_content.short_description = "Content"

    @admin.action(description="Pin selected posts")
    def pin_posts(self, request, queryset):
        queryset.update(is_pinned=True)

    @admin.action(description="Unpin selected posts")
    def unpin_posts(self, request, queryset):
        queryset.update(is_pinned=False)

    @admin.action(description="Mark as admin posts")
    def mark_admin_posts(self, request, queryset):
        queryset.update(is_admin_post=True)

    @admin.action(description="Remove admin flag")
    def unmark_admin_posts(self, request, queryset):
        queryset.update(is_admin_post=False)

    @admin.action(description="Soft delete posts")
    def soft_delete_posts(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore posts")
    def restore_posts(self, request, queryset):
        queryset.update(is_deleted=False)


# ==========================================================
# Comments
# ==========================================================

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

    list_filter = (
        "is_deleted",
        "created_at",
    )

    search_fields = (
        "content",
        "author__username",
        "author__profile__display_name",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "author",
        "author__profile",
        "post",
        "parent",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    actions = (
        "soft_delete_comments",
        "restore_comments",
    )

    fieldsets = (
        (
            "Comment",
            {
                "fields": (
                    "author",
                    "post",
                    "parent",
                    "content",
                )
            },
        ),
        (
            "Moderation",
            {
                "fields": (
                    "is_deleted",
                )
            },
        ),
        (
            "Dates",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    def short_content(self, obj):
        return obj.content[:70]

    short_content.short_description = "Content"

    @admin.action(description="Soft delete comments")
    def soft_delete_comments(self, request, queryset):
        queryset.update(
            is_deleted=True,
            content="[deleted]",
        )

    @admin.action(description="Restore comments")
    def restore_comments(self, request, queryset):
        queryset.update(is_deleted=False)


# ==========================================================
# Votes
# ==========================================================

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "post",
        "comment",
        "value",
        "created_at",
    )

    list_filter = (
        "value",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__profile__display_name",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "user",
        "user__profile",
        "post",
        "comment",
    )

    readonly_fields = (
        "created_at",
    )


# ==========================================================
# Notifications
# ==========================================================

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
        "created_at",
    )

    search_fields = (
        "recipient__username",
        "recipient__profile__display_name",
        "actor__username",
        "actor__profile__display_name",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "recipient",
        "recipient__profile",
        "actor",
        "actor__profile",
        "post",
        "comment",
    )

    readonly_fields = (
        "recipient",
        "actor",
        "post",
        "comment",
        "notification_type",
        "created_at",
    )

    actions = (
        "mark_read",
        "mark_unread",
    )

    @admin.action(description="Mark selected notifications as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected notifications as unread")
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
        