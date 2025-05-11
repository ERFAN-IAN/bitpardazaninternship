from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    TemplateView,
    FormView
)
from .forms import UserSignupForm, BookForm, BookFormSingleNoAjax, BookFormSingleAjax, BookSelectForm, \
    ForgotPasswordForm, ConfirmCodeForm, SmsConfirmCodeForm
from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Author, Book, BookCategory, UserProfile, Purchase, PasswordResetCode
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect
from django_tables2 import SingleTableView
from .tables import AuthorBooksTable, AuthorTable, AuthorBookCountTable
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from django_tables2.views import MultiTableMixin
from .filters import AuthorFilter, BookFilter
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
from .utility import send_sms
from django.contrib.auth import login

# from django.views.generic.detail import SingleObjectMixin
# from braces.views import SuperuserRequiredMixin
# from django.contrib.auth.decorators import user_passes_test
# from django.utils.decorators import method_decorator
# from chartjs.views.pie import HighChartPieView
# from django.http import JsonResponse
# from django.db.models import Sum
# from slick_reporting.views import ReportView, Chart
# from slick_reporting.fields import ComputationField
# from .reports import AuthorBookReport
# from django.shortcuts import render

# Create your views here.


class AuthorListView(FilterView, ExportMixin, SingleTableView):
    model = Author
    template_name = "app/home.html"
    table_class = AuthorTable
    context_object_name = "authors"
    filterset_class = AuthorFilter

    def get_queryset(self):
        query = self.request.GET.get("q")
        print(query)
        if query:
            return Author.objects.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(national_id__icontains=query)
            )
        return Author.objects.all()


class AuthorCreateView(GroupRequiredMixin, CreateView):
    model = Author
    fields = ["first_name", "last_name", "age", "national_id"]

    template_name = "app/add_author_form.html"
    group_required = ['Operator', 'Moderator', 'Admin']

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.id})


class AuthorUpdateView(GroupRequiredMixin, UpdateView):
    model = Author
    fields = ["first_name", "last_name", "age", "national_id"]
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


class AuthorDetailView(DetailView):
    model = Author
    template_name = "app/author_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_query = self.request.GET.get("q")
        books = self.object.books.all()
        if book_query:
            books = books.filter(title__icontains=book_query)
        book_table = AuthorBooksTable(books)
        context["book_table"] = book_table
        return context


class BookCreateView(GroupRequiredMixin, CreateView):
    model = Book
    # fields = ["title", "release_date", "image", "category"]
    template_name = "app/add_book_form.html"
    group_required = ['Operator', 'Moderator', 'Admin']
    form_class = BookFormSingleAjax

    def form_valid(self, form):
        form.instance.author = get_object_or_404(Author, id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.kwargs["pk"]})


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


# class AuthorSlickView(TemplateView):
#     template_name = "app/authorslick.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = None
#         return context


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


import logging


class BookPurchaseView(LoginRequiredMixin, FormView):
    template_name = "app/purchaseconfirmation.html"
    success_url = '/'
    form_class = forms.Form

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context

    def form_valid(self, form):
        user = self.request.user
        book = self.book
        logger = logging.getLogger(__name__)
        try:
            with transaction.atomic():
                user = user.__class__.objects.select_for_update().get(pk=user.pk)

                if user.profile.balance < book.price:
                    messages.error(self.request, "Insufficient balance to buy this book.")
                    return redirect('/')
                user.profile.balance -= book.price
                user.save()

                Purchase.objects.create(user=user, book=book, price=book.price)

                messages.success(self.request, f"You have successfully purchased '{book.title}'.")
                return super().form_valid(form)

        except Exception as e:
            logger.error("Purchase error: %s", e, exc_info=True)
            messages.error(self.request, "An error occurred during purchase. Please try again.")
            return redirect('/')


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
