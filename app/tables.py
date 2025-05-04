import django_tables2 as tables
from .models import Author, Book
from django.db.models import Count
from django.urls import reverse

class AuthorTable(tables.Table):
    detail = tables.LinkColumn("author_detail", kwargs={"pk": tables.A("pk")}, empty_values=())
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "age", "national_id")
        attrs = {'class': 'table table-striped'}
    def render_detail(self, record):
        return 'Details'

class AuthorBooksTable(tables.Table):
    class Meta:
        model = Book
        fields = ("title", "publication_year")
        attrs = {'class': 'table table-bordered'}

class AuthorBookCountTable(tables.Table):
    book_count = tables.Column(footer=lambda table: sum(x.book_count for x in table.data))
    class Meta:
        model = Author
        fields = ("first_name", "last_name", "book_count")
        attrs = {'class': 'table table-striped table-hover'}

    def render_book_count(self, value):
        return f"{value}"