from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from books.models import Book
from cart.cart import Cart


@require_POST
def cart_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.add(book_id, quantity, update_quantity=bool(request.POST.get('update', False)))
    messages.success(request, f"Added {book.title} to cart.")
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    cart.remove(book_id)
    messages.info(request, "Item removed from cart.")
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, book_id):
    quantity = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.update_quantity(book_id, quantity)
    messages.success(request, "Cart quantity updated.")
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_items = cart.get_items()
    subtotal = cart.get_subtotal()
    shipping = cart.get_shipping_cost()
    total = cart.get_total()
    free_threshold = Decimal(str(getattr(settings, 'FREE_SHIPPING_THRESHOLD', Decimal('50.00'))))
    shipping_saving = free_threshold - subtotal if subtotal < free_threshold else Decimal('0.00')
    featured_books = Book.objects.filter(featured=True).select_related('author')[:4]
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'free_shipping_threshold': free_threshold,
        'shipping_saving': shipping_saving,
        'featured_books': featured_books,
    })


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "All items removed from cart.")
    return redirect('cart:cart_detail')
