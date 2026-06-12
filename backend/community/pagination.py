from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 20

class CommentPagination(PageNumberPagination):
    page_size = 30

class NotificationPagination(PageNumberPagination):
    page_size = 15