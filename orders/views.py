from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.core.paginator import Paginator
from cart.cart import Cart
from cart.models import Cart as CartModel
from .forms import CheckoutForm
from .models import Order, OrderItem
from books.models import Book
from django.conf import settings
import uuid
import string
import random


def generate_order_number():
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'BN-{timestamp}-{rand}'


def checkout_view(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('/books/')
    initial = {}
    if request.user.is_authenticated:
        initial = {
            'shipping_name': request.user.get_full_name() or '',
            'shipping_phone': request.user.phone or '',
            'shipping_address': request.user.address or '',
            'shipping_city': request.user.city or '',
            'shipping_postcode': request.user.postcode or '',
        }
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                subtotal = cart.get_subtotal()
                shipping_cost = cart.get_shipping_cost()
                total = cart.get_total()
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    order_number=generate_order_number(),
                    status='Pending',
                    subtotal=subtotal,
                    shipping_cost=shipping_cost,
                    discount=0.00,
                    total=total,
                    payment_method=form.cleaned_data['payment_method'],
                    payment_status='Pending',
                    shipping_name=form.cleaned_data['shipping_name'],
                    shipping_phone=form.cleaned_data['shipping_phone'],
                    shipping_address=form.cleaned_data['shipping_address'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_postcode=form.cleaned_data['shipping_postcode'],
                )
                for item in cart_items:
                    book = item['book']
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=item['quantity'],
                        price=book.final_price,
                    )
                    book.stock = max(0, book.stock - item['quantity'])
                    book.save(update_fields=['stock'])
                cart.clear()
                messages.success(request, "Order placed successfully!")
                return redirect('orders:order_success', order_number=order.order_number)
    else:
        form = CheckoutForm(initial=initial)
    free_shipping_threshold = getattr(settings, 'FREE_SHIPPING_THRESHOLD', 50)
    subtotal_val = cart.get_subtotal()
    from decimal import Decimal
    remaining_for_free_shipping = max(Decimal('0.00'), Decimal(str(free_shipping_threshold)) - subtotal_val)
    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal_val,
        'shipping_cost': cart.get_shipping_cost(),
        'total': cart.get_total(),
        'free_shipping_threshold': free_shipping_threshold,
        'remaining_for_free_shipping': remaining_for_free_shipping,
    }
    return render(request, 'orders/checkout.html', context)


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    items = order.items.select_related('book')
    is_cod = order.payment_method == 'Cash on Delivery'
    context = {
        'order': order,
        'items': items,
        'is_cod': is_cod,
    }
    return render(request, 'orders/order_success.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    items = order.items.select_related('book')
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/order_detail.html', context)
