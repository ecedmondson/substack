import json
from uuid import uuid4
from django.db import migrations
from django.utils.timezone import now, timedelta
books = [
    {
        "title": "Butter",
        "author_first_name": "Asako",
        "author_last_name": "Yuzuki",
        "isbb": "9780063236400",
        "publication_date": "April 16, 2024",
        "genre": "Mystery",
    },
    {
        "title": "History",
        "author_first_name": "Elsa",
        "author_last_name": "Morante",
        "isbb": "9781586420048",
        "publication_date": "October 1, 2000",
        "genre": "Historical Fiction",
    },
    {
        "title": "Figuring",
        "author_first_name": "Maria",
        "author_last_name": "Popova",
        "isbb": "9781524748135",
        "publication_date": "February 5, 2019",
        "genre": "Non-Fiction",
    },
    {
        "title": "Liars",
        "author_first_name": "Sarah",
        "author_last_name": "Manguso",
        "isbb": "9780593241257",
        "publication_date": "July 23, 2024",
        "genre": "Thriller",
    },
    {
        "title": "Mongrel",
        "author_first_name": "Hanako",
        "author_last_name": "Footman",
        "isbb": "9781804440438",
        "publication_date": "February 8, 2024",
        "genre": "Contemporary Fiction",
    },
    {
        "title": "We Do What We Do in the Dark",
        "author_first_name": "Michelle",
        "author_last_name": "Hart",
        "isbb": "9780593329672",
        "publication_date": "May 3, 2022",
        "genre": "LGBT",
    },
    {
        "title": "Tender is the Flesh",
        "author_first_name": "Augstina",
        "author_last_name": "Bazterrica",
        "isbb": "9781982150921",
        "publication_date": "August 4, 2020",
        "genre": "Horror",
    },
    {
        "title": "Circe",
        "author_first_name": "Madeline",
        "author_last_name": "Miller",
        "isbb": "9780316556347",
        "publication_date": "April 10, 2018",
        "genre": "Mythology",
    },
    {
        "title": "Parable of the Sower",
        "author_first_name": "Octavia",
        "author_last_name": "Butler",
        "isbb": "9780446675505",
        "publication_date": "October 1, 1993",
        "genre": "Dystopia",
    },
]

patrons = [
    {
        "first_name": "JJ",
        "last_name": "Flewellen",
        "email": "jj.flewellen@cats.com"
    },
    {
        "first_name": "Emily",
        "last_name": "Edmondson",
        "email": "emily@edmondsonreportingservices.com"
    }
]

def populate_db(apps, schema_editor):
    Book = apps.get_model("library_management", "Book")
    Patron = apps.get_model("library_management", "Patron")
    BookLoan = apps.get_model("library_management", "BookLoan")

    # Create books
    book_instances = {}
    for book_data in books:
        book = Book.objects.create(
            title=book_data["title"],
            author_first_name=book_data["author_first_name"],
            author_last_name=book_data["author_last_name"],
            isbn=book_data["isbb"],
            publication_date=book_data["publication_date"],
            catalogued=now().date(),
            genre=book_data["genre"],
        )
        book_instances[book_data["title"]] = book

    # Create patrons
    patron_instances = {}
    for patron_data in patrons:
        patron = Patron.objects.create(
            first_name=patron_data["first_name"],
            last_name=patron_data["last_name"],
            email=patron_data["email"],
            membership_card_id=uuid4(),
        )
        patron_instances[patron_data["email"]] = patron

    # Create book loans for JJ Flewellen
    jj = patron_instances["jj.flewellen@cats.com"]

    # Loan 1: Returned
    BookLoan.objects.create(
        book=book_instances["Butter"],
        patron=jj,
        due_date=now() - timedelta(days=15),
        book_returned=now() - timedelta(days=10),
    )

    # Loan 2: Overdue
    BookLoan.objects.create(
        book=book_instances["History"],
        patron=jj,
        due_date=now() - timedelta(days=5),
    )

    # Loan 3: Currently checked out and not overdue
    BookLoan.objects.create(
        book=book_instances["Figuring"],
        patron=jj,
        due_date=now() + timedelta(days=10),

class Migration(migrations.Migration):
    dependencies = [
        ("library_management", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_db),
    ]