from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
import math

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of devices per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Maximum number of devices per page

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