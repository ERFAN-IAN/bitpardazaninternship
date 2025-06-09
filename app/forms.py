from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget
from .models import Book, BookCategory, Author, UserProfile
from django_select2.forms import ModelSelect2Widget, Select2MultipleWidget
from phonenumber_field.formfields import PhoneNumberField
from django.forms.widgets import ClearableFileInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django.core.validators import MinLengthValidator, ValidationError, BaseValidator
from django.utils.translation import gettext_lazy as _
import datetime

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'app/customformuserprofile.html'
    initial_text = ''  # Remove "Currently:"
    input_text = 'Change'  # Customize input label
    clear_checkbox_label = 'Remove'  # Customize clear checkbox label


class MinMaxValidator(BaseValidator):
    message = _("Value %(value)s must be between %(min_value)s and %(max_value)s.")
    code = "min_max_value"

    def __init__(self, min_value, max_value, message=None, *args, **kwargs):
        super().__init__(limit_value=min_value, message=message, *args, **kwargs)
        self.max_value = max_value

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {"min_value": self.limit_value, "max_value": self.max_value, "value": cleaned}
        if not self.compare(self.limit_value, cleaned, self.max_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def compare(self, a, b, c):
        return a <= b <= c

class UserSignupForm(UserCreationForm):
    father_name = forms.CharField(max_length=150, required=True, label="Father's Name")
    phone_number = PhoneNumberField(required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['username', 'father_name', 'password1', 'password2', 'phone_number']


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
        fields = ["title", "release_date", "author", "category", "image", "price"]
        widgets = {
            'category': Select2Widget(),
        }


class CategoryAjaxWidget(ModelSelect2Widget):
    model = BookCategory
    search_fields = ['title__icontains']


class BookFormSingleAjax(forms.ModelForm):
    release_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']  # format expected from datetime-local input
    )
    title = forms.CharField(validators=[MinLengthValidator(5, 'Title should be at least 5 characters long')])
    price = forms.DecimalField(validators=[MinMaxValidator(10, 1000)])
    class Meta:
        model = Book
        fields = ["title", "release_date", "category", "image", "price"]
        widgets = {
            'category': CategoryAjaxWidget(
                attrs={'data-placeholder': 'Select a category', 'style': 'width: 100%;'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookFormSingleAjax, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        user_groups = self.user.groups.values_list('name', flat=True)
        if "Admin" not in user_groups and not self.user.is_superuser:
            self.fields['release_date'].widget = forms.HiddenInput()
            self.fields['release_date'].initial = datetime.datetime.now()
        self.helper.layout = Layout(
            Fieldset(
                "Add Book",
                "title",
                "release_date",
                "category",
                "image",
                "price"
            ),
            Submit('submit', 'submit', css_class='btn-primary'),
        )

    def clean_image(self):
        max_size = 10 * 1024 * 1024
        image = self.cleaned_data["image"]
        if image:
            if image.size > max_size:
                raise forms.ValidationError("Image should be smaller than 10MB!")
        return image


class BookSelectForm(forms.Form):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label="Author",
        widget=ModelSelect2Widget(
            model=Author,
            search_fields=['first_name__icontains', 'last_name__icontains'],
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


# class BookSelectForm(forms.Form):
#     author = forms.ModelChoiceField(
#         queryset=Author.objects.all(),
#         label="Author",
#         widget=Select2Widget(
#             attrs={
#                 'data-placeholder': 'Select an author',
#                 'style': 'width: 100%;',  # Make the select2 widget full width
#             }
#         )
#     )
#
#     book = forms.ModelChoiceField(
#         queryset=Book.objects.all(),
#         label="Book",
#         widget=Select2Widget(
#             attrs={
#                 'data-placeholder': 'Select a book',
#                 'style': 'width: 100%;',  # Make the select2 widget full width
#                 'disabled': 'disabled'
#             },
#
#         )
#     )
#
#     def __init__(self, *args, **kwargs):
#         author_id = kwargs.pop('author_id', None)
#         super().__init__(*args, **kwargs)
#         if author_id:
#             # Filter books by author if author_id is provided
#             self.fields['book'].queryset = Book.objects.filter(author_id=author_id)
#         else:
#             # No author selected, empty queryset or all books
#             self.fields['book'].queryset = Book.objects.none()


class ForgotPasswordForm(forms.Form):
    user_name = forms.CharField(max_length=150, label="Username", required=False)
    phone_number = PhoneNumberField(label='Phone Number', required=False)

    def clean(self):
        cleaned_data = super().clean()
        user_name = cleaned_data.get('user_name')
        phone_number = cleaned_data.get('phone_number')

        if not user_name and not phone_number:
            raise forms.ValidationError(
                "Please provide either your username or your phone number."
            )
        if user_name or phone_number:
            if not User.objects.filter(profile__phone_number=phone_number).exists() and not User.objects.filter(
                    username=user_name).exists():
                raise forms.ValidationError('Neither username nor phone number exist')
        return cleaned_data


class ConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6)


class SmsConfirmCodeForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pop 'user' from kwargs
        self.request = kwargs.pop('request', None)  # Optional: pop 'request' if needed
        super().__init__(*args, **kwargs)

    def get_user(self):
        return self.user


class TestForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "release_date", "author", "category", "image"]
        widgets = {'category': Select2MultipleWidget()}


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
        widgets = {
            'avatar': CustomClearableFileInput,
        }


class ContactusForm(forms.Form):
    author_name = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super(ContactusForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Contact Us",
                "author_name",
                "message",
            ),
            Submit('submit', 'Send Email', css_class='btn-primary'),
        )

