from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from books.models import Book
from wishlist.models import Wishlist
from cart.cart import Cart


def wishlist_add(request, book_id):
    if request.user.is_authenticated:
        Wishlist.objects.get_or_create(user=request.user, book_id=book_id)
        book = Book.objects.filter(id=book_id).first()
        if book:
            messages.success(request, f"Added {book.title} to wishlist.")
        else:
            messages.success(request, "Added to wishlist.")
    else:
        messages.warning(request, "Please login to add items to your wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist_list'))


@login_required
def wishlist_remove(request, book_id):
    Wishlist.objects.filter(user=request.user, book_id=book_id).delete()
    messages.info(request, "Item removed from wishlist.")
    return redirect('wishlist:wishlist_list')


@login_required
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('book__author', 'book__category')
    return render(request, 'wishlist/wishlist_list.html', {
        'wishlist_items': wishlist_items,
    })


@login_required
def wishlist_move_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Wishlist.objects.filter(user=request.user, book_id=book_id).delete()
    cart = Cart(request)
    cart.add(book_id, 1)
    messages.success(request, f"Moved {book.title} to cart.")
    return redirect('cart:cart_detail')
