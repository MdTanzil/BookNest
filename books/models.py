from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Book(models.Model):
    FORMAT_CHOICES = [
        ('Hardcover', 'Hardcover'),
        ('Paperback', 'Paperback'),
        ('Ebook', 'Ebook'),
        ('Audiobook', 'Audiobook'),
    ]

    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    description = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateField()
    pages = models.PositiveIntegerField()
    language = models.CharField(max_length=50, default='English')
    format = models.CharField(max_length=50, default='Hardcover', choices=FORMAT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to='books/covers/', blank=True)
    featured = models.BooleanField(default=False)
    bestseller = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['title']),
            models.Index(fields=['price']),
            models.Index(fields=['bestseller']),
            models.Index(fields=['featured']),
            models.Index(fields=['new_arrival']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        return self.stock > 0

    @property
    def discount_percent(self):
        if self.discount_price:
            return round((self.price - self.discount_price) / self.price * 100)
        return None

    @property
    def final_price(self):
        return self.discount_price or self.price

    @property
    def is_on_sale(self):
        return self.discount_price is not None


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='books/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.book.title}"
