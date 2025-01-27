from rest_framework import serializers
from library_management.models import Book, BookLoan


class BookLoanSerializer(serializers.ModelSerializer):
    checked_out_date = serializers.ReadOnlyField(source="checked_out_on")
    returned_date = serializers.ReadOnlyField(source="book_return")

    class Meta:
        model = BookLoan
        fields = ("checked_out_date", "due_date", "is_overdue", "returned_date")


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    loans = BookLoanSerializer(source="bookloans", many=True)

    def get_author(self, obj):
        return f"{obj.author_last_name}, {obj.author_first_name}"

    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "isbn",
            "publication_date",
            "genre",
            "loans",
        )
