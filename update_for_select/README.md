# Update for Select

Update for Select is a [substack post](https://wwww.faulttolerance.substack.com/p/update-for-slect) written by the same author of this code. 

This directory contains code examples relevant to the post. 

## Running

Start docker the standard way:

`docker compose up -d`

This will start a postgres db container and a django app container

## Usage

I didn't configure all the localhost hostnames. So you will literally need to go to localhost:8000 after docker is running. 

I didn't spend much time making pages. There are two routes basically

```
/admin/
/api/books
```

For either you will need to create data. I suggest: 

```docker-compose exec app python manage.py createsuperuser```

This will allow you to login to the /admin and

```docker-compose exec app python manage.py shell```

Then you can create some objects:

```
from library_management.models import Book, Patron, BookLoan
from datetime import datetime
from uuid import uuid4

patron = Patron.objects.create(first_name="Emily", last_name="Flewellen", email="emily.flewellen@example.com", membership_card_id=uuid4())
book = Book.objects.create(title="Valencia", author_first_name="Michelle", author_last_name="Tea", genre="Fiction", publication_date=datetime.now(), catalogued=datetime.now())
loan = BookLoan.objets.create(book=book, patron=patron, due_date=datetime.now())
```

## Notes

There is an intentional bug in the api. More information on the bug is in the library_management/README.md. The point of this project is to show the bug, so I am unlikely to change it.
