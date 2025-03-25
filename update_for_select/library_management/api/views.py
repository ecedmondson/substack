from rest_framework.response import Response

from rest_framework import generics
from library_management.models import Book
from library_management.api.serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination


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
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
