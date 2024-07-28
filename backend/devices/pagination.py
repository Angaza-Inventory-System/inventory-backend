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

import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = "page_size"
    max_page_size = 100  # Maximum number of items per page

    def get_page_size(self, request):
        """
        Returns the page size based on the request query parameter.
        If the query parameter is not provided, returns the default page size.
        """
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size is not None:
            try:
                page_size = int(page_size)
                if page_size > 0 and page_size <= self.max_page_size:
                    return page_size
            except ValueError:
                pass
        return self.page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": math.ceil(
                    self.page.paginator.count / self.get_page_size(self.request)
                ),
                "results": data,
            }
        )
