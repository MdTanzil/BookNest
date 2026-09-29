from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),  
    path('category/<slug:category_slug>/', views.CategoryBooksView.as_view(), name='category_books'),
    path('author/<slug:author_slug>/', views.AuthorBooksView.as_view(), name='author_books'),
    path('bestsellers/', views.BookListView.as_view(filter='bestsellers'), name='bestsellers'),
    path('new-arrivals/', views.BookListView.as_view(filter='new'), name='new_arrivals'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('featured/', views.FeaturedBookListView.as_view(), name='featured_books'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
]
