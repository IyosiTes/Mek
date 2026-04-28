#community/pagination.py
from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50  

class CommentPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 50    