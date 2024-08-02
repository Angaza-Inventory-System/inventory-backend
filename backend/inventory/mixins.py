from haystack.query import SearchQuerySet

class SearchAndLimitMixin:
    """
    A mixin that provides search and limit functionalities for Django viewsets.

    Attributes:
        search_fields (list): Fields to be used for searching. This attribute is not used in the current implementation but can be extended.
        filterset_fields (list): Fields to be used for filtering. This attribute is not used in the current implementation but can be extended.
        ordering_fields (list): Fields to be used for ordering the results. This attribute is not used in the current implementation but can be extended.
        ordering (list): Default ordering fields for the queryset. This attribute is not used in the current implementation but can be extended.
    """

    search_fields = []
    filterset_fields = []
    ordering_fields = []
    ordering = []

    def search_queryset(self, queryset, search_query):
        """
        Filter the given queryset based on the search query.

        Args:
            queryset (QuerySet): The initial queryset to be filtered.
            search_query (str): The search query string to filter the queryset.

        Returns:
            QuerySet: The filtered queryset based on the search query.
        """
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
        """
        Retrieve the filtered and limited queryset based on the search query and limit parameters from the request.

        Returns:
            QuerySet: The final queryset after applying search and limit filters.
        """
        queryset = super().get_queryset()
        search_query = self.request.query_params.get("search", None)
        limit = self.request.query_params.get("limit", None)

        queryset = self.search_queryset(queryset, search_query)

        # Apply limit after all other query modifications
        if limit:
            queryset = queryset[: int(limit)]

        return queryset
