"""
Custom pagination class for paginating API responses.

Attributes:
    page_size (int): Default number of items per page.
    page_size_query_param (str): Query parameter name for overriding `page_size`.
    max_page_size (int): Maximum number of items per page.

Methods:
    get_paginated_response(data):
        Returns a paginated Response object with links to next and previous pages,
        total count of items, total number of pages, and the paginated data results.
"""

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import math

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Maximum number of items per page

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': math.ceil(self.page.paginator.count / self.page_size),
            'results': data
        })
