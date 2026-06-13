from django.urls import path

from .views import (
    PostFeedView,
    CreatePostView,
    PostDetailView,
    UpdatePostView,
    DeletePostView,

    CommentListView,
    CreateCommentView,
    UpdateCommentView,
    DeleteCommentView,

    VoteView,

    NotificationListView,
    NotificationUnreadCountView,
    MarkNotificationReadView,

    CommunityMeView,
)

urlpatterns = [

    # current user
    path(
        "me/",
        CommunityMeView.as_view()
    ),

    # posts
    path(
        "posts/",
        PostFeedView.as_view()
    ),

    path(
        "posts/create/",
        CreatePostView.as_view()
    ),

    path(
        "posts/<int:public_id>/",
        PostDetailView.as_view()
    ),

    path(
        "posts/<int:public_id>/edit/",
        UpdatePostView.as_view()
    ),

    path(
        "posts/<int:public_id>/delete/",
        DeletePostView.as_view()
    ),

    # comments
    path(
        "posts/<int:post_id>/comments/",
        CommentListView.as_view()
    ),

    path(
        "posts/<int:post_id>/comments/create/",
        CreateCommentView.as_view()
    ),

    path(
        "comments/<int:pk>/edit/",
        UpdateCommentView.as_view()
    ),

    path(
        "comments/<int:pk>/delete/",
        DeleteCommentView.as_view()
    ),

    # votes
    path(
        "vote/",
        VoteView.as_view()
    ),

    # notifications
    path(
        "notifications/",
        NotificationListView.as_view()
    ),

    path(
        "notifications/unread-count/",
        NotificationUnreadCountView.as_view()
    ),

    path(
        "notifications/<int:notification_id>/mark-read/",
        MarkNotificationReadView.as_view()
    ),
]