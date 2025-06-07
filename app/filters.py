from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter
from .models import Author, Book, BookCategory
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from django.db.models import Q
from django.forms.widgets import TextInput


class BookCategoryWidget(ModelSelect2MultipleWidget):
    model = BookCategory
    search_fields = [
        'title__icontains',
    ]


class AuthorFilter(FilterSet):
    search = CharFilter(label="search", method="search_filter", widget=TextInput(attrs={'placeholder': 'search by name, last name and id'}))

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(national_id__icontains=value)
        )

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
