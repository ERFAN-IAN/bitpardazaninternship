import django_tables2 as tables
from .models import Author, Book, Purchase
import django_tables2 as tables
import jdatetime
from django.db.models import Count
from django.urls import reverse
import datetime
from django.utils.safestring import mark_safe
from django.conf import settings


class DateFormatGregorian(tables.DateTimeColumn):
    def __init__(self, *args, **kwargs):
        custom_format = kwargs.pop('format', 'H:i d-m-Y')
        super().__init__(format=custom_format, *args, **kwargs)


class DateTimeJalali(tables.Column):

    def render(self, value):
        return jdatetime.datetime.fromgregorian(datetime=value).strftime('%Y-%m-%d %H:%M')


class CurrencyColumn(tables.Column):
    def render(self, value):
        if value is None:
            return ""
        try:
            return "{:,}$".format(value)
        except (ValueError, TypeError):
            return value


# class BookTitileColumn(tables.Column):
#     def render(self, value):
#         return value



class AuthorTable(tables.Table):
    full_name = tables.Column(empty_values=(), verbose_name="full name")
    detail = tables.LinkColumn("author_detail", kwargs={"pk": tables.A("pk")}, empty_values=(),
                               exclude_from_export=True)
    icon = tables.Column(empty_values=(), verbose_name='Age State')
    country = tables.Column(empty_values=())

    class Meta:
        model = Author
        fields = ("first_name", "last_name", "age", "icon", "national_id", "country")
        attrs = {'class': 'table table-striped'}

    def render_detail(self, record):
        return 'Details'

    def render_full_name(self, record):
        return mark_safe(f'{record.first_name} {record.last_name}')

    def render_icon(self, record):
        innericon = '<i class="fa fa-child"></i>' if int(record.age) >= 19 else '<i class="fa fa-baby"></i>'
        if int(record.age) >= 41:
            innericon = '<i class="fa fa-user-injured"></i>'
        return mark_safe(f'{innericon}')

    def value_icon(self, record):
        age = int(record.age)
        if age >= 41:
            return "Elder"
        elif age >= 19:
            return "Adult"
        else:
            return "Child"

    def render_country(self, record):
        return record.country.name


class AuthorBooksTable(tables.Table):
    edit = tables.LinkColumn("edit_book", kwargs={"pk": tables.A("pk")}, empty_values=())
    delete = tables.LinkColumn("delete_book", kwargs={"pk": tables.A("pk")}, empty_values=())
    purchase = tables.LinkColumn('purchase_page', kwargs={"pk": tables.A("pk")}, empty_values=())
    price = CurrencyColumn(accessor="price")

    class Meta:
        model = Book
        fields = ("title", "publication_year", "category", "image", "release_date", 'price')
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

    def render_purchase(self, value):
        return 'Buy!'

    def render_delete(self, value):
        return "Delete"

    def render_image(self, value):
        return mark_safe(f'<img src="{settings.MEDIA_URL}{value}" style="width:200px; height:auto;">')

    def render_release_date(self, record):
        if record.release_date:
            iso_date = record.release_date.isoformat()
            # Render a span with a data attribute containing the ISO date
            return mark_safe(f'<span class="release-date" data-release-date="{iso_date}"></span>')
        return ''

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


class PurchaseTable(tables.Table):
    full_name = tables.Column(empty_values=(), verbose_name="full name")
    title = tables.Column(empty_values=(), accessor="book.title")
    author = tables.LinkColumn("author_detail", kwargs={"pk": tables.A("book.author.pk")}, empty_values=())
    author_country = tables.Column(empty_values=(), verbose_name="Author's Country")
    purchased_at = DateFormatGregorian(verbose_name='Purchase Date')
    jalali_date = DateTimeJalali(accessor='purchased_at', verbose_name='Purchase Date (Jalali)')
    price_formatted = CurrencyColumn(accessor='price')

    class Meta:
        model = Purchase
        fields = ["full_name", "title", 'price_formatted', "purchased_at", 'jalali_date']
        attrs = {'class': 'table table-striped table-hover'}

    def render_full_name(self, record):
        customer = record.user.username
        first_name = record.user.first_name
        last_name = record.user.last_name
        if first_name:
            customer = f"{first_name}"
        if last_name:
            customer = f"{last_name}"
        if first_name and last_name:
            customer = f'{first_name} {last_name}'
        return customer

    # def render_title(self, record):
    #     return record.book.title

    def render_author(self, record):
        author = record.book.author
        return f'{author.first_name} {author.last_name}'

    def render_author_country(self, record):
        return record.book.author.country.name

    # def render_jalali_date(self, record):
    #     return jdatetime.datetime.fromgregorian(date=record.purchased_at).strftime('%Y-%m-%d %H:%M')
