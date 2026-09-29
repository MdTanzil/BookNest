from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'quantity', 'total']
    fields = ['book', 'price', 'quantity', 'total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # CRITICAL UI FIX: Re-arranged column placements for a professional layout alignment
    list_display = [
        'order_number', 
        'user', 
        'shipping_name',
        'total', 
        
        # 1. Group the editable dropdowns together cleanly in the center-right
        'status', 
        'payment_status', 
        'created_at'
    ]
    
    list_filter = [
        'status', 'payment_status', 'payment_method', 'created_at'
    ]
    search_fields = [
        'order_number', 'shipping_name',
        'shipping_phone', 'user__email'
    ]
    
    # Matches the list fields perfectly
    list_editable = ['status', 'payment_status']
    
    readonly_fields = [
        'order_number', 'subtotal', 'shipping_cost',
        'discount', 'total', 'created_at', 'updated_at'
    ]
    inlines = [OrderItemInline]
    

    # --- 1. Renders the Label Button inside the Main Admin Grid ---
    def print_label_button(self, obj):
        """Generates an action link column straight inside the main datagrid rows table listing."""
        url = reverse('admin:print_delivery_label_action', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank" style="background-color: #264b5d; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 11px; text-decoration: none; display: inline-block;">📦 Label</a>', 
            url
        )
    print_label_button.short_description = 'Courier'

    # --- 2. Renders the Receipt Button inside the Main Admin Grid ---
    def print_receipt_button(self, obj):
        """Generates a separate receipt link column inside the main list rows log table."""
        url = reverse('admin:print_customer_receipt_action', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank" style="background-color: #79aec8; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 11px; text-decoration: none; display: inline-block;">📄 Receipt</a>', 
            url
        )
    print_receipt_button.short_description = 'Customer'

    # --- 3. Inject Buttons Context Into the Upper Action Ribbon on the Order Details Page ---
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        order = self.get_object(request, object_id)
        if order:
            extra_context['show_print_label_button'] = True
            extra_context['print_label_url'] = reverse('orders:print_delivery_label', args=[order.order_number])
            # Added receipt template injection parameters
            extra_context['print_receipt_url'] = reverse('orders:print_customer_receipt', args=[order.order_number])
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    # --- 4. Custom Admin URL Catchment to Prevent Apps Namespace Clashes ---
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/print-label-action/', self.admin_site.admin_view(self.admin_print_label_redirect), name='print_delivery_label_action'),
            path('<int:object_id>/print-receipt-action/', self.admin_site.admin_view(self.admin_print_receipt_redirect), name='print_customer_receipt_action'),
        ]
        return custom_urls + urls

    def admin_print_label_redirect(self, request, object_id):
        order = self.get_object(request, object_id)
        return redirect('orders:print_delivery_label', order_number=order.order_number)

    def admin_print_receipt_redirect(self, request, object_id):
        order = self.get_object(request, object_id)
        return redirect('orders:print_customer_receipt', order_number=order.order_number)

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