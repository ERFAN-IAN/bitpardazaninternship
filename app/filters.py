from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Author, Book, BookCategory
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget


class BookCategoryWidget(ModelSelect2MultipleWidget):
    model = BookCategory
    search_fields = [
        'title__icontains',
    ]


class AuthorFilter(FilterSet):
    class Meta:
        model = Author
        fields = {"first_name": ["contains"], "last_name": ["contains"], "age": ["exact"],
                  "national_id": ["contains"]}


# class BookFilter(FilterSet):
#     category = ModelChoiceFilter(
#         queryset=BookCategory.objects.all(),
#         widget=BookCategoryWidget(
#             attrs={'data-placeholder': 'Select a category', 'style': 'width: 100%;'}
#         )
#     )
#     class Meta:
#         model = Book
#         fields = {'title': ['contains']}

class BookFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        queryset=BookCategory.objects.all(),
        widget=BookCategoryWidget(
            attrs={'data-placeholder': 'Select a category', 'style': 'width: 100%;'}
        )
    )
    class Meta:
        model = Book
        fields = {'title': ['contains']}
