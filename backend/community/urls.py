from django.urls import path
from .views import CommentList, CommentReactionCreate, PostListCreate, CommentCreate, PostRetrieveAPIView

urlpatterns = [
    path('posts/', PostListCreate.as_view()),
    path('posts/<int:post_id>/comment/', CommentCreate.as_view()),
    path('posts/<int:post_id>/comments/', CommentList.as_view()),
    path('comments/<int:comment_id>/react/', CommentReactionCreate.as_view()),
    path('posts/<int:post_id>/', PostRetrieveAPIView.as_view()),
]