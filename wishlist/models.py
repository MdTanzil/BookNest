from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'book']]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.book.title}"
