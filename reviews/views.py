from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from books.models import Book
from reviews.models import Review
from reviews.forms import ReviewForm


@login_required
def review_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.book = book
        review.save()
        messages.success(request, "Review submitted!")
        return redirect('books:book_detail', slug=book.slug)
    else:
        messages.error(request, "There was an error with your review. Please check the form.")
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('books:book_detail', slug=book.slug)


@login_required
def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully!")
            return redirect('books:book_detail', slug=review.book.slug)
        else:
            messages.error(request, "There was an error updating your review.")
    return redirect('books:book_detail', slug=review.book.slug)


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    slug = review.book.slug
    review.delete()
    messages.info(request, "Review deleted.")
    return redirect('books:book_detail', slug=slug)
