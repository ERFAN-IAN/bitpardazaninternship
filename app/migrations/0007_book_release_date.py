# Generated by Django 4.2.5 on 2025-05-07 12:56

from django.db import migrations, models
import django.utils.timezone
import datetime


def set_release_date(apps, schema_editor):
    Book = apps.get_model('app', 'Book')
    books = Book.objects.all()
    for bk in books:
        try:
            bk.release_date = datetime.datetime(int(bk.publication_year), 1, 1)
            bk.save()
        except:
            continue

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='release_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.RunPython(set_release_date)
    ]
