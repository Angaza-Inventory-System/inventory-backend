import os
from haystack.query import SearchQuerySet
from rest_framework.response import Response
from rest_framework import generics
from .pagination import CustomPagination  # Ensure the correct import path

class SearchAndLimitMixin:
    search_fields = []
    filterset_fields = []
    ordering_fields = []
    ordering = []

    def search_queryset(self, queryset, search_query):
        if search_query:
            sqs = SearchQuerySet().models(self.queryset.model).filter(content=search_query)
            for field in self.search_fields:
                sqs = sqs.filter(**{f"{field}__icontains": search_query})
            object_ids = [result.pk for result in sqs]
            pk_field = self.queryset.model._meta.pk.name
            queryset = queryset.filter(**{f"{pk_field}__in": object_ids})
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)

        queryset = self.search_queryset(queryset, search_query)
        
        paginator = CustomPagination()
        page = self.request.query_params.get('page', 1)
        paginated_queryset = paginator.paginate_queryset(queryset, self.request)
        
        return paginated_queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.request.query_params.get('page', 1)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
