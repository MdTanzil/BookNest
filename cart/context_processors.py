from cart.cart import Cart


def cart_counter(request):
    cart = Cart(request)
    return {'cart_count': cart.get_total_items()}
