from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'book']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'book']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.user} rated {self.book} {self.rating}/5"


def _update_book_average_rating(book):
    from books.models import Book

    avg = book.reviews.aggregate(
        avg_rating=models.Avg('rating')
    )['avg_rating'] or 0
    book.average_rating = round(avg, 2)
    book.save(update_fields=['average_rating'])


@receiver(post_save, sender=Review)
def update_average_rating_on_save(sender, instance, **kwargs):
    _update_book_average_rating(instance.book)


@receiver(post_delete, sender=Review)
def update_average_rating_on_delete(sender, instance, **kwargs):
    _update_book_average_rating(instance.book)
