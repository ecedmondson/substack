from django.db import connection
from library_management.api.serializers import BookSerializer
from library_management.models import Book
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BookPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class BookListView(generics.ListAPIView):
    queryset = Book.objects.prefetch_related("bookloans").all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get(self, request, *args, **kwargs):
        queryset_filters = {}
        genre = request.query_params.get("genre", None)

        if genre:
            queryset_filters["genre"] = genre

        queryset = self.get_queryset().filter(**queryset_filters)
        print("Before serialization:")
        if not connection.queries:
            print("No queries executed.")
        for query in connection.queries:
            print(f"\t{query['sql']}")
            print()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data_to_return = self.get_paginated_response(serializer.data)
            print("After serialization:")
            for query in connection.queries:
                    print(f"\t{query['sql']}")
                    print()
            return data_to_return
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
