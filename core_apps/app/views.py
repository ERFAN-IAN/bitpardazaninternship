from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy, reverse
from .models import Author, Book
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

# Create your views here.


class AuthorListView(ListView):
    model = Author
    template_name = "app/home.html"
    context_object_name = "authors"

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


class AuthorCreateView(CreateView):
    model = Author
    fields = ["first_name", "last_name", "age", "national_id"]

    template_name = "app/add_author_form.html"

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.id})


class AuthorUpdateView(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "age", "national_id"]
    context_object_name = "author"
    template_name = "app/edit_author_form.html"

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.id})


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = "app/delete_author.html"
    success_url = reverse_lazy("home")


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
        context["books"] = books
        return context


class BookCreateView(CreateView):
    model = Book
    fields = ["title", "publication_year"]
    template_name = "app/add_book_form.html"

    def form_valid(self, form):
        form.instance.author = get_object_or_404(Author, id=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.kwargs["pk"]})


class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", "publication_year", "author"]
    template_name = "app/edit_book_form.html"

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.author.id})


class BookDeleteView(DeleteView):
    model = Book
    template_name = "app/delete_book.html"
    context_object_name = "book"

    def get_success_url(self):
        return reverse("author_detail", kwargs={"pk": self.object.author.id})
