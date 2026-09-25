from django.db import models
from django.conf import settings


class Cart(models.Model):
    session_key = models.CharField(max_length=50, unique=True, blank=True, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.user:
            return f'Cart #{self.id} - {self.user.email}'
        return f'Cart #{self.id}'

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def get_subtotal(self):
        return sum(item.quantity * item.book.final_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='cart_items',
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['cart', 'book']]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.quantity}x {self.book.title}'

    @property
    def subtotal(self):
        return self.quantity * self.book.final_price
