from decimal import Decimal
from django.conf import settings
from books.models import Book
from cart.models import Cart as CartModel, CartItem


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.user = getattr(request, 'user', None)
        self.cart_db = None
        self.cart_session = None

        if self.user and self.user.is_authenticated:
            self.cart_db, _ = CartModel.objects.get_or_create(user=self.user)
        else:
            cart_session_id = getattr(settings, 'CART_SESSION_ID', 'cart')
            self.cart_session = self.session.get(cart_session_id)
            if self.cart_session is None:
                self.cart_session = {}
                self.session[cart_session_id] = self.cart_session
                self.save()

    def add(self, book_id, quantity=1, update_quantity=False):
        book = Book.objects.get(id=book_id)
        max_qty = book.stock

        if self.cart_db is not None:
            cart_item, created = CartItem.objects.get_or_create(
                cart=self.cart_db,
                book=book,
                defaults={'quantity': 0}
            )
            if update_quantity:
                cart_item.quantity = min(quantity, max_qty)
            else:
                cart_item.quantity = min(cart_item.quantity + quantity, max_qty)
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        else:
            book_id_str = str(book_id)
            current_qty = int(self.cart_session.get(book_id_str, 0))
            if update_quantity:
                new_qty = min(quantity, max_qty)
            else:
                new_qty = min(current_qty + quantity, max_qty)
            if new_qty <= 0:
                if book_id_str in self.cart_session:
                    del self.cart_session[book_id_str]
            else:
                self.cart_session[book_id_str] = new_qty
            self.save()

    def remove(self, book_id):
        if self.cart_db is not None:
            CartItem.objects.filter(cart=self.cart_db, book_id=book_id).delete()
        else:
            book_id_str = str(book_id)
            if book_id_str in self.cart_session:
                del self.cart_session[book_id_str]
                self.save()

    def update_quantity(self, book_id, quantity):
        book = Book.objects.get(id=book_id)
        if quantity <= 0:
            self.remove(book_id)
            return
        quantity = min(quantity, book.stock)
        self.add(book_id, quantity=quantity, update_quantity=True)

    def get_items(self):
        items = []
        if self.cart_db is not None:
            for cart_item in self.cart_db.items.all().select_related('book'):
                book = cart_item.book
                items.append({
                    'book': book,
                    'book_id': book.id,
                    'title': book.title,
                    'quantity': cart_item.quantity,
                    'price': book.final_price,
                    'subtotal': cart_item.quantity * book.final_price,
                    'cover_image': book.cover_image,
                })
        else:
            book_ids = [int(bid) for bid in self.cart_session.keys()]
            books_map = {}
            if book_ids:
                for book in Book.objects.filter(id__in=book_ids):
                    books_map[book.id] = book
            for book_id_str, qty in self.cart_session.items():
                book_id = int(book_id_str)
                book = books_map.get(book_id)
                if book:
                    quantity = int(qty)
                    items.append({
                        'book': book,
                        'book_id': book.id,
                        'title': book.title,
                        'quantity': quantity,
                        'price': book.final_price,
                        'subtotal': quantity * book.final_price,
                        'cover_image': book.cover_image,
                    })
        return items

    def get_subtotal(self):
        subtotal = Decimal('0.00')
        if self.cart_db is not None:
            for item in self.cart_db.items.all().select_related('book'):
                subtotal += item.quantity * item.book.final_price
        else:
            items = self.get_items()
            for item in items:
                subtotal += item['subtotal']
        return subtotal

    def get_shipping_cost(self):
        shipping_cost = getattr(settings, 'SHIPPING_COST', Decimal('0.00'))
        free_threshold = getattr(settings, 'FREE_SHIPPING_THRESHOLD', Decimal('0.00'))
        subtotal = self.get_subtotal()
        if subtotal >= free_threshold:
            return Decimal('0.00')
        return Decimal(str(shipping_cost))

    def get_total(self):
        return self.get_subtotal() + self.get_shipping_cost()

    def get_total_items(self):
        if self.cart_db is not None:
            return sum(item.quantity for item in self.cart_db.items.all())
        return sum(int(qty) for qty in self.cart_session.values())

    def clear(self):
        if self.cart_db is not None:
            self.cart_db.items.all().delete()
        else:
            cart_session_id = getattr(settings, 'CART_SESSION_ID', 'cart')
            self.cart_session = {}
            self.session[cart_session_id] = self.cart_session
            self.save()

    def save(self):
        if self.cart_db is None:
            self.session.modified = True
