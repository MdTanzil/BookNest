from django.contrib import admin

from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'book__title']
