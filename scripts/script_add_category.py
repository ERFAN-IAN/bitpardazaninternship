from app.models import BookCategory
def run():
	BookCategory.objects.create(title="Art")
	BookCategory.objects.create(title="History")
	BookCategory.objects.create(title="Thriller")


