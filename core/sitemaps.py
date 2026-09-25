from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from books.models import Book, Category, Author


class BookSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Book.objects.filter(stock__gt=0)

    def location(self, obj):
        return f'/books/{obj.slug}/'

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f'/books/category/{obj.slug}/'


class AuthorSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Author.objects.all()

    def location(self, obj):
        return f'/books/author/{obj.slug}/'


class StaticSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['core:home', 'core:about']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'books': BookSitemap,
    'categories': CategorySitemap,
    'authors': AuthorSitemap,
    'static': StaticSitemap,
}
