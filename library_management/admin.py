from django.contrib import admin
from library_management.models import Patron, Book, BookLoan


@admin.register(Patron)
class PatronAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "membership_card_id")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("membership_card_id",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "publication_date", "genre")
    search_fields = ("title", "author", "isbn")
    list_filter = ("genre", "publication_date")


@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "patron",
        "checked_out_on",
        "due_date",
        "book_returned",
        "is_overdue",
    )
    search_fields = ("book__title", "patron__first_name", "patron__last_name")
    list_filter = ("checked_out_on", "due_date", "returned_on", "is_overdue")
