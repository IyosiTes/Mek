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
    Q,
    BooleanField,
)
from django.db.models.functions import Coalesce, Substr

#from backend.accounts import serializers
from .pagination import PostPagination, CommentPagination, NotificationPagination
from .serializers import (CommentUpdateSerializer, 
PostFeedSerializer, 
PostCreateSerializer, 
PostDetailSerializer,
CommentSerializer, 
NotificationSerializer, PostUpdateSerializer,
VoteRequestSerializer)
from .models import Post, Comment, Vote, Notification
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated

class PostFeedView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = PostFeedSerializer
    pagination_class = PostPagination

    def get_queryset(self):

        user = (
            self.request.user
            if self.request.user.is_authenticated
            else None
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

        upvote_count_subquery = (
           Vote.objects
           .filter(
               post=OuterRef("pk"),
              value=Vote.UPVOTE,
         )
           .values("post")
           .annotate(
           total=Count("id")
        )
          .values("total")[:1]
    )
        
        downvote_count_subquery = (
           Vote.objects
              .filter(
                post=OuterRef("pk"),
                 value=Vote.DOWNVOTE,
             )
              .values("post")
              .annotate(
         total=Count("id")
         )
           .values("total")[:1]
        )

        if user:

            user_vote_subquery = (
                Vote.objects
                .filter(
                    user=user,
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
                    author_id=user.id,
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
                "author", 
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
                upvote_count=Coalesce(
                    Subquery(upvote_count_subquery),
                    Value(0),
                      output_field=IntegerField(),
                ),

                downvote_count=Coalesce(
                    Subquery(downvote_count_subquery),
                    Value(0),
                    output_field=IntegerField(),
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
                "author_id",
               
            )
            .order_by(
                "-is_pinned",
                "-created_at"
            )
        )
class CreatePostView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )

class UpdatePostView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = PostUpdateSerializer

    lookup_field = "public_id"

    queryset = Post.objects.filter(
        is_deleted=False
    )

    def get_object(self):

        post = super().get_object()

        if post.author_id != self.request.user.id:
            raise PermissionDenied(
                "You cannot edit this post."
            )

        if post.is_admin_post:
            raise PermissionDenied(
                "Admin posts cannot be edited."
            )

        return post        

class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, public_id):

        post = get_object_or_404(
            Post,
            public_id=public_id,
            is_deleted=False
        )

        if post.author_id != request.user.id:
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
    permission_classes = [AllowAny]

    serializer_class = PostDetailSerializer

    lookup_field = "public_id"

    def get_queryset(self):

        user = (
          self.request.user
          if self.request.user.is_authenticated
          else None
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

        upvote_count_subquery = (
    Vote.objects
    .filter(
        post=OuterRef("pk"),
        value=Vote.UPVOTE,
    )
    .values("post")
    .annotate(
        total=Count("id")
    )
    .values("total")[:1]
)

        downvote_count_subquery = (
    Vote.objects
    .filter(
        post=OuterRef("pk"),
        value=Vote.DOWNVOTE,
    )
    .values("post")
    .annotate(
        total=Count("id")
    )
    .values("total")[:1]
)

        if user:

            user_vote_subquery = (
                Vote.objects
                .filter(
                    user=user,
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
                "author",
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
                upvote_count=Coalesce(
    Subquery(upvote_count_subquery),
    Value(0),
    output_field=IntegerField(),
),

               downvote_count=Coalesce(
    Subquery(downvote_count_subquery),
    Value(0),
    output_field=IntegerField(),
),

                user_vote=user_vote_annotation
            )
            .only(
                "public_id",
                "author_id",
                "content",
                "image_url",
                "is_admin_post",
                "is_pinned",
                "created_at",
                "updated_at",  
            )
        )
class CommentListView(ListAPIView):
    permission_classes = [AllowAny]

    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):

        post_id = self.kwargs["post_id"]

        user = (
    self.request.user
    if self.request.user.is_authenticated
    else None
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
        upvote_count_subquery = (
    Vote.objects
    .filter(
        comment=OuterRef("pk"),
        value=Vote.UPVOTE,
    )
    .values("comment")
    .annotate(
        total=Count("id")
    )
    .values("total")[:1]
)

        downvote_count_subquery = (
    Vote.objects
    .filter(
        comment=OuterRef("pk"),
        value=Vote.DOWNVOTE,
    )
    .values("comment")
    .annotate(
        total=Count("id")
    )
    .values("total")[:1]
)

        if user:

            user_vote_subquery = (
                Vote.objects
                .filter(
                    comment=OuterRef("pk"),
                    user=user
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
                    author_id=user.id,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )

            is_post_creator_annotation = Case(
                When(
                    author_id=F("post__author_id"),
                    then=Value(True),
                 ),
                default=Value(False),
                output_field=BooleanField(),
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

            is_post_creator_annotation = Value(
                False,
                output_field=BooleanField()
            )

        return (
            Comment.objects
            .filter(
                post_id=post_id,
            )
            .select_related(
                "author",
                "parent",
                "post"
            )
            .annotate(
                vote_score=Coalesce(
                    Subquery(
                        vote_score_subquery,
                        output_field=IntegerField()
                    ),
                    Value(0)
                ),

                upvote_count=Coalesce(
    Subquery(upvote_count_subquery),
    Value(0),
    output_field=IntegerField(),
),

                downvote_count=Coalesce(
    Subquery(downvote_count_subquery),
    Value(0),
    output_field=IntegerField(),
),

                user_vote=user_vote_annotation,

                is_author=is_author_annotation,

                is_post_creator=is_post_creator_annotation,

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
            .order_by("created_at")
        )
       
class UpdateCommentView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CommentUpdateSerializer

    queryset = (
        Comment.objects
        .filter(is_deleted=False)
    )

    def get_object(self):

        comment = super().get_object()

        user = self.request.user

        if comment.author_id != user.id:
            raise PermissionDenied(
                "You cannot edit this comment."
            )

        return comment  

class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        comment = get_object_or_404(
            Comment,
            pk=pk,
            is_deleted=False
        )

        if comment.author_id != request.user.id:
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
    permission_classes = [IsAuthenticated]

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

            if parent.post != post:
                raise serializer.ValidationError(
                    "Parent comment must belong to the same post."
                )
            if parent.is_deleted:
                raise serializer.ValidationError(
                    "Parent comment has been deleted."
                )

        comment = serializer.save(
            author=self.request.user,
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
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        serializer = VoteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        value = data["value"]
        post_id = data.get("post_id")
        comment_id = data.get("comment_id")

        if post_id:

            target = get_object_or_404(
                Post,
                public_id=post_id,
                is_deleted=False,
            )

            vote_filter = {
                "user": request.user,
                "post": target,
            }

            score_filter = {
                "post": target,
            }

        else:

            target = get_object_or_404(
                Comment,
                pk=comment_id,
                is_deleted=False,
            )

            vote_filter = {
                "user": request.user,
                "comment": target,
            }

            score_filter = {
                "comment": target,
            }

        if value == 0:

            Vote.objects.filter(**vote_filter).delete()
            status_text = "removed"

        else:

            Vote.objects.update_or_create(
                defaults={
                    "value": value,
                },
                **vote_filter,
            )

            status_text = "ok"

        vote_stats = (
            Vote.objects
            .filter(**score_filter)
            .aggregate(
                vote_score=Coalesce(
                    Sum("value"),
                    Value(0),
                    output_field=IntegerField(),
                ),
                upvote_count=Count(
                    "id",
                    filter=Q(value=Vote.UPVOTE),
                ),
                downvote_count=Count(
                    "id",
                    filter=Q(value=Vote.DOWNVOTE),
                ),
            )
        )

        return Response({
            "status": status_text,
            "user_vote": value,
            **vote_stats,
        })
    

class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):

        return (
            Notification.objects
            .filter(
                recipient=self.request.user
            )
            .select_related(
                "actor",
                "post",
                "comment"
            )
        )
    
class NotificationUnreadCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        count = (
            Notification.objects
            .filter(
                recipient=request.user,
                is_read=False
            )
            .count()
        )

        return Response({
            "count": count
        })

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(
        self,
        request,
        notification_id
    ):

        notification = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user
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

    permission_classes = [IsAuthenticated]

    def post(self, request):

        updated = (
            Notification.objects
            .filter(
                recipient=request.user,
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
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):

        return (
            Notification.objects
            .filter(
                recipient=self.request.user
            )
        )       















































    