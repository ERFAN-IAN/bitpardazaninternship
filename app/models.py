from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.
def validate_publication_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f"Publication year can't be in the future (max {current_year})."
        )


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(199)])
    national_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField(
        validators=[validate_publication_year]
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    category = models.ForeignKey(BookCategory, on_delete=models.PROTECT, related_name='category')
    image = models.ImageField(upload_to="books/", null=True, blank=True)
    release_date = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=12)

    def save(self, *args, **kwargs):
        if self.release_date:
            self.publication_year = self.release_date.year
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    father_name = models.CharField(max_length=150, null=True, blank=True, default=None)
    balance = models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Purchase(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='purchase')
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="purchase")
    price = models.DecimalField(decimal_places=2, max_digits=12)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.book.title} for {self.price}"
