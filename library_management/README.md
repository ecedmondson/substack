## Library Management 

Library Management is a hastily thrown together django app intended to demonstrate a prodution bug 
I wrote in a previous role. As such, I very intentionally added a bug (in the serializer code), and
very intentionally _did not really think too deeply_ about anything else. This code should not be considered
production-ready or representative of a django app with best practices.

If you are looking for the bug in the serializer code, the bug is this:

```python
    returned_date = serializers.ReadOnlyField(source="book_return")
```

This source references a classmethod with no positional args. As such, Django Rest Framework is fine, actually, calling it.
Since the method returns the books, this means that a fetch api is writing to the DB. 