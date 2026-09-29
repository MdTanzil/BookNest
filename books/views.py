from django.db.models import Q, Avg, Count, Case, When, F, DecimalField, Value, FloatField, Min, Max
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book, Category, Author
from reviews.forms import ReviewForm
from wishlist.models import Wishlist


class BookListView(ListView):
    model = Book
    paginate_by = 12
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    filter = None

    def get_queryset(self):
        qs = Book.objects.select_related('author', 'category').prefetch_related('images', 'reviews')

        qs = qs.annotate(
            calculated_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )

        qs = qs.annotate(
            review_count=Count('reviews', distinct=True)
        )

        filter_arg = self.filter
        if filter_arg == 'bestsellers':
            qs = qs.filter(bestseller=True)
        elif filter_arg == 'new':
            qs = qs.filter(new_arrival=True)
        elif filter_arg == 'featured':
            qs = qs.filter(featured=True)

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(author__name__icontains=q) |
                Q(isbn__icontains=q) |
                Q(category__name__icontains=q)
            )

        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)

        author = self.request.GET.get('author')
        if author:
            qs = qs.filter(author__slug=author)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                qs = qs.filter(final_price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        if max_price:
            try:
                qs = qs.filter(final_price__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        rating = self.request.GET.get('rating')
        if rating:
            try:
                qs = qs.filter(average_rating__gte=float(rating))
            except (ValueError, TypeError):
                pass

        available = self.request.GET.get('available')
        if available == '1':
            qs = qs.filter(stock__gt=0)

        sort = self.request.GET.get('sort')
        if sort == 'popularity':
            qs = qs.order_by('-review_count', '-average_rating')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'price-asc':
            qs = qs.order_by('final_price')
        elif sort == 'price-desc':
            qs = qs.order_by('-final_price')
        elif sort == 'rating':
            qs = qs.order_by('-average_rating')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        context['all_authors'] = Author.objects.all()

        all_prices = Book.objects.annotate(
            fp=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ).aggregate(
            min_p=Min('fp'),
            max_p=Max('fp'),
        )
        context['price_min'] = all_prices['min_p'] or 0
        context['price_max'] = all_prices['max_p'] or 0

        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'category': self.request.GET.getlist('category'),
            'author': self.request.GET.get('author', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'rating': self.request.GET.get('rating', ''),
            'available': self.request.GET.get('available', ''),
        }
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', '')

        if self.filter:
            context['filter_type'] = self.filter

        return context


class BookDetailView(DetailView):
    model = Book
    slug_field = 'slug'
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.select_related('author', 'category').prefetch_related('images', 'reviews__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        context['related_books'] = Book.objects.filter(
            category=book.category
        ).exclude(
            pk=book.pk
        ).select_related('author')[:8]

        context['review_form'] = ReviewForm()

        if self.request.user.is_authenticated:
            context['user_review'] = book.reviews.filter(user=self.request.user).first()
            context['in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user,
                book=book
            ).exists()
        else:
            context['user_review'] = None
            context['in_wishlist'] = False

        return context


class CategoryBooksView(ListView):
    model = Book
    paginate_by = 12
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        qs = Book.objects.select_related('author', 'category').prefetch_related('images', 'reviews')
        qs = qs.filter(category=self.category)

        qs = qs.annotate(
            final_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        qs = qs.annotate(review_count=Count('reviews', distinct=True))

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(author__name__icontains=q) |
                Q(isbn__icontains=q)
            )

        author = self.request.GET.get('author')
        if author:
            qs = qs.filter(author__slug=author)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                qs = qs.filter(final_price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        if max_price:
            try:
                qs = qs.filter(final_price__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        rating = self.request.GET.get('rating')
        if rating:
            try:
                qs = qs.filter(average_rating__gte=float(rating))
            except (ValueError, TypeError):
                pass

        available = self.request.GET.get('available')
        if available == '1':
            qs = qs.filter(stock__gt=0)

        sort = self.request.GET.get('sort')
        if sort == 'popularity':
            qs = qs.order_by('-review_count', '-average_rating')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'price-asc':
            qs = qs.order_by('final_price')
        elif sort == 'price-desc':
            qs = qs.order_by('-final_price')
        elif sort == 'rating':
            qs = qs.order_by('-average_rating')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['all_categories'] = Category.objects.all()
        context['all_authors'] = Author.objects.all()

        cat_books = Book.objects.filter(category=self.category).annotate(
            fp=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ).aggregate(min_p=Min('fp'), max_p=Max('fp'))
        context['price_min'] = cat_books['min_p'] or 0
        context['price_max'] = cat_books['max_p'] or 0

        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'category': [self.category.slug],
            'author': self.request.GET.get('author', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'rating': self.request.GET.get('rating', ''),
            'available': self.request.GET.get('available', ''),
        }
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', '')

        return context


class AuthorBooksView(ListView):
    model = Book
    paginate_by = 12
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        self.author = get_object_or_404(Author, slug=self.kwargs['author_slug'])
        qs = Book.objects.select_related('author', 'category').prefetch_related('images', 'reviews')
        qs = qs.filter(author=self.author)

        qs = qs.annotate(
            final_price=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        qs = qs.annotate(review_count=Count('reviews', distinct=True))

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(isbn__icontains=q) |
                Q(category__name__icontains=q)
            )

        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                qs = qs.filter(final_price__gte=float(min_price))
            except (ValueError, TypeError):
                pass
        if max_price:
            try:
                qs = qs.filter(final_price__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        rating = self.request.GET.get('rating')
        if rating:
            try:
                qs = qs.filter(average_rating__gte=float(rating))
            except (ValueError, TypeError):
                pass

        available = self.request.GET.get('available')
        if available == '1':
            qs = qs.filter(stock__gt=0)

        sort = self.request.GET.get('sort')
        if sort == 'popularity':
            qs = qs.order_by('-review_count', '-average_rating')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'price-asc':
            qs = qs.order_by('final_price')
        elif sort == 'price-desc':
            qs = qs.order_by('-final_price')
        elif sort == 'rating':
            qs = qs.order_by('-average_rating')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        context['all_categories'] = Category.objects.all()
        context['all_authors'] = Author.objects.all()

        auth_books = Book.objects.filter(author=self.author).annotate(
            fp=Case(
                When(discount_price__isnull=False, then=F('discount_price')),
                default=F('price'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ).aggregate(min_p=Min('fp'), max_p=Max('fp'))
        context['price_min'] = auth_books['min_p'] or 0
        context['price_max'] = auth_books['max_p'] or 0

        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'category': self.request.GET.getlist('category'),
            'author': self.author.slug,
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'rating': self.request.GET.get('rating', ''),
            'available': self.request.GET.get('available', ''),
        }
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', '')

        return context


class CategoryListView(ListView):
    model = Category
    paginate_by = 20
    template_name = 'books/category_list.html'
    ordering = ['name']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(book_count=Count('books'))
        return qs


class AuthorListView(ListView):
    model = Author
    paginate_by = 20
    template_name = 'books/author_list.html'
    ordering = ['name']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(book_count=Count('books'))
        return qs

class FeaturedBookListView(ListView):
    model = Book
    template_name = 'books/featured_books.html'
    context_object_name = 'featured_books'
    paginate_by = 12  # Displays 12 books per page clean layout grid

    def get_queryset(self):
        # Grabs only books where featured flag is checked true
        return Book.objects.filter(featured=True).select_related('author', 'category')