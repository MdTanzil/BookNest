import random
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory
import factory
from books.models import Category, Author, Book, BookImage

# A simple 1x1 pixel dummy image string to keep ImageFields completely functional
DUMMY_IMAGE = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'

# Get the base faker instance to extract words inline safely inside lambdas
faker_instance = factory.Faker._get_faker()

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    # Appends the sequence index cleanly ensuring structural uniqueness for your unique slugs
    name = factory.Sequence(lambda n: f" {faker_instance.word().capitalize()} {n}")
    description = factory.Faker('paragraph', nb_sentences=2)
    image = factory.LazyAttribute(lambda _: ContentFile(DUMMY_IMAGE, name='cat_dummy.gif'))

class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f"{faker_instance.name()} {n}")
    biography = factory.Faker('paragraph', nb_sentences=4)
    photo = factory.LazyAttribute(lambda _: ContentFile(DUMMY_IMAGE, name='author_dummy.gif'))

class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f"The {faker_instance.word().capitalize()}  {n}")
    description = factory.Faker('text', max_nb_chars=600)
    
    # Generate exactly 13 digits for the unique ISBN requirement
    isbn = factory.Sequence(lambda n: f"{1000000000000 + n}") 
    
    publisher = factory.Faker('company')
    publication_date = factory.Faker('date_between', start_date='-10y', end_date='today')
    pages = factory.LazyAttribute(lambda _: random.randint(120, 950))
    language = factory.Iterator(['English', 'Spanish', 'French', 'Bengali'])
    format = factory.Iterator(['Hardcover', 'Paperback', 'Ebook', 'Audiobook'])
    
    price = factory.LazyAttribute(lambda _: round(random.uniform(15.00, 120.00), 2))
    discount_price = factory.LazyAttribute(lambda o: round(o.price * random.uniform(0.70, 0.90), 2) if random.choice([True, False]) else None)
    
    stock = factory.LazyAttribute(lambda _: random.randint(0, 50))
    cover_image = factory.LazyAttribute(lambda _: ContentFile(DUMMY_IMAGE, name='cover_dummy.gif'))
    
    featured = factory.Faker('boolean', chance_of_getting_true=25)
    bestseller = factory.Faker('boolean', chance_of_getting_true=15)
    new_arrival = factory.Faker('boolean', chance_of_getting_true=40)
    average_rating = factory.LazyAttribute(lambda _: round(random.uniform(3.00, 5.00), 2))

class BookImageFactory(DjangoModelFactory):
    class Meta:
        model = BookImage

    image = factory.LazyAttribute(lambda _: ContentFile(DUMMY_IMAGE, name='gallery_dummy.gif'))
    alt_text = factory.Faker('sentence', nb_words=4)


class Command(BaseCommand):
    help = "Seeds the database dynamically with highly comprehensive, clean dummy data for your Books App."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=15,
            help='The total count of items to seed per model'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write(self.style.WARNING("Flushing existing book database entries..."))
        BookImage.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(f"Generating {count} Categories...")
        categories = [CategoryFactory() for _ in range(count)]

        self.stdout.write(f"Generating {count} Authors...")
        authors = [AuthorFactory() for _ in range(count)]

        self.stdout.write(f"Generating {count} Books and setting up relationships...")
        books = []
        for i in range(count):
            book = BookFactory(
                author=random.choice(authors),
                category=random.choice(categories)
            )
            books.append(book)

        self.stdout.write(f"Generating multi-gallery images for each book...")
        for book in books:
            for _ in range(random.randint(1, 3)):
                BookImageFactory(book=book)

        self.stdout.write(self.style.SUCCESS(f"Successfully populated all tables with {count} unique data records! 🎉"))
