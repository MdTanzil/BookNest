from django.contrib import admin

from .models import Category, Author, Book, BookImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['created_at']


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'price', 'discount_price', 'final_price',
        'stock', 'is_available', 'bestseller', 'featured',
        'new_arrival', 'average_rating'
    ]
    list_editable = [
        'bestseller', 'featured', 'new_arrival',
        'price', 'discount_price', 'stock'
    ]
    list_filter = [
        'category', 'format', 'language', 'bestseller',
        'featured', 'new_arrival', 'publication_date'
    ]
    search_fields = [
        'title', 'isbn', 'author__name', 'category__name'
    ]
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['author', 'category']
    inlines = [BookImageInline]
    readonly_fields = ['average_rating', 'created_at', 'updated_at']

    fieldsets = (
        ('Book Details', {
            'fields': (
                'title', 'slug', 'author', 'category',
                'description', 'isbn', 'publisher',
                'publication_date', 'pages', 'language',
                'format', 'cover_image'
            )
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Flags', {
            'fields': ('featured', 'bestseller', 'new_arrival')
        }),
        ('Meta', {
            'fields': ('average_rating', 'created_at', 'updated_at')
        }),
    )