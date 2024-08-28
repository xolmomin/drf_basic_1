from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 5


class CustomCursorPagination(CursorPagination):
    ordering = 'created_at',

    def get_paginated_response(self, data):
        return Response({
            'vali': 1,
            'ali': 2,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
        })
