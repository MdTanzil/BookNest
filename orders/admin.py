from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'quantity', 'total']
    fields = ['book', 'price', 'quantity', 'total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'shipping_name',
        'total', 'status', 'payment_status', 'created_at'
    ]
    list_filter = [
        'status', 'payment_status', 'payment_method', 'created_at'
    ]
    search_fields = [
        'order_number', 'shipping_name',
        'shipping_phone', 'user__email'
    ]
    list_editable = ['status', 'payment_status']
    readonly_fields = [
        'order_number', 'subtotal', 'shipping_cost',
        'discount', 'total', 'created_at', 'updated_at'
    ]
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Info', {
            'fields': (
                'order_number', 'user', 'status',
                'created_at', 'updated_at'
            )
        }),
        ('Shipping', {
            'fields': (
                'shipping_name', 'shipping_phone',
                'shipping_address', 'shipping_city', 'shipping_postcode'
            )
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status')
        }),
        ('Financial Totals', {
            'fields': ('subtotal', 'shipping_cost', 'discount', 'total')
        }),
    )
