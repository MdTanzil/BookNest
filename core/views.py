from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from books.models import Book, Category, Author
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.conf import settings
import os


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_categories'] = Category.objects.all()[:9]
        ctx['best_sellers'] = Book.objects.filter(bestseller=True, stock__gt=0).select_related('author', 'category').prefetch_related('reviews')[:8]
        ctx['new_arrivals'] = Book.objects.filter(new_arrival=True, stock__gt=0).select_related('author', 'category').order_by('-created_at')[:8]
        ctx['featured_books'] = Book.objects.filter(featured=True, stock__gt=0).select_related('author', 'category')[:8]
        ctx['on_sale'] = Book.objects.filter(discount_price__isnull=False, stock__gt=0).select_related('author', 'category')[:4]
        return ctx


def about_view(request):
    return render(request, 'about.html', {'page_title': 'About BookNest'})


@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip()
    if email and '@' in email:
        messages.success(request, f"Thank you! {email} has been subscribed.")
    else:
        messages.error(request, "Please enter a valid email address.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_403(request, exception=None):
    return render(request, '403.html', status=403)


def custom_500(request):
    return render(request, '500.html', status=500)


class RobotsTxtView(TemplateView):
    template_name = 'robots.txt'
    content_type = 'text/plain'
