from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, BooleanFilter, NumericRangeFilter, RangeFilter
from .models import Author, Book, BookCategory, Purchase
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


class PurchaseFilter(FilterSet):
    is_expensive = BooleanFilter(method="filter_expensive", label="Is Expensive")
    price = RangeFilter(field_name='price')

    def filter_expensive(self, queryset, name, value):
        if value:
            return queryset.filter(price__gt=100)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_groups = self.request.user.groups.values_list('name', flat=True)
        if "Operator" in user_groups:
            self.filters.pop('user__username__icontains')

    class Meta:
        model = Purchase
        fields = {"book__title": ['icontains'], "user__username": ['icontains']}