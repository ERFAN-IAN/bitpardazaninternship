from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


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

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    father_name = models.CharField(max_length=150, null=True, blank=True, default=None)

    def __str__(self):
        return f"Profile of {self.user.username}"
