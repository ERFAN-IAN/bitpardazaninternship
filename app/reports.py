from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from django.db.models import Count, Sum, Avg
from .models import Author, Book, Purchase
from braces.views import GroupRequiredMixin


class BookSalesReport(GroupRequiredMixin, ReportView):
    template_name = "app/customslickreporting.html"
    report_model = Purchase
    date_field = "purchased_at"
    group_by = "book__title"
    group_required = ['Admin']
    columns = [
        "book__title",
        "book__author__first_name",
        "book__author__last_name",
        "book__category__title",
        ComputationField.create(Sum, "price", name="price__sum", verbose_name="Total Sales ($)"),
        ComputationField.create(Count, "id", name="id__count", verbose_name="Number of Purchases"),
    ]

    chart_settings = [
        Chart("Number of Purchases by Book", Chart.PIE, data_source=["id__count"], title_source=["book__title"]),
        Chart("Total Sales by Book", Chart.PIE, data_source=["price__sum"], title_source=["book__title"]),

    ]


class BookPublicationReport(GroupRequiredMixin, ReportView):
    template_name = "app/customslickreporting.html"
    report_model = Book
    date_field = "release_date"
    group_by = "publication_year"
    group_required = ['Admin']
    columns = [
        "publication_year",
        ComputationField.create(Sum, "price", name="price__sum", verbose_name="Total Price ($)"),
        ComputationField.create(Count, "id", name="id__count", verbose_name="Number of Books"),
    ]

    chart_settings = [
        Chart("Total Price by Publication Year", Chart.LINE, data_source=["price__sum"],
              title_source=["publication_year"]),
        Chart("Books Published per Year", Chart.BAR, data_source=["id__count"], title_source=["publication_year"]),
    ]


class AuthorByCountryReport(GroupRequiredMixin, ReportView):
    template_name = "app/customslickreporting.html"
    report_model = Author
    group_by = "country__name"
    group_required = ['Admin']
    columns = [
        "country__name",
        ComputationField.create(Count, "id", name="author_count", verbose_name="Number of Authors"),
        ComputationField.create(Avg, "age", name="average_age", verbose_name="Average Age"),
    ]

    chart_settings = [
        Chart(
            "Number of Authors by Country",
            Chart.BAR,
            data_source=["author_count"],
            title_source=["country__name"],
        ),
        Chart(
            "Average Age of Authors by Country",
            Chart.LINE,
            data_source=["average_age"],
            title_source=["country__name"],
        ),
    ]
