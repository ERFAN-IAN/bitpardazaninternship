import django_tables2 as tables
from .models import Author, Book
import django_tables2 as tables
import jdatetime
from django.db.models import Count
from django.urls import reverse
import datetime
from django.utils.safestring import mark_safe


class AuthorTable(tables.Table):
    full_name = tables.Column(empty_values=(), verbose_name="full name")
    detail = tables.LinkColumn("author_detail", kwargs={"pk": tables.A("pk")}, empty_values=())

    class Meta:
        model = Author
        fields = ("first_name", "last_name", "age", "national_id")
        attrs = {'class': 'table table-striped'}

    def render_detail(self, record):
        return 'Details'

    def render_full_name(self, record):
        icon = '<i class="fa fa-child"></i>' if int(record.age) >= 19 else '<i class="fa fa-baby"></i>'
        if int(record.age) >= 41:
            icon = '<i class="fa fa-user-injured"></i>'
        return mark_safe(f'{record.first_name} {record.last_name} {icon}')





class AuthorBooksTable(tables.Table):
    edit = tables.LinkColumn("edit_book", kwargs={"pk": tables.A("pk")}, empty_values=())
    delete = tables.LinkColumn("delete_book", kwargs={"pk": tables.A("pk")}, empty_values=())

    class Meta:
        model = Book
        fields = ("title", "publication_year")
        attrs = {'class': 'table table-bordered'}

    def render_publication_year(self, value):
        try:
            gregorian_date = datetime.date(int(value), 1, 1)
            jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
            return jalali_date.strftime('%Y')
        except Exception:
            return "-"

    def render_edit(self, value):
        return "Edit"

    def render_delete(self, value):
        return "Delete"

    def before_render(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if "Admin" not in user_groups and not request.user.is_superuser:
            self.columns.hide('delete')
        if not request.user.is_authenticated:
            self.columns.hide('edit')


class AuthorBookCountTable(tables.Table):
    book_count = tables.Column(footer=lambda table: sum(x.book_count for x in table.data))

    class Meta:
        model = Author
        fields = ("first_name", "last_name", "book_count")
        attrs = {'class': 'table table-striped table-hover'}

    def render_book_count(self, value):
        return f"{value}"
