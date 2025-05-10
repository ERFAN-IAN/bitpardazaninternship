from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget
from .models import Book, BookCategory, Author
from django_select2.forms import ModelSelect2Widget


class UserSignupForm(UserCreationForm):
    father_name = forms.CharField(max_length=150, required=True, label="Father's Name")

    class Meta:
        model = User
        fields = ['username', 'father_name', 'password1', 'password2']


class BookForm(forms.ModelForm):
    release_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']  # format expected from datetime-local input
    )

    class Meta:
        model = Book
        fields = ["title", "release_date", "author", "category", "image"]


class BookFormSingleNoAjax(forms.ModelForm):
    release_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']  # format expected from datetime-local input
    )

    class Meta:
        model = Book
        fields = ["title", "release_date", "author", "category", "image"]
        widgets = {
            'category': Select2Widget(),
        }


class CategoryAjaxWidget(ModelSelect2Widget):
    model = BookCategory
    search_fields = ['title__icontains']


class BookFormSingleAjax(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "release_date", "author", "category", "image"]
        widgets = {
            'category': CategoryAjaxWidget(
                attrs={'data-placeholder': 'Select a category', 'style': 'width: 100%;'}
            ),
        }
class BookSelectForm(forms.Form):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label="Author",
        widget=ModelSelect2Widget(
            model=Author,
            search_fields=['first_name__icontains','last_name__icontains'],
            attrs={
                'data-placeholder': 'Select an author',
                'style': 'width: 100%;',  # Make the select2 widget full width
            }
        )
    )

    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        label="Book",
        widget=ModelSelect2Widget(
            model=Book,
            search_fields=['title__icontains'],
            dependent_fields={'author': 'author'},
            max_results=500,
            attrs={
                'data-placeholder': 'Select a book',
                'style': 'width: 100%;',  # Make the select2 widget full width
                'disabled': 'disabled'
            },

        )
    )