from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
    FormView,
    View
)
from .forms import UserSignupForm, BookForm, BookFormSingleNoAjax, BookFormSingleAjax, BookSelectForm, \
    ForgotPasswordForm, ConfirmCodeForm, SmsConfirmCodeForm, TestForm, UserProfileForm, ContactusForm, PurchaseBookForm, ConfirmBookPurchaseForm
from braces.views import GroupRequiredMixin
from django.utils.dateparse import parse_datetime
from django.urls import reverse_lazy, reverse
from .models import Author, Book, BookCategory, UserProfile, Purchase, PasswordResetCode, Discount
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect
from django_tables2 import SingleTableView, SingleTableMixin
from .tables import AuthorBooksTable, AuthorTable, AuthorBookCountTable, PurchaseTable
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from django_tables2.views import MultiTableMixin
from .filters import AuthorFilter, BookFilter, PurchaseFilter
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
import random, datetime
from .utility import send_sms, otp_code_generator
from django.contrib.auth import login
from two_factor.views import LoginView as TwoFactorLoginView
from datetime import timedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import EmailMessage
from decimal import Decimal
from django.http import JsonResponse

# from django.views.generic.detail import SingleObjectMixin
# from braces.views import SuperuserRequiredMixin
# from django.contrib.auth.decorators import user_passes_test
# from django.utils.decorators import method_decorator
# from chartjs.views.pie import HighChartPieView
# from django.db.models import Sum
# from .reports import AuthorBookReport
# from django.shortcuts import render

# Create your views here.


class AuthorListView(ExportMixin, SingleTableMixin, FilterView):
    model = Author
    template_name = "app/home.html"
    table_class = AuthorTable
    context_object_name = "authors"
    filterset_class = AuthorFilter


class AuthorCreateView(GroupRequiredMixin, CreateView):
    model = Author
    fields = ["first_name", "last_name", "age", "national_id", "country"]
    template_name = "app/add_author_form.html"
    group_required = ['Operator', 'Moderator', 'Admin']

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.id})


class AuthorUpdateView(GroupRequiredMixin, UpdateView):
    model = Author
    fields = ["first_name", "last_name", "age", "national_id", "country"]
    context_object_name = "author"
    template_name = "app/edit_author_form.html"
    group_required = ['Operator', 'Moderator', 'Admin']

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.id})


class AuthorDeleteView(GroupRequiredMixin, DeleteView):
    model = Author
    template_name = "app/delete_author.html"
    success_url = reverse_lazy("home")
    group_required = ['Admin']


class AuthorDetailView(SingleTableMixin, DetailView):
    model = Author
    template_name = "app/author_detail.html"
    context_object_name = "author"
    table_class = AuthorBooksTable

    def get_table_data(self):
        books = self.object.books.all()
        book_query = self.request.GET.get("q")
        if book_query:
            books = books.filter(title__icontains=book_query)
        return books


class BookCreateView(GroupRequiredMixin, CreateView):
    model = Book
    # fields = ["title", "release_date", "image", "category"]
    template_name = "app/add_book_form.html"
    group_required = ['Operator', 'Moderator', 'Admin']
    form_class = BookFormSingleAjax

    def form_valid(self, form):
        form.instance.author = get_object_or_404(Author, id=self.kwargs["pk"])
        book_title = form.cleaned_data['title']
        book = Book.objects.filter(title=book_title, author=form.instance.author).exists()
        if book:
            messages.error(self.request, f'Book "{book_title}" has already been added!')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.kwargs["pk"]})

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs


class BookUpdateView(GroupRequiredMixin, UpdateView):
    model = Book
    # fields = ["title", "release_date", "author", "category", "image"]
    template_name = "app/edit_book_form.html"
    group_required = ['Operator', 'Moderator', 'Admin']
    form_class = BookFormSingleNoAjax

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.author.id})


class BookDeleteView(GroupRequiredMixin, DeleteView):
    model = Book
    template_name = "app/delete_book.html"
    context_object_name = "book"
    group_required = ['Admin']

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.author.id})


class AuthorBookCountView(SingleTableView):
    model = Author
    template_name = "app/AuthorBookCountView.html"
    context_object_name = "authors"
    table_class = AuthorBookCountTable

    def get_queryset(self):
        # Prefetch books related to each author
        return Author.objects.annotate(book_count=Count('books')).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context["chart_labels"] = [author.first_name for author in queryset]
        context["chart_counts"] = [author.book_count for author in queryset]
        return context


class AuthorBookMixinView(MultiTableMixin, TemplateView):
    template_name = "app/AuthorBookMixin.html"

    def get_tables(self):
        return [
            AuthorTable(Author.objects.all()),
            AuthorBooksTable(Book.objects.all())
        ]


class AuthorBookTreeView(TemplateView):
    template_name = "app/treeview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []

        for author in Author.objects.prefetch_related('books'):
            author_node = {
                "id": f"author-{author.id}",
                "text": author.first_name,
                "children": [
                    {
                        "id": f"book-{book.id}",
                        "text": book.title,
                        "children": []  # or False if using lazy loading
                    }
                    for book in author.books.all()
                ]
            }
            data.append(author_node)
        context["data"] = json.dumps(data)
        print(data)
        return context


# def author_book_tree_json(request):
#     data = []
#
#     for author in Author.objects.prefetch_related('books'):
#         author_node = {
#             "id": f"author-{author.id}",
#             "text": author.first_name,
#             "children": [
#                 {
#                     "id": f"book-{book.id}",
#                     "text": book.title,
#                     "children": False
#                 }
#                 for book in author.books.all()
#             ]
#         }
#         data.append(author_node)
#
#     return JsonResponse(data, safe=False)

class AuthorBookPieView(TemplateView):
    template_name = "app/standalone_pie_django-chartjs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Prepare data
        authors = Author.objects.annotate(book_count=Count('books'))
        chart_data = [
            {"name": author.first_name, "y": author.book_count}
            for author in authors
        ]

        context["chart_data"] = chart_data
        return context


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'app/index.html'

    # @transaction.atomic
    # def get_context_data(self, **kwargs):
    #     # with transaction.atomic():
    #     #     context = super().get_context_data(**kwargs)
    #     #     context['username'] = self.request.user.username
    #     #     context['user_list'] = User.objects.all()
    #     context = super().get_context_data(**kwargs)
    #     context['username'] = self.request.user.username
    #     context['user_list'] = User.objects.all()
    #
    #     return context
    def get_context_data(self, **kwargs):
        transaction.set_autocommit(False)
        try:
            context = super().get_context_data(**kwargs)
            context['username'] = self.request.user.username
            context['user_list'] = User.objects.all()
            transaction.commit()
        except NameError:
            transaction.rollback()
            print(NameError)
        finally:
            transaction.set_autocommit(True)

        return context


class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    # def dispatch(self, request, *args, **kwargs):
    #     # Check if the user is already logged in
    #     if request.user.is_authenticated:
    #         # Redirect to a different page (e.g., homepage or user dashboard)
    #         return redirect(self.next_page)
    #     # If the user is not authenticated, proceed with the normal login view
    #     return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = '/'  # or 'login' or wherever you want

    def dispatch(self, request, *args, **kwargs):
        # for logged-out users, otherwise they get redirected to /login/?next=/logout/
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class BookCategoryListView(ListView):
    model = BookCategory
    template_name = 'app/bookcategory_list.html'


# @method_decorator(user_passes_test(is_superuser, login_url='/login/'), name='dispatch')
class BookCategoryCreateView(GroupRequiredMixin, CreateView):
    model = BookCategory
    template_name = 'app/bookcategory_form.html'
    fields = ['title']
    success_url = reverse_lazy('bookcategory_list')
    group_required = ['Moderator', 'Admin']


# @method_decorator(user_passes_test(is_superuser, login_url='/login/'), name='dispatch')
class BookCategoryUpdateView(GroupRequiredMixin, UpdateView):
    model = BookCategory
    template_name = 'app/bookcategory_confirm_edit.html'
    fields = ['title']
    success_url = reverse_lazy('bookcategory_list')
    group_required = ['Moderator', 'Admin']


# @method_decorator(user_passes_test(is_superuser, login_url='/login/'), name='dispatch')
class BookCategoryDeleteView(GroupRequiredMixin, DeleteView):
    model = BookCategory
    template_name = 'app/bookcategory_confirm_delete.html'
    success_url = reverse_lazy('bookcategory_list')
    group_required = ['Admin']


class SignUpCreateView(CreateView):
    model = User
    template_name = 'app/signupform.html'
    form_class = UserSignupForm
    success_url = '/login'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        father_name = form.cleaned_data.get('father_name')
        phone_number = form.cleaned_data.get('phone_number')
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.father_name = father_name
        profile.phone_number = phone_number
        profile.save()
        operate_group, created = Group.objects.get_or_create(name='Operator')
        user.groups.add(operate_group)

        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class BooksListView(FilterView, ListView):
    model = Book
    template_name = 'app/booklist.html'
    filterset_class = BookFilter


class BookSelectView(FormView):
    template_name = 'app/bookselect2.html'
    form_class = BookSelectForm

    def get_success_url(self):
        book_id = self.request.POST.get('book')
        return reverse("edit_book", kwargs={"pk": book_id})
    #
    # def form_valid(self, form):
    #
    #     return super()


import logging


class BookPurchaseView(LoginRequiredMixin, FormView):
    template_name = "app/book_purchase.html"
    form_class = PurchaseBookForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = None

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        author_id = self.book.author.id
        cancel_url = reverse('author_detail', kwargs={'pk': author_id})
        book_title = self.book.title
        price = self.book.price
        kwargs.update({'cancel_url': cancel_url, 'book_title': book_title, 'price': price})
        return kwargs

    def form_valid(self, form):
        discount_code = form.cleaned_data.get('discount_code')
        if discount_code:
            self.request.session['discount_code'] = discount_code
        else:
            self.request.session.pop('discount_code', None)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("confirm_purchase", kwargs={"pk": self.kwargs["pk"]})


class CheckDiscountCodeView(View):

    def get(self, request, *args, **kwargs):
        is_valid = False
        percentage = 0
        discount_query = request.GET.get('code', '')
        discount = Discount.objects.filter(discount_code=discount_query).first()
        if discount:
            is_valid = True
            percentage = discount.percentage
        return JsonResponse({
            'is_valid': is_valid,
            'discount_amount': percentage
        })


class ConfirmBookPurchaseView(LoginRequiredMixin, FormView):
    template_name = "app/book_purchase.html"
    success_url = '/'
    form_class = ConfirmBookPurchaseForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = None
        self.discount_code = None
        self.percentage = None

    def dispatch(self, request, *args, **kwargs):
        purchase_page = reverse('purchase_page', kwargs={'pk': kwargs.get('pk')})
        confirm_page = reverse('confirm_purchase', kwargs={'pk': kwargs.get('pk')})
        prev_url = str(request.META.get('HTTP_REFERER'))
        if purchase_page not in prev_url and confirm_page not in prev_url:
            self.request.session.pop('discount_code', None)
            return redirect(reverse('purchase_page', kwargs={'pk': kwargs.get('pk')}))
        self.book = get_object_or_404(Book, pk=kwargs['pk'])
        self.discount_code = self.request.session.get('discount_code', None)
        self.percentage = self.get_discount_percentage(self.discount_code)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        author_id = self.book.author.id
        cancel_url = reverse('author_detail', kwargs={'pk': author_id})
        price = self.get_discounted_price()
        kwargs.update({'cancel_url': cancel_url, 'book_title': self.book.title, 'price': price})
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        book = self.book
        price = self.get_discounted_price()
        logger = logging.getLogger(__name__)
        try:
            with transaction.atomic():
                user = user.__class__.objects.select_for_update().get(pk=user.pk)
                if user.profile.balance < price:
                    messages.error(self.request, "Insufficient balance to buy this book.")
                    return redirect('/')
                user.profile.balance -= price
                user.save()

                Purchase.objects.create(user=user, book=book, price=price)
                self.request.session.pop('discount_code', None)
                messages.success(self.request, f"You have successfully purchased '{book.title}'.")
                return super().form_valid(form)

        except Exception as e:
            logger.error("Purchase error: %s", e, exc_info=True)
            messages.error(self.request, "An error occurred during purchase. Please try again.")
            return redirect('/')

    def get_discount_percentage(self, discount_code):
        if not discount_code:
            return None
        try:
            return Discount.objects.get(discount_code=discount_code).percentage
        except Discount.DoesNotExist:
            return None

    def get_discounted_price(self):
        if self.percentage:
            discount_multiplier = Decimal('1') - (Decimal(str(self.percentage)) / Decimal('100'))
            return self.book.price * discount_multiplier
        return self.book.price


class ForgotPasswordFormView(FormView):
    template_name = 'app/forgotpass.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy("confirm_code")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_name = form.cleaned_data['user_name']
        phone_number = form.cleaned_data['phone_number']
        if phone_number:
            try:
                user = User.objects.get(profile__phone_number=phone_number)
            except User.DoesNotExist:
                user = None

        if user_name and not phone_number:
            try:
                user = User.objects.get(username=user_name)
            except User.DoesNotExist:
                user = None
                return self.form_invalid(form)

        code = f"{random.randint(100000, 999999)}"
        expires_at = timezone.now() + datetime.timedelta(minutes=2)

        PasswordResetCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'expires_at': expires_at, 'created_at': timezone.now()}
        )

        # Send SMS with code
        try:
            send_sms(user.profile.phone_number, code)
        except Exception as e:
            form.add_error(None, f"Failed to send SMS: {e}")
            return self.form_invalid(form)

        # Save user id in session for next steps
        self.request.session['password_reset_user_id'] = user.id
        messages.success(self.request, "Verification code sent to your phone.")
        return super().form_valid(form)


class ConfirmCodeFormView(FormView):
    template_name = 'app/resetepasswordpage.html'
    form_class = ConfirmCodeForm
    success_url = reverse_lazy("resetpassword")

    def dispatch(self, request, *args, **kwargs):
        if 'password_reset_user_id' not in request.session:
            messages.error(request, "Please start password reset process first.")
            return redirect('forgotpassword')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        formcode = form.cleaned_data['code']
        user_id = self.request.session.get("password_reset_user_id")

        try:
            reset_request = PasswordResetCode.objects.get(user=user_id)
        except PasswordResetCode.DoesNotExist:
            messages.error(self.request, "No reset request found. Please start again.")
            return redirect('forgotpassword')
        code = reset_request.code
        if reset_request.is_expired():
            form.add_error('code', "Verification code expired. Please request a new one.")
            return self.form_invalid(form)
        if formcode != code:
            form.add_error('code', "code is incorrect")
            return self.form_invalid(form)

        self.request.session['password_reset_verified'] = True
        messages.success(self.request, "Code verified. You can now reset your password.")
        return super().form_valid(form)


class ResetPasswordFormView(FormView):
    template_name = 'app/resetepasswordpage.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('password_reset_verified'):
            messages.error(request, "You must verify your phone code first.")
            return redirect('forgotpassword')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session.get('password_reset_user_id')
        user = get_object_or_404(User, id=user_id)
        kwargs['user'] = user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Clean up session
        self.request.session.pop('password_reset_user_id', None)
        self.request.session.pop('password_reset_verified', None)
        messages.success(self.request, "Your password has been reset successfully.")
        return super().form_valid(form)


class SmsLoginView(FormView):
    template_name = 'app/smslogin.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy("smsloginconfirm")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user_name = form.cleaned_data['user_name']
        phone_number = form.cleaned_data['phone_number']
        if phone_number:
            try:
                user = User.objects.get(profile__phone_number=phone_number)
            except User.DoesNotExist:
                user = None

        if user_name and not phone_number:
            try:
                user = User.objects.get(username=user_name)
            except User.DoesNotExist:
                user = None
                return self.form_invalid(form)

        code = f"{random.randint(100000, 999999)}"
        expires_at = timezone.now() + datetime.timedelta(minutes=2)

        PasswordResetCode.objects.update_or_create(
            user=user,
            defaults={'code': code, 'expires_at': expires_at, 'created_at': timezone.now()}
        )

        # Send SMS with code
        try:
            send_sms(user.profile.phone_number, code)
        except Exception as e:
            form.add_error(None, f"Failed to send SMS: {e}")
            return self.form_invalid(form)

        # Save user id in session for next steps
        self.request.session['smslogin_user_id'] = user.id
        messages.success(self.request, "Verification code sent to your phone.")
        return super().form_valid(form)


class SmsLoginConfirmCodeFormView(LoginView):
    template_name = 'app/resetepasswordpage.html'
    form_class = SmsConfirmCodeForm
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session.get('smslogin_user_id')
        user = None
        if user_id:
            user = User.objects.get(id=user_id)
        kwargs['user'] = user
        kwargs['request'] = self.request  # optional
        return kwargs

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('/')
        if 'smslogin_user_id' not in request.session:
            messages.error(request, "Please relogin")
            return redirect('smslogin')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        formcode = form.cleaned_data['code']
        user_id = self.request.session.get("smslogin_user_id")

        try:
            login_request = PasswordResetCode.objects.get(user=user_id)
        except PasswordResetCode.DoesNotExist:
            messages.error(self.request, "No login request found. Please start again.")
            return redirect('smslogin')
        code = login_request.code
        if login_request.is_expired():
            form.add_error('code', "Verification code expired. Please request a new one.")
            return self.form_invalid(form)
        if formcode != code:
            form.add_error('code', "code is incorrect")
            return self.form_invalid(form)
        user = User.objects.get(id=self.request.session['smslogin_user_id'])
        login(self.request, user)
        self.request.session.pop("smslogin_user_id", None)
        messages.success(self.request, "Code verified.")
        return super().form_valid(form)


class Login2FAView(LoginView):
    template_name = 'app/logn2fa.html'
    success_url = 'login2faconfirm'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        code = otp_code_generator()
        expiry_time = timezone.now() + datetime.timedelta(minutes=2)
        user = form.get_user()
        if user:
            try:
                send_sms(user.profile.phone_number, code)
            except Exception as e:
                form.add_error(None, f"Failed to send SMS: {e}")
                return self.form_invalid(form)
            self.request.session['2falogin_user_id'] = user.id
            self.request.session['2fa_code'] = code
            self.request.session['2fa_expiry'] = expiry_time.isoformat()
            return redirect("login2faconfirm")
        return super().form_valid(form)


class Login2FAConfirmView(FormView):
    template_name = 'app/login2faconfirmpage.html'
    form_class = SmsConfirmCodeForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session.get('2falogin_user_id')
        user = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = None
        kwargs['user'] = user
        kwargs['request'] = self.request  # optional
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if '2falogin_user_id' not in request.session:
            return redirect('/')
        if '2fa_code' not in request.session:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        formcode = str(form.cleaned_data['code']).strip()
        user_id = self.request.session.get("2falogin_user_id")
        code = str(self.request.session.get("2fa_code")).strip()
        expiry_str = self.request.session.get("2fa_expiry")
        expiry = timezone.datetime.fromisoformat(expiry_str)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(self.request, "User not found. Please login again.")
            return redirect(reverse_lazy('login2fa'))
        if timezone.now() > expiry:
            messages.error(self.request, "token is expired, please relogin")
            self.request.session.pop("2falogin_user_id", None)
            self.request.session.pop("2fa_code", None)
            self.request.session.pop("2fa_expiry", None)
            return redirect('login2fa')
        if formcode != code:
            form.add_error('code', "code is incorrect")
            print(f"Session code: {code}, Entered code: {formcode}")
            return self.form_invalid(form)
        print(f"Session code: {code}, Entered code: {formcode}")
        login(self.request, user)
        self.request.session.pop("2falogin_user_id", None)
        self.request.session.pop("2fa_code", None)
        self.request.session.pop("2fa_expiry", None)
        messages.success(self.request, "Code verified.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        countdowntime = self.request.session.get("2fa_expiry")
        context["time"] = countdowntime
        return context


class Library2FALoginView(TwoFactorLoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class TestView(UserPassesTestMixin, FormView):
    template_name = 'app/test.html'
    form_class = TestForm

    def test_func(self):
        if not self.request.user.is_superuser:
            messages.error(self.request, 'Please login as superuser')
        return self.request.user.is_superuser


class PurchaseView(LoginRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    model = Purchase
    table_class = PurchaseTable
    template_name = "app/purchaselist.html"
    filterset_class = PurchaseFilter

    def get_queryset(self, *args, **kwargs):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        if "Operator" in user_groups:
            return Purchase.objects.filter(user__username=self.request.user.username)
        return Purchase.objects.all()


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'app/userprofile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse("userprofile", kwargs={"pk": self.object.id})

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.id != self.kwargs.get('pk'):
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class ContactusFormView(FormView):
    template_name = 'app/contactus.html'
    form_class = ContactusForm
    success_url = reverse_lazy('contactus')

    def form_valid(self, form):
        message = form.cleaned_data['message']
        author_name = form.cleaned_data['author_name']

        subject = f"Contact Us - {author_name}"
        email = EmailMessage(
            subject=subject,
            body=message,
            to=["admin@test.ir"]
        )
        email.send(fail_silently=False)
        messages.success(self.request, f"Email sent successfully")
        return super().form_valid(form)
