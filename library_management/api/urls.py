from django.urls import path
from .views import BookListView

urlpatterns = [
    path("api/books/", BookListView.as_view(), name="book-list"),
]
