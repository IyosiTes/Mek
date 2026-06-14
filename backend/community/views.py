from django.db.models import (
    Case,
    CharField,
    Count,
    Sum,
    F,
    Value,
    IntegerField,
    OuterRef,
    Subquery,
    When,
    BooleanField,
)
from django.db.models.functions import Coalesce, Substr

#from backend.accounts import serializers
from .pagination import PostPagination, CommentPagination, NotificationPagination
from .serializers import (CommentUpdateSerializer, 
CommunityUserSerializer,
PostFeedSerializer, 
PostCreateSerializer, 
PostDetailSerializer,
CommentSerializer, 
NotificationSerializer,
VoteRequestSerializer)
from .models import Post, Comment, Vote, Notification
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.db import transaction

class PostFeedView(ListAPIView):

    serializer_class = PostFeedSerializer
    pagination_class = PostPagination

    def get_queryset(self):

        community_user = getattr(
            self.request,
            "community_user",
            None
        )

        comment_count_subquery = (
            Comment.objects
            .filter(
                post=OuterRef("pk"),
                is_deleted=False
            )
            .values("post")
            .annotate(
                total=Count("id")
            )
            .values("total")[:1]
        )

        vote_score_subquery = (
            Vote.objects
            .filter(
                post=OuterRef("pk")
            )
            .values("post")
            .annotate(
                total=Sum("value")
            )
            .values("total")[:1]
        )

        if community_user:

            user_vote_subquery = (
                Vote.objects
                .filter(
                    user=community_user,
                    post=OuterRef("pk")
                )
                .values("value")[:1]
            )

            user_vote_annotation = Coalesce(
                Subquery(user_vote_subquery),
                Value(0),
                output_field=IntegerField()
            )

            is_author_annotation = Case(
                When(
                    author_id=community_user.id,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )

        else:

            user_vote_annotation = Value(
                0,
                output_field=IntegerField()
            )

            is_author_annotation = Value(
                False,
                output_field=BooleanField()
            )

        return (
            Post.objects
            .filter(
                is_deleted=False
            )
            .select_related(
                "author"
            )
            .annotate(
                comment_count=Coalesce(
                    Subquery(comment_count_subquery),
                    Value(0),
                    output_field=IntegerField()
                ),

                vote_score=Coalesce(
                    Subquery(vote_score_subquery),
                    Value(0),
                    output_field=IntegerField()
                ),

                user_vote=user_vote_annotation,

                is_author=is_author_annotation,
            )
            .only(
                "public_id",
                "content",
                "image_url",
                "is_admin_post",
                "is_pinned",
                "created_at",

                "author__display_name",
                "author__avatar",
                "author__is_verified",
            )
            .order_by(
                "-is_pinned",
                "-created_at"
            )
        )
class CreatePostView(CreateAPIView):

    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.community_user
        )

class UpdatePostView(UpdateAPIView):

    serializer_class = PostCreateSerializer

    lookup_field = "public_id"

    queryset = Post.objects.filter(
        is_deleted=False
    )

    def get_object(self):

        post = super().get_object()

        if post.author_id != self.request.community_user.id:
            raise PermissionDenied(
                "You cannot edit this post."
            )

        if post.is_admin_post:
            raise PermissionDenied(
                "Admin posts cannot be edited."
            )

        return post        

class DeletePostView(APIView):

    def post(self, request, public_id):

        post = get_object_or_404(
            Post,
            public_id=public_id,
            is_deleted=False
        )

        if post.author_id != request.community_user.id:
            raise PermissionDenied(
                "You cannot delete this post."
            )

        if post.is_admin_post:
            raise PermissionDenied(
                "Admin posts cannot be deleted."
            )

        post.is_deleted = True

        post.save(
            update_fields=["is_deleted"]
        )

        return Response({
            "success": True
        })        

class PostDetailView(RetrieveAPIView):

    serializer_class = PostDetailSerializer

    lookup_field = "public_id"

    def get_queryset(self):

        community_user = getattr(
            self.request,
            "community_user",
            None
        )

        comment_count_subquery = (
            Comment.objects
            .filter(
                post=OuterRef("pk"),
                is_deleted=False
            )
            .values("post")
            .annotate(
                total=Count("id")
            )
            .values("total")[:1]
        )

        vote_score_subquery = (
            Vote.objects
            .filter(
                post=OuterRef("pk")
            )
            .values("post")
            .annotate(
                total=Coalesce(
                    Sum("value"),
                    0
                )
            )
            .values("total")[:1]
        )

        if community_user:

            user_vote_subquery = (
                Vote.objects
                .filter(
                    user=community_user,
                    post=OuterRef("pk")
                )
                .values("value")[:1]
            )

            user_vote_annotation = Coalesce(
                Subquery(
                    user_vote_subquery
                ),
                Value(0),
                output_field=IntegerField()
            )

        else:

            user_vote_annotation = Value(
                0,
                output_field=IntegerField()
            )

        return (
            Post.objects
            .filter(
                is_deleted=False
            )
            .select_related(
                "author"
            )
            .annotate(
                comment_count=Coalesce(
                    Subquery(
                        comment_count_subquery
                    ),
                    Value(0),
                    output_field=IntegerField()
                ),

                vote_score=Coalesce(
                    Subquery(
                        vote_score_subquery
                    ),
                    Value(0),
                    output_field=IntegerField()
                ),

                user_vote=user_vote_annotation
            )
            .only(
                "public_id",
                "content",
                "image_url",
                "is_admin_post",
                "is_pinned",
               # "is_deleted",
                "created_at",
                "updated_at",

                "author__uuid",
                "author__display_name",
                "author__avatar",
                "author__is_verified",
            )
        )
class CommentListView(ListAPIView):

    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):

        post_id = self.kwargs["post_id"]

        community_user = getattr(
            self.request,
            "community_user",
            None
        )

        vote_score_subquery = (
            Vote.objects
            .filter(
                comment=OuterRef("pk")
            )
            .values("comment")
            .annotate(
                total=Sum("value")
            )
            .values("total")[:1]
        )

        if community_user:

            user_vote_subquery = (
                Vote.objects
                .filter(
                    comment=OuterRef("pk"),
                    user=community_user
                )
                .values("value")[:1]
            )

            user_vote_annotation = Coalesce(
                Subquery(
                    user_vote_subquery,
                    output_field=IntegerField()
                ),
                Value(0)
            )

            is_author_annotation = Case(
                When(
                    author_id=community_user.id,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )

        else:

            user_vote_annotation = Value(
                0,
                output_field=IntegerField()
            )

            is_author_annotation = Value(
                False,
                output_field=BooleanField()
            )

        return (
            Comment.objects
            .filter(
                post_id=post_id,
            )
            .select_related(
                "author"
            )
            .annotate(
                vote_score=Coalesce(
                    Subquery(
                        vote_score_subquery,
                        output_field=IntegerField()
                    ),
                    Value(0)
                ),

                user_vote=user_vote_annotation,

                is_author=is_author_annotation,

                reply_preview=Case(
                    When(
                        parent__is_deleted=True,
                        then=Value("[deleted]")
                    ),
                    When(
                        parent__isnull=False,
                        then=Substr(
                            F("parent__content"),
                            1,
                            80
                        )
                    ),
                    default=Value(None),
                    output_field=CharField()
                )
            )
            .order_by("-created_at")
        )
       
class UpdateCommentView(UpdateAPIView):

    serializer_class = CommentUpdateSerializer

    queryset = (
        Comment.objects
        .filter(is_deleted=False)
    )

    def get_object(self):

        comment = super().get_object()

        community_user = self.request.community_user

        if comment.author_id != community_user.id:
            raise PermissionDenied(
                "You cannot edit this comment."
            )

        return comment  

class DeleteCommentView(APIView):

    def post(self, request, pk):

        comment = get_object_or_404(
            Comment,
            pk=pk,
            is_deleted=False
        )

        if comment.author_id != request.community_user.id:
            raise PermissionDenied(
                "You cannot delete this comment."
            )

        comment.is_deleted = True
        comment.content = "[deleted]"

        comment.save(
            update_fields=[
                "is_deleted",
                "content"
            ]
        )

        return Response(
            {"detail": "Comment deleted."},
            status=status.HTTP_200_OK
        )      

class CreateCommentView(CreateAPIView):

    serializer_class = CommentSerializer

    @transaction.atomic
    def perform_create(self, serializer):

        post = get_object_or_404(
            Post,
            public_id=self.kwargs["post_id"],
            is_deleted=False
        )

        parent = None

        parent = serializer.validated_data.get(
            "parent"
        )

        if parent:

            if parent.post_id != post.public_id:
                raise serializer.ValidationError(
                    "Parent comment must belong to the same post."
                )
            if parent.is_deleted:
                raise serializer.ValidationError(
                    "Parent comment has been deleted."
                )

        comment = serializer.save(
            author=self.request.community_user,
            post=post,
            parent=parent
        )

        self._create_notification(
            comment
        )

    def _create_notification(
        self,
        comment
    ):

        # Reply notification

        if comment.parent:

            recipient = comment.parent.author

            if recipient.id != comment.author_id:

                Notification.objects.create(
                    recipient=recipient,
                    actor=comment.author,
                    post=comment.post,
                    comment=comment.parent,
                    notification_type=
                    Notification.REPLY_ON_COMMENT
                )

            return

        # New comment on post notification

        recipient = comment.post.author

        if recipient.id != comment.author_id:

            Notification.objects.create(
                recipient=recipient,
                actor=comment.author,
                post=comment.post,
                comment=comment,
                notification_type=
                Notification.COMMENT_ON_POST
            )


class VoteView(APIView):

    @transaction.atomic
    def post(self, request):

        serializer = VoteRequestSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        value = data["value"]
        post_id = data.get("post_id")
        comment_id = data.get("comment_id")

      

        if post_id:

            target = get_object_or_404(
                Post,
                public_id=post_id,
                is_deleted=False
            )

            vote_filter = {
                "user": request.community_user,
                "post": target
            }

            score_filter = {
                "post": target
            }

        else:

            target = get_object_or_404(
                Comment,
                pk=comment_id,
                is_deleted=False
            )

            vote_filter = {
                "user": request.community_user,
                "comment": target
            }

            score_filter = {
                "comment": target
            }

        if value == 0:

            Vote.objects.filter(
                **vote_filter
            ).delete()

            status_text = "removed"

        else:

            Vote.objects.update_or_create(
                defaults={
                    "value": value
                },
                **vote_filter
            )

            status_text = "ok"


        score = (
            Vote.objects
            .filter(
                **score_filter
            )
            .aggregate(
                total=Coalesce(
                    Sum("value"),
                    Value(0),
                    output_field=IntegerField()
                )
            )["total"]
        )


        return Response({
            "status": status_text,
            "user_vote": value,
            "vote_score": score
        })
    
class CommunityMeView(APIView):

    def get(self, request):

        serializer = CommunityUserSerializer(
            request.community_user
        )

        return Response(
            serializer.data
        )    
class NotificationListView(ListAPIView):

    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):

        return (
            Notification.objects
            .filter(
                recipient=self.request.community_user
            )
            .select_related(
                "actor",
                "post",
                "comment"
            )
        )
    
class NotificationUnreadCountView(APIView):

    def get(self, request):

        count = (
            Notification.objects
            .filter(
                recipient=request.community_user,
                is_read=False
            )
            .count()
        )

        return Response({
            "count": count
        })

class MarkNotificationReadView(APIView):

    def post(
        self,
        request,
        notification_id
    ):

        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.community_user
        )

        if not notification.is_read:

            notification.is_read = True

            notification.save(
                update_fields=["is_read"]
            )

        return Response({
            "success": True
        })
    
class MarkAllNotificationsReadView(
    APIView
):

    def post(self, request):

        updated = (
            Notification.objects
            .filter(
                recipient=request.community_user,
                is_read=False
            )
            .update(
                is_read=True
            )
        )

        return Response({
            "success": True,
            "updated": updated
        })

class DeleteNotificationView(
    DestroyAPIView
):
    
    def get_queryset(self):

        return (
            Notification.objects
            .filter(
                recipient=self.request.community_user
            )
        )       















































    