# # reports.py
# from slick_reporting import SlickReport
# from django.db.models import Count
# from .models import Author
#
#
# class AuthorBookReport(SlickReport):
#     title = "Author Book Report"
#     model = Author  # The model to generate the report for
#
#     # Define the columns you want to display in the report
#     columns = [
#         ('First Name', 'first_name'),
#         ('Last Name', 'last_name'),
#         ('Number of Books', 'books_count'),
#     ]
#
#     # For the "Number of Books" column, we will annotate the data to count related books
#     def get_queryset(self):
#         # Annotating the queryset with a count of books related to each author
#         queryset = Author.objects.annotate(books_count=Count('books')).all()
#         return queryset
