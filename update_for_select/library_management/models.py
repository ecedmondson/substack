from django.db import models
from django.utils import timezone


# Yeah, I could use user or make a customer user but this is throwaway code.
class Patron(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    membership_card_id = models.UUIDField()



class Book(models.Model):
    title = models.CharField(max_length=255)
    author_first_name = models.CharField(max_length=255)
    author_last_name = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    publication_date = models.DateField()
    catalogued = models.DateField()
    genre = models.CharField(max_length=255)


class BookLoan(models.Model):
    book = models.ForeignKey(Book, related_name="bookloans", on_delete=models.CASCADE)
    patron = models.ForeignKey(
        Patron, related_name="bookloans", on_delete=models.CASCADE
    )
    checked_out_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    book_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} loaned to {self.patron.first_name} {self.patron.last_name}"

    @property
    def is_overdue(self):
        """Returns whether the book loan is overdue."""
        return self.book_returned is None and self.due_date < timezone.now()
    
    @property
    def property_decorated_method(self):
        return "The property"
    
    def method_with_no_args(self):
        return "method with no args"
    
    def method_with_a_kwarg(self, my_kwarg_list=None):
        my_kwarg_list = my_kwarg_list or ["kwarg"]
        return "this is my list of kwargs: " + "\n\t-".join(my_kwarg_list)

    def book_return(self, return_date=None):
        """Marks the book as returned."""
        return_date = return_date or timezone.now()
        self.book_returned = return_date
        self.save(update_fields=["book_returned"])
    
    def serialize_me(self, number_to_add, number_to_subtract=None):
        result = number_to_add + 7
        if number_to_subtract:
            return result - number_to_subtract
        return result
