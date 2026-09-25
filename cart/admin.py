from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['book', 'quantity']
    readonly_fields = []


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'session_key',
        'get_total_items', 'get_subtotal', 'updated_at'
    ]
    list_filter = ['updated_at', 'created_at']
    search_fields = ['user__email', 'session_key']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at']
