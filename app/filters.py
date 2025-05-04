from django_filters import FilterSet
from .models import Author, Book


class AuthorFilter(FilterSet):
    class Meta:
        model = Author
        fields = {"first_name": ["contains"], "last_name": ["contains"], "age": ["exact"],
                  "national_id": ["contains"]}
