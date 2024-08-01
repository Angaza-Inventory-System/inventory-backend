import os

from haystack.query import SearchQuerySet


class SearchAndLimitMixin:
    search_fields = []
    filterset_fields = []
    ordering_fields = []
    ordering = []

    def search_queryset(self, queryset, search_query):
        if search_query:
            sqs = (
                SearchQuerySet()
                .models(self.queryset.model)
                .filter(content=search_query)
            )
            object_ids = [result.pk for result in sqs]
            pk_field = self.get_pk_field()
            queryset = queryset.filter(**{f"{pk_field}__in": object_ids})
        return queryset

    def get_pk_field(self):
        return self.queryset.model._meta.pk.name

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)
        limit = self.request.query_params.get("limit", None)

        queryset = self.search_queryset(queryset, search_query)

        # Apply limit after all other query modifications
        if limit:
            queryset = queryset[: int(limit)]

        return queryset
